"""
EXHUMED: Streamlit Frontend
Interactive UI for AI discussion platform
"""

import asyncio
import html
import logging
import time
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4

import streamlit as st
import streamlit.components.v1 as components

from styles import apply_styles
import api
from components import (
    ACCENT_COLORS,
    get_style_index,
    get_avatar_url,
    get_logo_data_uri,
    load_legends_registry,
    toggle_legend_selection,
    render_drafted_chips_component,
    render_telemetry_panel,
    render_speaker_card_html,
    save_topic_from_inline_editor,
    _cancel_topic_edit,
    _toggle_message_expansion,
    render_entropy_slider_control,
    update_debate_entropy,
)

st.set_page_config(
    page_title="EXHUMED",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

apply_styles()


def ensure_sidebar_open_on_load() -> None:
    components.html(
        """
        <script>
        (function () {
          const SESSION_KEY = "exhumed_sidebar_opened_once";
          const parentWindow = window.parent;
          const parentDoc = parentWindow.document;

          function openSidebarIfNeeded() {
            const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
            const collapsedControl =
              parentDoc.querySelector('[data-testid="collapsedControl"] button') ||
              parentDoc.querySelector('[data-testid="collapsedControl"]');

            if (sessionStorage.getItem(SESSION_KEY) === "1") {
              return true;
            }

            if (sidebar && collapsedControl) {
              collapsedControl.click();
              sessionStorage.setItem(SESSION_KEY, "1");
              return true;
            }

            if (sidebar && !collapsedControl) {
              sessionStorage.setItem(SESSION_KEY, "1");
              return true;
            }

            return false;
          }

          if (openSidebarIfNeeded()) {
            return;
          }

          const observer = new MutationObserver(() => {
            if (openSidebarIfNeeded()) {
              observer.disconnect();
            }
          });

          observer.observe(parentDoc.body, { childList: true, subtree: true });
          setTimeout(() => observer.disconnect(), 4000);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


ensure_sidebar_open_on_load()


def render_section_title(icon: str, label: str, extra_class: str = "") -> None:
    class_attr = "exhum-section-title"
    if extra_class:
        class_attr += f" {extra_class}"
    st.markdown(
        (
            f"<div class='{class_attr}'>"
            f"<span class='exhum-section-icon'>{icon}</span>"
            f"<span class='exhum-sidebar-heading'>{label}</span>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_sidebar_heading(label: str, extra_class: str = "") -> None:
    class_attr = "exhum-sidebar-heading"
    if extra_class:
        class_attr += f" {extra_class}"
    st.markdown(
        f"<div class='{class_attr}'>{label}</div>",
        unsafe_allow_html=True,
    )


TOPIC_LOCKED_MESSAGE = (
    "Discussion theme is locked after the debate starts. "
    "Wipe the debate or start a new session to change it."
)

DEFAULT_COUNCIL_AGENT_IDS = ["agt_001", "agt_002", "agt_003", "agt_004"]


def open_topic_edit_mode() -> None:
    st.session_state.topic_edit_mode = True
    st.session_state.topic_edit_buffer = st.session_state.topic_input


def handle_topic_edit_button_click() -> None:
    if st.session_state.discussion_started or st.session_state.messages:
        st.session_state.topic_edit_mode = False
        toast = getattr(st, "toast", None)
        if callable(toast):
            toast(TOPIC_LOCKED_MESSAGE)
        else:
            st.info(TOPIC_LOCKED_MESSAGE)
        return
    open_topic_edit_mode()


def _render_message_body(raw_body: str, is_expanded: bool) -> str:
    if len(raw_body) <= 280 or is_expanded:
        return html.escape(raw_body)
    return html.escape(raw_body[:280].rstrip() + "...")


# ============================================================================
# SESSION STATE
# ============================================================================


def init_session_state() -> None:
    defaults = {
        "session_id": str(uuid4()),
        "messages": [],
        "discussion_active": False,
        "discussion_started": False,
        "turn_count": 0,
        "topic_input": "The future of AI in society",
        "topic_edit_mode": False,
        "selected_agents": [],
        "topic_loaded_for_session": "",
        "expanded_message_keys": [],
        "speaker_progress": {},
        "default_legends_seeded": False,
        "last_inference_latency_ms": 0.0,
        "debate_entropy": 0.37,
        "estimated_tokens": 0,
        "session_burn_usd": 0.0,
        "target_entropy": 0.7,
        "current_agent_index": 0,
        "current_turn_number": 1,
        "thinking_message_id": "",
        "thinking_visible": False,
        "telemetry_live": False,
        "agents_backend_url": "",
        "agents_payload_cache": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "topic_edit_buffer" not in st.session_state:
        st.session_state.topic_edit_buffer = st.session_state.topic_input
    if "round_temperature" not in st.session_state:
        st.session_state.round_temperature = st.session_state.target_entropy


init_session_state()


def load_agents_payload() -> Dict[str, Any]:
    cached_backend_url = str(st.session_state.get("agents_backend_url", ""))
    cached_payload = st.session_state.get("agents_payload_cache")
    if cached_payload is not None and cached_backend_url == api.BACKEND_URL:
        return cached_payload

    payload = asyncio.run(api.fetch_agents_from_backend())
    st.session_state.agents_backend_url = api.BACKEND_URL
    st.session_state.agents_payload_cache = payload
    return payload


def get_default_council_agent_ids(available_agents: Dict[str, str]) -> list[str]:
    available_default_ids = [
        agent_id for agent_id in DEFAULT_COUNCIL_AGENT_IDS if agent_id in available_agents
    ]
    if available_default_ids:
        return available_default_ids
    return list(available_agents.keys())[:4]


# ============================================================================
# INITIAL DATA LOAD
# ============================================================================

agents_payload = load_agents_payload()
loaded_agents = agents_payload.get("agents", []) if isinstance(agents_payload, dict) else []
backend_error = (
    agents_payload.get("_error", "") if isinstance(agents_payload, dict) else ""
)
backend_ok = not bool(backend_error)
backend_probe_message = ""

available_agents: Dict[str, str] = {
    a.get("agent_id", ""): a.get("display_name", a.get("agent_id", ""))
    for a in loaded_agents
    if a.get("agent_id")
}

legends_catalog = load_legends_registry(available_agents)
legend_map = {item["agent_id"]: item for item in legends_catalog}

if (
    not st.session_state.default_legends_seeded
    and not st.session_state.selected_agents
    and available_agents
):
    st.session_state.selected_agents = get_default_council_agent_ids(available_agents)
    st.session_state.default_legends_seeded = True

if st.session_state.selected_agents:
    st.session_state.default_legends_seeded = True

if st.session_state.topic_loaded_for_session != st.session_state.session_id:
    if not str(st.session_state.topic_input).strip():
        backend_topic = asyncio.run(api.fetch_session_topic(st.session_state.session_id))
        if backend_topic:
            st.session_state.topic_input = backend_topic
            st.session_state.topic_edit_buffer = backend_topic
    st.session_state.topic_loaded_for_session = st.session_state.session_id

if not backend_ok:
    st.error(
        backend_error or backend_probe_message or "Backend connection failed."
    )
    st.caption(f"Configured backend URL: `{api.BACKEND_URL}`")


# ============================================================================
# LEGEND PICKER DIALOG
# ============================================================================

@st.dialog(" ", width="large", on_dismiss="rerun")
def legend_picker_dialog() -> None:
    render_section_title("☷", "Council Draft Board")
    st.caption("Select which voices enter the chamber.")
    grid_cols = st.columns(4)

    for idx, legend in enumerate(legends_catalog):
        aid = legend["agent_id"]
        selected = aid in st.session_state.selected_agents
        card_class = "exhum-legend-card exhum-legend-selected" if selected else "exhum-legend-card"
        with grid_cols[idx % 4]:
            avatar_url = get_avatar_url(aid, legend["display_name"])
            name_esc = legend["display_name"].replace("'", "&#39;").replace('"', "&quot;")
            arch_esc = legend["archetype"].replace("'", "&#39;").replace('"', "&quot;")
            drafted_badge = "<span class='exhum-legend-state-badge'>✅ Drafted</span>" if selected else ""
            draft_button_key = f"draft_remove_{aid}" if selected else f"draft_add_{aid}"
            st.markdown(
                f"<div class='{card_class}' style='display:block;'>"
                f"{drafted_badge}"
                f"<img class='exhum-legend-avatar' src='{avatar_url}' alt='{name_esc}'"
                " style='display:block;width:44px;height:44px;object-fit:cover;"
                "border:2px solid #000;border-radius:0;box-shadow:2px 2px 0 0 #000;margin-bottom:6px;' />"
                f"<p class='exhum-legend-name'>{name_esc}</p>"
                f"<p class='exhum-legend-meta'>{arch_esc}</p>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.button(
                "❌ Remove from Council" if selected else "⚡ Draft to Council",
                key=draft_button_key,
                use_container_width=True,
                on_click=toggle_legend_selection,
                args=(aid,),
            )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    _, close_col = st.columns([3, 2])
    with close_col:
        if st.button("🔄 Update Council Lineup", key="close_legend_picker",
                     use_container_width=True, type="primary"):
            st.rerun()


# ============================================================================
# SIDEBAR
# ============================================================================

speaker_progress_bars: Dict[str, Any] = {}

with st.sidebar:
    with st.container(key="sidebar_root"):
        logo_uri = get_logo_data_uri()
        logo_html = (
            f"<img class='exhum-brand-logo' src='{logo_uri}' alt='EXHUMED logo' />"
            if logo_uri
            else "<div style='text-align:center;font-size:72px;line-height:1;margin:0 0 10px 0;'>🎭</div>"
        )
        st.markdown(logo_html, unsafe_allow_html=True)
        st.markdown(
            "<div class='exhum-brand-copy'>"
            "<div class='exhum-brand-title'>EXHUMED</div>"
            "<div class='exhum-brand-subtitle'>Digital Exhumation of Historical Logic.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button("🪏 Select Speaker", key="open_legend_picker", use_container_width=True, type="primary"):
            legend_picker_dialog()

        render_sidebar_heading("Drafted Council")

        if st.session_state.selected_agents:
            render_drafted_chips_component(
                st.session_state.selected_agents, available_agents
            )
        else:
            st.markdown(
                "<div class='exhum-drafted-empty'>NO ENTITIES RECOVERED.<br/>CLICK ABOVE TO START.</div>",
                unsafe_allow_html=True,
            )

        with st.container(key="sidebar_entropy"):
            render_sidebar_heading("Logic Entropy", extra_class="exhum-temperature-controller")
            st.markdown(
                "<span class='exhum-temperature-caption'>Adjust between rigid logic & creative unpredictability.</span>",
                unsafe_allow_html=True,
            )
            render_entropy_slider_control()

        render_sidebar_heading("Commands")

        start = st.button("▶️ Start Debate", key="start_button", use_container_width=True)
        stop = st.button("⏸️ Halt Debate", key="pause_button", use_container_width=True)
        clear = st.button("🧹 Wipe Debate", key="clear_button", use_container_width=True)

        if start:
            if not st.session_state.topic_input.strip():
                st.error("Set a discussion topic first.")
            elif not st.session_state.selected_agents:
                st.error("Draft at least one legend.")
            else:
                topic_to_run = st.session_state.topic_input.strip()
                st.session_state.topic_input = topic_to_run
                st.session_state.topic_edit_buffer = topic_to_run
                asyncio.run(api.push_session_topic(st.session_state.session_id, topic_to_run))
                st.session_state.round_temperature = float(st.session_state.target_entropy)
                st.session_state.discussion_active = True
                st.session_state.discussion_started = True
                st.session_state.speaker_progress = {aid: 0.0 for aid in st.session_state.selected_agents}
                st.session_state.current_agent_index = 0
                st.session_state.current_turn_number = int(st.session_state.turn_count) + 1
                st.session_state.thinking_message_id = ""
                st.session_state.thinking_visible = False
                st.rerun()

        if stop:
            st.session_state.discussion_active = False
            st.session_state.current_agent_index = 0
            st.session_state.thinking_message_id = ""
            st.session_state.thinking_visible = False
            st.info("Round paused.")

        if clear:
            clear_ok = asyncio.run(api.clear_session(st.session_state.session_id))
            st.session_state.update({
                "messages": [],
                "expanded_message_keys": [],
                "speaker_progress": {},
                "turn_count": 0,
                "discussion_active": False,
                "discussion_started": False,
                "topic_edit_mode": False,
                "current_agent_index": 0,
                "current_turn_number": 1,
                "thinking_message_id": "",
                "thinking_visible": False,
            })
            st.session_state.topic_edit_buffer = st.session_state.topic_input
            if clear_ok:
                st.success("Debate cleared.")
            else:
                st.warning("Debate cleared locally, but backend cleanup failed.")

        if st.button("📄 Download Transcript", use_container_width=True):
            if not st.session_state.messages:
                st.warning("No messages to export.")
            else:
                with st.spinner("Generating PDF..."):
                    pdf_bytes = asyncio.run(api.download_pdf_export(st.session_state.session_id))
                if pdf_bytes:
                    st.download_button(
                        "Download",
                        data=pdf_bytes,
                        file_name=f"exhumed_{st.session_state.session_id[:8]}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

        render_sidebar_heading("Session")
        st.caption(f"Current session: {st.session_state.session_id[:12]}...")
        if st.button("⟳ Renew Session", key="new_session_button", help="Create new session", use_container_width=True):
            st.session_state.update({
                "session_id": str(uuid4()),
                "messages": [],
                "expanded_message_keys": [],
                "selected_agents": get_default_council_agent_ids(available_agents),
                "speaker_progress": {},
                "turn_count": 0,
                "discussion_active": False,
                "discussion_started": False,
                "topic_input": "The future of AI in society",
                "topic_edit_mode": False,
                "topic_loaded_for_session": "",
                "default_legends_seeded": True,
                "current_agent_index": 0,
                "current_turn_number": 1,
                "thinking_message_id": "",
                "thinking_visible": False,
            })
            st.session_state.topic_edit_buffer = st.session_state.topic_input
            st.rerun()


# ============================================================================
# MAIN AREA
# ============================================================================

col_chat, col_panel = st.columns([3, 1])
agent_counts: Dict[str, int] = {}
for msg in st.session_state.messages:
    aid = msg.get("agent_id", "Unknown")
    if msg.get("is_thinking"):
        continue
    agent_counts[aid] = agent_counts.get(aid, 0) + 1

if st.session_state.selected_agents:
    display_speakers = list(st.session_state.selected_agents)
elif agent_counts:
    display_speakers = [aid for aid, _ in sorted(agent_counts.items(), key=lambda x: -x[1])]
else:
    display_speakers = []

with col_chat:
    topic_locked = st.session_state.discussion_started or len(st.session_state.messages) > 0
    st.markdown("## 💬 Discussion")

    if not st.session_state.topic_edit_mode:
        st.session_state.topic_edit_buffer = st.session_state.topic_input
        safe_topic = st.session_state.topic_input.replace("<", "&lt;").replace(">", "&gt;")
        hero_col, edit_col = st.columns([18, 1])
        with hero_col:
            st.markdown(
                f"<div class='exhum-topic-hero'>"
                f"<p class='exhum-topic-title'>{safe_topic}</p>"
                "</div>",
                unsafe_allow_html=True,
            )
        with edit_col:
            if topic_locked:
                st.markdown(
                    """
                    <style>
                    div[class*="st-key-topic_edit_toggle"] button {
                        background: #e5e7eb !important;
                        color: #6b7280 !important;
                        box-shadow: none !important;
                        transform: none !important;
                        cursor: not-allowed !important;
                    }
                    div[class*="st-key-topic_edit_toggle"] button:hover {
                        background: #e5e7eb !important;
                        color: #6b7280 !important;
                        box-shadow: none !important;
                        transform: none !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
            st.button(
                "✏️",
                key="topic_edit_toggle",
                help=TOPIC_LOCKED_MESSAGE if topic_locked else "Edit discussion theme",
                on_click=handle_topic_edit_button_click,
                use_container_width=True,
            )
    else:
        st.text_input(
            "Discussion Topic",
            key="topic_edit_buffer",
            on_change=save_topic_from_inline_editor,
            help="Press Enter to save immediately.",
        )
        c_save, c_cancel = st.columns(2)
        with c_save:
            if st.button("💾 Save Topic", key="save_topic_btn", use_container_width=True):
                save_topic_from_inline_editor()
        with c_cancel:
            st.button("↩️ Cancel", key="cancel_topic_btn", use_container_width=True,
                      on_click=_cancel_topic_edit)

    status_live = st.session_state.discussion_started or len(st.session_state.messages) > 0
    status_class = "exhum-badge-live" if status_live else "exhum-badge-draft"
    status_text = "Live" if status_live else "Dormant"
    st.markdown(
        f"<span class='exhum-badge {status_class}'>📡 Status: {status_text}</span>",
        unsafe_allow_html=True,
    )

    if display_speakers:
        for aid in display_speakers:
            stored_name = next(
                (m.get("display_name") for m in st.session_state.messages
                 if m.get("agent_id") == aid and m.get("display_name")),
                None,
            )
            name = available_agents.get(aid) or stored_name or aid
            idx = get_style_index(aid)
            accent = ACCENT_COLORS[idx]
            avatar_url = get_avatar_url(aid, name)
            archetype = legend_map.get(aid, {}).get("archetype", "")
            speaker_progress_bars[aid] = {
                "name": name,
                "avatar_url": avatar_url,
                "accent": accent,
                "turns": agent_counts.get(aid, 0),
                "archetype": archetype,
            }

    with st.container(border=False):
        if not st.session_state.messages:
            st.markdown(
                "<div class='exhum-empty'><h3>🎬 Ready to start</h3>"
                "<p>Use ✨ Add Legend and press ▶️ Start</p></div>",
                unsafe_allow_html=True,
            )
        else:
            for message_index, msg in enumerate(st.session_state.messages):
                aid = msg.get("agent_id", "")
                name = available_agents.get(aid) or msg.get("display_name") or aid
                idx = get_style_index(aid)
                accent = ACCENT_COLORS[idx]
                avatar_url = get_avatar_url(aid, name)
                ts = msg.get("created_at", "")
                if ts and "T" in ts:
                    ts = ts.split("T")[1][:5]

                turn = msg.get("turn_number", "-")
                raw_body = str(msg.get("message", ""))
                is_thinking = bool(msg.get("is_thinking"))
                message_key = f"{aid}-{turn}-{message_index}"
                is_expanded = message_key in st.session_state.expanded_message_keys
                body = _render_message_body(raw_body, is_expanded)
                progress = float(st.session_state.speaker_progress.get(aid, 0.0))
                thinking_text = "<span class='exhum-thinking-pulse'>Agent is formulating logic...</span>"
                thinking_progress_html = ""
                if is_thinking:
                    thinking_progress_html = (
                        "<div class='exhum-bubble-progress-track exhum-bubble-progress-track-inline'>"
                        f"<div class='exhum-bubble-progress-fill' style='width:{max(8.0, progress * 100.0):.1f}%'></div>"
                        "</div>"
                    )

                with st.container():
                    st.markdown(
                        f"<div class='exhum-bubble exhum-bubble-{idx}'>"
                        f"{thinking_progress_html}"
                        f"<div class='exhum-header exhum-bubble-header-static'>"
                        f"<div class='exhum-avatar' style='background:{accent}22; color:{accent};'>"
                        f"<img class='exhum-avatar-img' src='{avatar_url}' alt='{name}' />"
                        "</div>"
                        "<div class='exhum-bubble-header-main'>"
                        f"<span class='exhum-name' style='color:{accent};'>{name}</span>"
                        f"<span class='exhum-meta'>Turn {turn} - {ts}</span>"
                        "</div>"
                        "</div>"
                        f"<p>{thinking_text if is_thinking else body}</p>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                    if (not is_thinking) and len(raw_body) > 280:
                        st.markdown(
                            f"<span class='exhum-read-more-anchor exhum-read-more-color-{idx}'></span>",
                            unsafe_allow_html=True,
                        )
                        st.button(
                            "Read less" if is_expanded else "Read more",
                            key=f"toggle_message_{message_key}",
                            on_click=_toggle_message_expansion,
                            args=(message_key,),
                        )

with col_panel:
    with st.container(key="telemetry_panel"):
        st.markdown(
            "<div class='exhum-telemetry-hero'>"
            "<span class='exhum-telemetry-kicker'>Runtime Monitor</span>"
            "<div class='exhum-telemetry-title'>Telemetry</div>"
            "<p class='exhum-telemetry-subtitle'>Live model health, context pressure, spend, and speaking balance.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.toggle(
            "Live backend metrics",
            key="telemetry_live",
            help="Enable live telemetry and service checks. Leaving this off improves page load and rerun speed.",
        )
        render_telemetry_panel(
            messages=st.session_state.messages,
            selected_agents=st.session_state.selected_agents,
            available_agents=available_agents,
            key_prefix="exhum_telemetry",
            fetch_live=bool(st.session_state.telemetry_live),
        )


# ============================================================================
# TURN EXECUTION
# ============================================================================

if st.session_state.discussion_active and st.session_state.selected_agents:
    def _update_card(aid: str, progress: float, text: str, extra_turns: int = 0) -> None:
        if aid in speaker_progress_bars:
            d = speaker_progress_bars[aid]
            d["turns"] = d.get("turns", 0) + extra_turns

    current_index = int(st.session_state.current_agent_index)
    if current_index >= len(st.session_state.selected_agents):
        st.session_state.discussion_active = False
        st.session_state.current_agent_index = 0
        st.session_state.current_turn_number = int(st.session_state.turn_count) + 1
        st.session_state.thinking_message_id = ""
        st.session_state.thinking_visible = False
        st.rerun()

    current_agent_id = st.session_state.selected_agents[current_index]

    if not st.session_state.thinking_visible:
        display_name = available_agents.get(current_agent_id) or current_agent_id
        st.session_state.speaker_progress[current_agent_id] = 0.25
        st.session_state.messages.append({
            "id": f"thinking-{current_agent_id}-{st.session_state.current_turn_number}",
            "agent_id": current_agent_id,
            "display_name": display_name,
            "message": "",
            "turn_number": st.session_state.current_turn_number,
            "created_at": datetime.utcnow().isoformat(),
            "is_thinking": True,
        })
        st.session_state.thinking_message_id = f"thinking-{current_agent_id}-{st.session_state.current_turn_number}"
        st.session_state.thinking_visible = True
        _update_card(current_agent_id, 0.25, "thinking...")
        st.rerun()

    async def run_current_turn() -> None:
        topic = st.session_state.topic_input
        temperature = float(st.session_state.round_temperature)
        turn_started_at = time.perf_counter()
        response = await api.process_agent_turn(
            session_id=st.session_state.session_id,
            topic=topic,
            agent_id=current_agent_id,
            temperature=temperature,
            turn_number=int(st.session_state.current_turn_number),
        )
        st.session_state.last_inference_latency_ms = (time.perf_counter() - turn_started_at) * 1000.0

        target_id = st.session_state.thinking_message_id
        target_message = next(
            (msg for msg in reversed(st.session_state.messages) if msg.get("id") == target_id),
            None,
        )

        if response and target_message is not None:
            target_message.update({
                "agent_id": response.get("agent_id"),
                "display_name": response.get("display_name", ""),
                "message": response.get("message"),
                "turn_number": response.get("turn_number"),
                "created_at": response.get("created_at", datetime.utcnow().isoformat()),
                "is_thinking": False,
            })
            st.session_state.turn_count += 1
            update_debate_entropy()
            st.session_state.speaker_progress[current_agent_id] = 1.0
            _update_card(current_agent_id, 1.0, "done", extra_turns=1)
        else:
            if target_message is not None:
                target_message.update({
                    "message": "Agent failed to produce a response.",
                    "is_thinking": False,
                    "created_at": datetime.utcnow().isoformat(),
                })
            st.session_state.speaker_progress[current_agent_id] = 0.0
            _update_card(current_agent_id, 0.0, "failed")

        st.session_state.current_agent_index += 1
        st.session_state.current_turn_number = int(st.session_state.turn_count) + 1
        st.session_state.thinking_message_id = ""
        st.session_state.thinking_visible = False

    asyncio.run(run_current_turn())
    st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

st.markdown(
    "<div class='exhum-sticky-footer'>EXHUMED | Digital Exhumation of Historical Logic.</div>",
    unsafe_allow_html=True,
)
