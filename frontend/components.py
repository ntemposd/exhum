"""
Roundtable Legends – reusable UI helpers and data utilities.
Pure functions + Streamlit widgets; no page-level layout here.
"""

import asyncio
import base64
import html
import json
import logging
import random
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import streamlit as st

import api

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = Path(__file__).resolve().parent
LEGENDS_REGISTRY_PATH = FRONTEND_DIR / "agents_registry.json"
LOGO_PATH = BASE_DIR / "static" / "logo.png"
ACCENT_COLORS = ["#ff6b00", "#1f2937", "#0ea5a4", "#2563eb", "#16a34a"]


# ── Data helpers ──────────────────────────────────────────────────────────────

def load_legends_registry(available_agents: Dict[str, str]) -> List[Dict[str, str]]:
    legends: List[Dict[str, str]] = []
    if LEGENDS_REGISTRY_PATH.exists():
        try:
            payload = json.loads(LEGENDS_REGISTRY_PATH.read_text(encoding="utf-8"))
            for item in payload:
                aid = str(item.get("agent_id", "")).strip()
                if not aid:
                    continue
                display = str(item.get("display_name") or available_agents.get(aid, aid))
                archetype = str(item.get("archetype", "Council Member"))
                legends.append({"agent_id": aid, "display_name": display, "archetype": archetype})
        except Exception as exc:
            logger.warning("Unable to load agents_registry.json: %s", exc)

    if not legends:
        for aid, name in sorted(available_agents.items()):
            legends.append({"agent_id": aid, "display_name": name, "archetype": "Council Member"})

    if available_agents:
        legends = [item for item in legends if item["agent_id"] in available_agents]
    return legends


def get_style_index(agent_id: str) -> int:
    try:
        return int(str(agent_id).split("_")[-1]) % 5
    except Exception:
        return abs(hash(agent_id)) % 5


def agent_initials(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()


@st.cache_data
def _load_avatar_b64s() -> Dict[str, str]:
    result: Dict[str, str] = {}
    avatars_dir = BASE_DIR / "static" / "avatars"
    if avatars_dir.exists():
        for png in avatars_dir.glob("*.png"):
            encoded = base64.b64encode(png.read_bytes()).decode()
            result[png.stem] = f"data:image/png;base64,{encoded}"
    return result


AVATAR_B64: Dict[str, str] = _load_avatar_b64s()


@st.cache_data
def get_logo_data_uri() -> Optional[str]:
    if not LOGO_PATH.exists():
        return None
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


def get_avatar_url(agent_id: str, display_name: str) -> str:
    if agent_id in AVATAR_B64:
        return AVATAR_B64[agent_id]
    seed = quote_plus(f"{agent_id}-{display_name}")
    return (
        "https://api.dicebear.com/9.x/notionists-neutral/svg"
        f"?seed={seed}&backgroundColor=f3f4f6,fff7ed,e9f1ff,e9fbfa"
    )


# ── Session-state mutators ────────────────────────────────────────────────────

def toggle_legend_selection(agent_id: str) -> None:
    if agent_id in st.session_state.selected_agents:
        st.session_state.selected_agents = [
            a for a in st.session_state.selected_agents if a != agent_id
        ]
    else:
        st.session_state.selected_agents = [*st.session_state.selected_agents, agent_id]


def remove_legend_selection(agent_id: str) -> None:
    st.session_state.selected_agents = [
        a for a in st.session_state.selected_agents if a != agent_id
    ]
    st.session_state.speaker_progress.pop(agent_id, None)
    if not st.session_state.selected_agents:
        st.session_state.discussion_active = False


def update_debate_entropy() -> None:
    swing = random.uniform(-0.08, 0.08)
    st.session_state.debate_entropy = max(
        0.0, min(1.0, st.session_state.debate_entropy + swing)
    )


def _cancel_topic_edit() -> None:
    st.session_state.topic_edit_mode = False


def _toggle_message_expansion(message_key: str) -> None:
    expanded = set(st.session_state.expanded_message_keys)
    if message_key in expanded:
        expanded.remove(message_key)
    else:
        expanded.add(message_key)
    st.session_state.expanded_message_keys = sorted(expanded)


def save_topic_from_inline_editor() -> None:
    new_topic = st.session_state.topic_edit_buffer.strip()
    if not new_topic:
        st.warning("Topic cannot be empty.")
        return
    st.session_state.topic_input = new_topic
    st.session_state.topic_edit_mode = False
    ok = asyncio.run(api.push_session_topic(st.session_state.session_id, new_topic))
    if ok:
        st.success("Topic updated.")
    else:
        st.warning("Topic updated locally; backend sync failed.")


# ── HTML component builders ───────────────────────────────────────────────────

def build_drafted_chips_component(
    selected_agents: List[str], available_agents: Dict[str, str]
) -> str:
    chip_html = []
    for aid in selected_agents:
        legend_name_raw = available_agents.get(aid, aid)
        legend_name = html.escape(legend_name_raw)
        remove_q = quote_plus(aid)
        chip_html.append(
            f"<a class='rtl-drafted-chip' href='?remove_legend={remove_q}'"
            f" aria-label='Remove {legend_name}'>"
            f"<span class='drafted-chip-label'>{legend_name}</span>"
            "<span class='drafted-chip-x'>✕</span>"
            "</a>"
        )
    return f"<div class='rtl-drafted-chip-wrap'>{''.join(chip_html)}</div>"


def build_telemetry_snapshot(
    messages: List[Dict[str, Any]],
    selected_agents: List[str],
    available_agents: Dict[str, str],
) -> Dict[str, Any]:
    agent_words: Dict[str, int] = {aid: 0 for aid in selected_agents}
    total_words = 0
    for msg in messages:
        words = len(str(msg.get("message", "")).split())
        total_words += words
        aid = str(msg.get("agent_id", ""))
        agent_words[aid] = agent_words.get(aid, 0) + words

    estimated_tokens = int(total_words / 0.75) if total_words else 0
    context_limit = 8192
    context_pct = min(100.0, (estimated_tokens / context_limit) * 100.0) if estimated_tokens else 0.0
    burn_usd = (estimated_tokens / 1000.0) * 0.0002

    st.session_state.estimated_tokens = estimated_tokens
    st.session_state.session_burn_usd = burn_usd

    display_agents = list(selected_agents)
    for aid in agent_words:
        if aid and aid not in display_agents:
            display_agents.append(aid)

    peak_words = max((agent_words.get(aid, 0) for aid in display_agents), default=0)
    airtime_rows = sorted(
        [
            {
                "label": available_agents.get(aid, aid) or aid,
                "words": agent_words.get(aid, 0),
                "pct": (agent_words.get(aid, 0) / peak_words * 100.0) if peak_words else 0.0,
            }
            for aid in display_agents
        ],
        key=lambda r: r["words"],
        reverse=True,
    )

    return {
        "latency_ms": float(st.session_state.last_inference_latency_ms),
        "estimated_tokens": estimated_tokens,
        "context_pct": context_pct,
        "burn_usd": burn_usd,
        "entropy": float(st.session_state.debate_entropy),
        "airtime_rows": airtime_rows,
    }


def render_telemetry_panel(
    messages: List[Dict[str, Any]],
    selected_agents: List[str],
    available_agents: Dict[str, str],
    mode_class: str,
) -> None:
    t = build_telemetry_snapshot(messages, selected_agents, available_agents)

    airtime_html = ""
    for row in t["airtime_rows"]:
        label = html.escape(str(row["label"]))
        words = int(row["words"])
        pct = max(2.0, float(row["pct"])) if words > 0 else 0.0
        airtime_html += (
            "<div class='rtl-air-row'>"
            f"<span class='rtl-air-label'>{label}</span>"
            "<div class='rtl-air-track'>"
            f"<div class='rtl-air-fill' style='width:{pct:.1f}%'></div>"
            "</div>"
            f"<span class='rtl-air-value'>{words}W</span>"
            "</div>"
        )
    if not airtime_html:
        airtime_html = "<span class='rtl-telemetry-kicker'>NO AIR-TIME DATA YET</span>"

    entropy_display = f"<div class='rtl-telemetry-value'>{t['entropy']:.2f}</div>"
    if st.session_state.target_entropy > 1.0:
        entropy_display += "<span class='rtl-critical-warning'>⚠️ CRITICAL INSTABILITY</span>"

    panel_html = (
        f"<div class='rtl-telemetry-shell {mode_class}'>"
        "<div class='rtl-telemetry-header'><span class='rtl-telemetry-dot'></span>SYSTEM STATUS: OPTIMAL</div>"
        "<div class='rtl-telemetry-block'>"
        "<span class='rtl-telemetry-kicker'>Inference Latency</span>"
        f"<div class='rtl-telemetry-value'>&gt; LATENCY: <span class='rtl-telemetry-emphasis'>{t['latency_ms']:.0f}ms</span></div>"
        "</div>"
        "<div class='rtl-telemetry-block'>"
        "<span class='rtl-telemetry-kicker'>Context Saturation</span>"
        f"<div class='rtl-telemetry-value'>{t['estimated_tokens']} / 8192 TOKENS</div>"
        "<div class='rtl-ctx-track'>"
        f"<div class='rtl-ctx-fill' style='width:{t['context_pct']:.1f}%'></div>"
        "</div>"
        "</div>"
        "<div class='rtl-telemetry-block'>"
        "<span class='rtl-telemetry-kicker'>Token Burn Rate</span>"
        f"<div class='rtl-telemetry-value'>&gt; BURN: <span class='rtl-telemetry-emphasis'>${t['burn_usd']:.6f}</span></div>"
        "</div>"
        "<div class='rtl-telemetry-block'>"
        f"<span class='rtl-telemetry-kicker'>Debate Entropy (Target: {float(st.session_state.target_entropy):.2f})</span>"
        + entropy_display
        + "</div>"
        "<div class='rtl-telemetry-block'>"
        "<span class='rtl-telemetry-kicker'>Agent Air-time</span>"
        f"{airtime_html}"
        "</div>"
        "</div>"
    )
    st.markdown(panel_html, unsafe_allow_html=True)


def render_speaker_card_html(
    name: str,
    avatar_url: str,
    accent: str,
    turns: int,
    progress: float,
    progress_text: str,
    archetype: str = "",
) -> str:
    progress_pct = max(0.0, min(100.0, progress * 100.0))
    safe_name = html.escape(name)
    safe_status = html.escape(progress_text.upper())
    safe_arch = html.escape(archetype) if archetype else ""
    turns_label = f"{turns} turn{'s' if turns != 1 else ''}"
    arch_html = f"<span class='rtl-speaker-archetype'>{safe_arch}</span>" if safe_arch else ""
    return (
        f"<div class='rtl-speaker'>"
        f"<div class='rtl-avatar' style='background:{accent}22; color:{accent}; width:40px; height:40px; font-size:14px;'>"
        f"<img class='rtl-avatar-img' src='{avatar_url}' alt='{safe_name}' />"
        "</div>"
        "<div style='flex:1;min-width:0;display:flex;flex-direction:column;'>"
        f"<span style='font-size:0.95rem;font-weight:700;line-height:1.2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>{safe_name}</span>"
        f"{arch_html}"
        "</div>"
        "<div class='rtl-speaker-progress-wrap'>"
        "<div class='rtl-speaker-progress-track'>"
        f"<div class='rtl-speaker-progress-fill' style='width:{progress_pct:.1f}%;'></div>"
        "</div>"
        "<div class='rtl-speaker-progress-footer'>"
        f"<span class='rtl-speaker-progress-text'>{safe_status}</span>"
        f"<span class='rtl-speaker-count'>{turns_label}</span>"
        "</div>"
        "</div>"
        "</div>"
    )


# ── Entropy slider (fragment-isolated) ───────────────────────────────────────

def _fragment_or_noop(func):
    fragment_api = getattr(st, "fragment", None)
    if callable(fragment_api):
        return fragment_api(func)
    return func


@_fragment_or_noop
def render_entropy_slider_control() -> None:
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.5,
        step=0.05,
        key="target_entropy",
        label_visibility="collapsed",
    )
