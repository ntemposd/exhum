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
    SESSION_COST_HELPER_TEXT,
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
st.markdown(
    """
    <style>
    @media (max-width: 1024px) {
        .stApp [data-testid="stAppViewContainer"] .main .block-container,
        .stApp .stMainBlockContainer.block-container {
            padding-top: calc(var(--exhum-main-top-gap) * 0.62) !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }

        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }

        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:has(.st-key-telemetry_panel) {
            margin-top: 0.9rem !important;
        }

        .exhum-telemetry-title,
        .exhum-sidebar-heading,
        .exhum-section-title,
        .exhum-brand-title {
            white-space: nowrap;
        }

        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button,
        .stTextInput,
        .stTextInput > div,
        .stSelectbox,
        .stSlider {
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def ensure_sidebar_open_on_load() -> None:
    if st.session_state.get("close_sidebar_after_start"):
        return

    components.html(
        """
        <script>
        (function () {
          const parentWindow = window.parent;
          const parentDoc = parentWindow.document;
          const MAX_ATTEMPTS = 80;
          const RETRY_MS = 150;

          function findOpenControl() {
            return (
              parentDoc.querySelector('[data-testid="collapsedControl"] button') ||
              parentDoc.querySelector('[data-testid="collapsedControl"]') ||
              parentDoc.querySelector('button[aria-label*="Open sidebar"]') ||
              parentDoc.querySelector('button[title*="Open sidebar"]')
            );
          }

          function findCloseControl() {
            return (
              parentDoc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
              parentDoc.querySelector('[data-testid="stSidebarCollapseButton"]') ||
              parentDoc.querySelector('button[aria-label*="Close sidebar"]') ||
              parentDoc.querySelector('button[title*="Close sidebar"]')
            );
          }

          function dispatchClick(element) {
            if (!element) return false;
            ['pointerdown', 'mousedown', 'mouseup', 'click'].forEach((eventName) => {
              element.dispatchEvent(new MouseEvent(eventName, {
                bubbles: true,
                cancelable: true,
                view: parentWindow,
              }));
            });
            return true;
          }

          function isSidebarOpen() {
            const closeControl = findCloseControl();
            if (closeControl) return true;

            const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return false;

            const expandedAttr = sidebar.getAttribute('aria-expanded');
            if (expandedAttr === 'true') return true;
            if (expandedAttr === 'false') return false;

            const computedStyle = parentWindow.getComputedStyle(sidebar);
            return computedStyle.transform === 'none' || !computedStyle.transform.includes('-');
          }

          function openSidebarIfNeeded() {
            if (parentWindow.__exhumSidebarAutoOpened || isSidebarOpen()) {
              parentWindow.__exhumSidebarAutoOpened = true;
              return true;
            }

            const openControl = findOpenControl();
            if (!openControl) return false;

            dispatchClick(openControl);
            const opened = isSidebarOpen();
            if (opened) {
              parentWindow.__exhumSidebarAutoOpened = true;
            }
            return opened;
          }

          if (openSidebarIfNeeded()) return;

          let attempts = 0;
          const interval = parentWindow.setInterval(() => {
            attempts += 1;
            if (openSidebarIfNeeded() || attempts >= MAX_ATTEMPTS) {
              parentWindow.clearInterval(interval);
              observer.disconnect();
            }
          }, RETRY_MS);

          const observer = new MutationObserver(() => {
            if (openSidebarIfNeeded()) {
              observer.disconnect();
              parentWindow.clearInterval(interval);
            }
          });

          observer.observe(parentDoc.body, { childList: true, subtree: true, attributes: true });
          parentWindow.setTimeout(() => {
            observer.disconnect();
            parentWindow.clearInterval(interval);
          }, MAX_ATTEMPTS * RETRY_MS);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def close_sidebar_after_mobile_start() -> None:
    if not st.session_state.get("close_sidebar_after_start"):
        return

    components.html(
        """
        <script>
        (function () {
          const parentWindow = window.parent;
          const parentDoc = parentWindow.document;
          const MAX_ATTEMPTS = 80;
          const RETRY_MS = 150;

          if ((parentWindow.innerWidth || 0) > 1024) {
            return;
          }

          function findOpenControl() {
            return (
              parentDoc.querySelector('[data-testid="collapsedControl"] button') ||
              parentDoc.querySelector('[data-testid="collapsedControl"]') ||
              parentDoc.querySelector('button[aria-label*="Open sidebar"]') ||
              parentDoc.querySelector('button[title*="Open sidebar"]')
            );
          }

          function findCloseControl() {
            return (
              parentDoc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
              parentDoc.querySelector('[data-testid="stSidebarCollapseButton"]') ||
              parentDoc.querySelector('button[aria-label*="Close sidebar"]') ||
              parentDoc.querySelector('button[title*="Close sidebar"]')
            );
          }

          function dispatchClick(element) {
            if (!element) return false;
            ['pointerdown', 'mousedown', 'mouseup', 'click'].forEach((eventName) => {
              element.dispatchEvent(new MouseEvent(eventName, {
                bubbles: true,
                cancelable: true,
                view: parentWindow,
              }));
            });
            return true;
          }

          function isSidebarClosed() {
            const openControl = findOpenControl();
            if (openControl) return true;

            const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return false;

            const expandedAttr = sidebar.getAttribute('aria-expanded');
            if (expandedAttr === 'false') return true;
            if (expandedAttr === 'true') return false;

            const computedStyle = parentWindow.getComputedStyle(sidebar);
            return computedStyle.transform !== 'none' && computedStyle.transform.includes('-');
          }

          function closeSidebarIfNeeded() {
            if (isSidebarClosed()) return true;

            const closeControl = findCloseControl();
            if (!closeControl) return false;

            dispatchClick(closeControl);
            return isSidebarClosed();
          }

          if (closeSidebarIfNeeded()) return;

          let attempts = 0;
          const interval = parentWindow.setInterval(() => {
            attempts += 1;
            if (closeSidebarIfNeeded() || attempts >= MAX_ATTEMPTS) {
              parentWindow.clearInterval(interval);
              observer.disconnect();
            }
          }, RETRY_MS);

          const observer = new MutationObserver(() => {
            if (closeSidebarIfNeeded()) {
              observer.disconnect();
              parentWindow.clearInterval(interval);
            }
          });

          observer.observe(parentDoc.body, { childList: true, subtree: true, attributes: true });
          parentWindow.setTimeout(() => {
            observer.disconnect();
            parentWindow.clearInterval(interval);
          }, MAX_ATTEMPTS * RETRY_MS);
        })();
        </script>
        """,
        height=0,
        width=0,
    )
    st.session_state.close_sidebar_after_start = False


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
        visible_text = raw_body
    else:
        visible_text = raw_body[:280].rstrip() + "..."
    escaped = html.escape(visible_text)
    return escaped.replace("\n\n", "<br><br>").replace("\n", "<br>")


def render_discussion_panel(
    available_agents: Dict[str, str],
    legend_map: Dict[str, Dict[str, str]],
    display_speakers: list[str],
    agent_counts: Dict[str, int],
    speaker_progress_bars: Dict[str, Any],
) -> None:
    with st.container(key="discussion_panel"):
        topic_locked = st.session_state.discussion_started or len(st.session_state.messages) > 0
        st.markdown(
            "<div class='exhum-telemetry-hero'>"
            "<div class='exhum-telemetry-title'>Discussion</div>"
            "<p class='exhum-telemetry-subtitle'>Debate topic and transcript.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        status_live = st.session_state.discussion_started or len(st.session_state.messages) > 0
        status_text = "Live" if status_live else "Dormant"
        st.markdown(
            "<div class='exhum-discussion-status-row'>"
            f"<span class='exhum-discussion-status-note'>Status: {status_text}</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        if not st.session_state.topic_edit_mode:
            st.session_state.topic_edit_buffer = st.session_state.topic_input
            safe_topic = html.escape(st.session_state.topic_input)
            with st.container(key="discussion_topic_shell"):
                topic_card_class = "exhum-topic-hero exhum-topic-hero-clickable"
                if topic_locked:
                    topic_card_class += " exhum-topic-hero-locked"
                st.markdown(
                    f"<div class='{topic_card_class}' data-topic-editable={'false' if topic_locked else 'true'}>"
                    f"<p class='exhum-topic-title'>{safe_topic}</p>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                helper_text = (
                    "Discussion theme is locked after the debate starts."
                    if topic_locked
                    else "Press the debate topic box above to edit."
                )
                st.markdown(
                    f"<div class='exhum-discussion-helper'>{helper_text}</div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "Edit discussion theme",
                    key="topic_edit_trigger",
                    help=TOPIC_LOCKED_MESSAGE if topic_locked else "Click to edit discussion theme",
                    on_click=handle_topic_edit_button_click,
                    use_container_width=False,
                    disabled=topic_locked,
                )
                if not topic_locked:
                    components.html(
                        """
                        <script>
                        (function () {
                          const parentDoc = window.parent.document;
                                                function bindTopicClick() {
                                                    const shell = parentDoc.querySelector('.st-key-discussion_topic_shell');
                                                    if (!shell) return false;

                                                    const card = shell.querySelector('.exhum-topic-hero-clickable[data-topic-editable="true"]');
                                                    const trigger = shell.querySelector('div[class*="st-key-topic_edit_trigger"] button') ||
                                                        shell.querySelector('[data-testid="stButton"] button');

                                                    if (!card || !trigger) return false;
                                                    if (card.dataset.topicClickBound === 'true') return true;

                                                    const openEditor = function (event) {
                                                        event.preventDefault();
                                                        event.stopPropagation();
                                                        trigger.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: parentDoc.defaultView }));
                                                    };

                                                    card.dataset.topicClickBound = 'true';
                                                    card.setAttribute('role', 'button');
                                                    card.setAttribute('tabindex', '0');
                                                    card.addEventListener('click', openEditor);
                                                    card.addEventListener('keydown', function (event) {
                                                        if (event.key === 'Enter' || event.key === ' ') {
                                                            openEditor(event);
                                                        }
                                                    });
                                                    return true;
                                                }

                                                if (bindTopicClick()) return;

                                                let attempts = 0;
                                                const interval = window.setInterval(function () {
                                                    attempts += 1;
                                                    if (bindTopicClick() || attempts > 30) {
                                                        window.clearInterval(interval);
                                                    }
                                                }, 150);
                        })();
                        </script>
                        """,
                        height=0,
                        width=0,
                    )
        else:
            with st.form("topic_edit_form", border=False):
                st.text_input(
                    "Discussion Topic",
                    key="topic_edit_buffer",
                    help="Edit the discussion theme and save when ready.",
                )
                c_save, c_cancel = st.columns(2)
                with c_save:
                    save_topic = st.form_submit_button(
                        "💾 Save Topic",
                        key="topic_save_submit",
                        use_container_width=True,
                    )
                with c_cancel:
                    cancel_topic = st.form_submit_button(
                        "↩️ Cancel",
                        key="topic_cancel_submit",
                        use_container_width=True,
                    )

            if save_topic:
                save_topic_from_inline_editor()
                st.rerun()
            elif cancel_topic:
                _cancel_topic_edit()
                st.rerun()

        if display_speakers:
            for aid in display_speakers:
                stored_name = next(
                    (
                        m.get("display_name")
                        for m in st.session_state.messages
                        if m.get("agent_id") == aid and m.get("display_name")
                    ),
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

        render_discussion_messages(available_agents)


def render_telemetry_section(available_agents: Dict[str, str]) -> None:
    with st.container(key="telemetry_panel"):
        st.markdown(
            "<div class='exhum-telemetry-hero'>"
            "<div class='exhum-telemetry-title'>Telemetry</div>"
            "<p class='exhum-telemetry-subtitle'>Live app metrics.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        render_telemetry_panel(
            messages=st.session_state.messages,
            selected_agents=st.session_state.selected_agents,
            available_agents=available_agents,
            key_prefix="exhum_telemetry",
            fetch_live=True,
        )


@st.fragment
def render_discussion_messages(available_agents: Dict[str, str]) -> None:
    with st.container(border=False):
        if not st.session_state.messages:
            st.markdown(
                "<div class='exhum-empty'><h3>🎬 Ready to start</h3>"
                "<p>Use 🪏 Select Speaker and Press ▶️ Start Debate</p></div>",
                unsafe_allow_html=True,
            )
            return

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
            turn_chip_label = f"Turn {turn} | {ts}" if ts else f"Turn {turn}"
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
                    "</div>"
                    f"<span class='exhum-turn-chip'>{turn_chip_label}</span>"
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
        "debate_entropy": None,
        "estimated_tokens": 0,
        "session_burn_usd": 0.0,
        "target_entropy": 0.7,
        "current_agent_index": 0,
        "current_turn_number": 1,
        "thinking_message_id": "",
        "thinking_visible": False,
        "agents_backend_url": "",
        "agents_payload_cache": None,
        "close_sidebar_after_start": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "topic_edit_buffer" not in st.session_state:
        st.session_state.topic_edit_buffer = st.session_state.topic_input
    if "round_temperature" not in st.session_state:
        st.session_state.round_temperature = st.session_state.target_entropy


init_session_state()

if st.session_state.close_sidebar_after_start:
    close_sidebar_after_mobile_start()
else:
    ensure_sidebar_open_on_load()


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

@st.dialog(" ", width="large", on_dismiss="ignore")
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
                "<span class='exhum-temperature-caption'>Adjust between rigid logic and creative unpredictability.</span>",
                unsafe_allow_html=True,
            )
            render_entropy_slider_control()

        render_sidebar_heading("Commands")

        has_existing_debate = bool(
            st.session_state.discussion_started or st.session_state.messages
        )
        start_button_label = "▶️ Advance Debate" if has_existing_debate else "▶️ Start Debate"
        start = st.button(start_button_label, key="start_button", use_container_width=True)
        stop = st.button("⏸️ Halt Debate", key="pause_button", use_container_width=True)
        stop_feedback = st.empty()
        clear = st.button("🧹 Wipe Debate", key="clear_button", use_container_width=True)
        clear_feedback = st.empty()

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
                st.session_state.close_sidebar_after_start = True
                if not st.session_state.speaker_progress:
                    st.session_state.speaker_progress = {aid: 0.0 for aid in st.session_state.selected_agents}

                round_finished = int(st.session_state.current_agent_index) >= len(st.session_state.selected_agents)
                fresh_start = not st.session_state.messages and int(st.session_state.turn_count) == 0

                if fresh_start or round_finished:
                    st.session_state.current_agent_index = 0
                    st.session_state.current_turn_number = int(st.session_state.turn_count) + 1
                    st.session_state.thinking_message_id = ""
                    st.session_state.thinking_visible = False

                st.rerun()

        if stop:
            st.session_state.discussion_active = False
            stop_feedback.info("Round paused.")

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
                clear_feedback.success("Debate cleared.")
            else:
                clear_feedback.warning("Debate cleared locally, but backend cleanup failed.")

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


# ============================================================================
# MAIN AREA
# ============================================================================

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

col_chat, col_panel = st.columns([3.2, 1], gap="large")
with col_chat:
    render_discussion_panel(
        available_agents=available_agents,
        legend_map=legend_map,
        display_speakers=display_speakers,
        agent_counts=agent_counts,
        speaker_progress_bars=speaker_progress_bars,
    )
with col_panel:
    render_telemetry_section(available_agents)


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
    else:
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
                telemetry = response.get("telemetry") if isinstance(response, dict) else None
                execution_metrics = response.get("execution_metrics") if isinstance(response, dict) else None
                target_message.update({
                    "agent_id": response.get("agent_id"),
                    "display_name": response.get("display_name", ""),
                    "message": response.get("message"),
                    "turn_number": response.get("turn_number"),
                    "created_at": response.get("created_at", datetime.utcnow().isoformat()),
                    "is_thinking": False,
                    "execution_metrics": execution_metrics if isinstance(execution_metrics, dict) else None,
                })
                st.session_state.turn_count += 1
                if isinstance(telemetry, dict):
                    entropy_value = telemetry.get("entropy")
                    if isinstance(entropy_value, (int, float)):
                        st.session_state.debate_entropy = max(0.0, min(1.0, float(entropy_value)))
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
