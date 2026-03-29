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


TOPIC_LOCKED_MESSAGE = (
    "Discussion theme is locked after the debate starts. "
    "Wipe the debate or start a new session to change it."
)


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
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "topic_edit_buffer" not in st.session_state:
        st.session_state.topic_edit_buffer = st.session_state.topic_input
    if "round_temperature" not in st.session_state:
        st.session_state.round_temperature = st.session_state.target_entropy


init_session_state()


# ============================================================================
# INITIAL DATA LOAD
# ============================================================================

agents_payload = asyncio.run(api.fetch_agents_from_backend())
loaded_agents = agents_payload.get("agents", []) if isinstance(agents_payload, dict) else []
backend_error = (
    agents_payload.get("_error", "") if isinstance(agents_payload, dict) else ""
)
backend_ok, backend_probe_message = asyncio.run(api.probe_backend())

available_agents: Dict[str, str] = {
    a.get("agent_id", ""): a.get("display_name", a.get("agent_id", ""))
    for a in loaded_agents
    if a.get("agent_id")
}

legends_catalog = load_legends_registry(available_agents)
legend_map = {item["agent_id"]: item for item in legends_catalog}

if not st.session_state.default_legends_seeded and not st.session_state.selected_agents and legends_catalog:
    st.session_state.selected_agents = [item["agent_id"] for item in legends_catalog[:4]]
    st.session_state.default_legends_seeded = True

if st.session_state.selected_agents:
    st.session_state.default_legends_seeded = True

if st.session_state.topic_loaded_for_session != st.session_state.session_id:
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
                f"<p style='margin:0 0 3px 0;font-weight:700;font-size:0.98rem;color:#111111;'>{name_esc}</p>"
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
    st.markdown("<div class='exhum-sidebar-heading'>⚙️ Controls</div>", unsafe_allow_html=True)

    col_sid, col_btn = st.columns([4, 1])
    with col_sid:
        st.caption(f"Session: {st.session_state.session_id[:12]}...")
    with col_btn:
        if st.button("⟳", key="new_session_button", help="Create new session", use_container_width=True):
            st.session_state.update({
                "session_id": str(uuid4()),
                "messages": [],
                "expanded_message_keys": [],
                "speaker_progress": {},
                "turn_count": 0,
                "discussion_active": False,
                "discussion_started": False,
                "topic_input": "The future of AI in society",
                "topic_edit_mode": False,
                "topic_loaded_for_session": "",
            })
            st.session_state.topic_edit_buffer = st.session_state.topic_input
            st.rerun()

    if st.button("🪏 Select Speaker", key="open_legend_picker", use_container_width=True, type="primary"):
        legend_picker_dialog()

    st.markdown(
        "<div class='exhum-sidebar-heading'>🧾 Drafted Council</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.selected_agents:
        render_drafted_chips_component(
            st.session_state.selected_agents, available_agents
        )
    else:
        st.markdown(
            "<div class='exhum-drafted-empty'>NO ENTITIES RECOVERED.<br/>CLICK ABOVE TO START.</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='exhum-temperature-controller'>"
        "<span class='exhum-sidebar-heading'>🌀 Logic Entropy</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<span class='exhum-temperature-caption'>Set the balance between rigid logic and creative unpredictability.</span>",
        unsafe_allow_html=True,
    )
    render_entropy_slider_control()

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
            st.rerun()

    if stop:
        st.session_state.discussion_active = False
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


# ============================================================================
# MAIN AREA
# ============================================================================

col_chat, col_panel = st.columns([3, 1])

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
                message_key = f"{aid}-{turn}-{message_index}"
                is_expanded = message_key in st.session_state.expanded_message_keys
                display_body = raw_body if (len(raw_body) <= 280 or is_expanded) else raw_body[:280].rstrip() + "..."
                body = html.escape(display_body)

                with st.container():
                    st.markdown(
                        f"<div class='exhum-bubble exhum-bubble-{idx}'>"
                        f"<div class='exhum-header'>"
                        f"<div class='exhum-avatar' style='background:{accent}22; color:{accent};'>"
                        f"<img class='exhum-avatar-img' src='{avatar_url}' alt='{name}' />"
                        "</div>"
                        f"<span class='exhum-name' style='color:{accent};'>{name}</span>"
                        f"<span class='exhum-meta'>Turn {turn} - {ts}</span>"
                        "</div>"
                        f"<p>{body}</p>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                    if len(raw_body) > 280:
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
    render_section_title("👥", "Speakers")

    agent_counts: Dict[str, int] = {}
    for msg in st.session_state.messages:
        aid = msg.get("agent_id", "Unknown")
        agent_counts[aid] = agent_counts.get(aid, 0) + 1

    if st.session_state.selected_agents:
        display_speakers = list(st.session_state.selected_agents)
    elif agent_counts:
        display_speakers = [aid for aid, _ in sorted(agent_counts.items(), key=lambda x: -x[1])]
    else:
        display_speakers = []

    if display_speakers:
        for aid in display_speakers:
            count = agent_counts.get(aid, 0)
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
            current_progress = float(st.session_state.speaker_progress.get(aid, 0.0))
            progress_text = "done" if current_progress >= 1.0 else "waiting"
            slot = st.empty()
            slot.markdown(
                render_speaker_card_html(
                    name=name, avatar_url=avatar_url, accent=accent,
                    turns=count, progress=current_progress, progress_text=progress_text,
                    archetype=archetype,
                ),
                unsafe_allow_html=True,
            )
            speaker_progress_bars[aid] = {
                "slot": slot, "name": name, "avatar_url": avatar_url,
                "accent": accent, "turns": count, "archetype": archetype,
            }
    else:
        st.caption("No speakers yet.")

    render_section_title("📡", "Telemetry")
    render_telemetry_panel(
        messages=st.session_state.messages,
        selected_agents=st.session_state.selected_agents,
        available_agents=available_agents,
        mode_class="exhum-telemetry-desktop",
    )

render_telemetry_panel(
    messages=st.session_state.messages,
    selected_agents=st.session_state.selected_agents,
    available_agents=available_agents,
    mode_class="exhum-telemetry-mobile",
)


# ============================================================================
# TURN EXECUTION
# ============================================================================

if st.session_state.discussion_active and st.session_state.selected_agents:
    def _update_card(aid: str, progress: float, text: str, extra_turns: int = 0) -> None:
        if aid in speaker_progress_bars:
            d = speaker_progress_bars[aid]
            d["slot"].markdown(
                render_speaker_card_html(
                    name=d["name"], avatar_url=d["avatar_url"], accent=d["accent"],
                    turns=d["turns"] + extra_turns, progress=progress, progress_text=text,
                    archetype=d.get("archetype", ""),
                ),
                unsafe_allow_html=True,
            )

    async def run_round() -> None:
        topic = st.session_state.topic_input
        temperature = float(st.session_state.round_temperature)
        next_turn_number = int(st.session_state.turn_count) + 1
        for agent_id in st.session_state.selected_agents:
            st.session_state.speaker_progress[agent_id] = 0.25
            _update_card(agent_id, 0.25, "processing...")

            turn_started_at = time.perf_counter()
            response = await api.process_agent_turn(
                session_id=st.session_state.session_id,
                topic=topic,
                agent_id=agent_id,
                temperature=temperature,
                turn_number=next_turn_number,
            )
            st.session_state.last_inference_latency_ms = (time.perf_counter() - turn_started_at) * 1000.0

            if response:
                st.session_state.messages.append({
                    "agent_id": response.get("agent_id"),
                    "display_name": response.get("display_name", ""),
                    "message": response.get("message"),
                    "turn_number": response.get("turn_number"),
                    "created_at": response.get("created_at", datetime.utcnow().isoformat()),
                })
                st.session_state.turn_count += 1
                next_turn_number += 1
                update_debate_entropy()
                st.session_state.speaker_progress[agent_id] = 1.0
                _update_card(agent_id, 1.0, "done", extra_turns=1)
            else:
                st.session_state.speaker_progress[agent_id] = 0.0
                _update_card(agent_id, 0.0, "failed")

    asyncio.run(run_round())
    st.session_state.discussion_active = False
    st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

st.markdown(
    "<div class='exhum-sticky-footer'>EXHUMED | Digital Exhumation of Historical Logic.</div>",
    unsafe_allow_html=True,
)
