"""
EXHUMED – reusable UI helpers and data utilities.
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
    if st.session_state.discussion_started or st.session_state.messages:
        st.session_state.topic_edit_mode = False
        st.warning(
            "Discussion theme is locked after the debate starts. "
            "Wipe the debate or start a new session to change it."
        )
        return
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
            f"<a class='exhum-drafted-chip' href='?remove_legend={remove_q}' target='_self'"
            f" aria-label='Remove {legend_name}'>"
            f"<span class='drafted-chip-label'>{legend_name}</span>"
            "<span class='drafted-chip-x'>✕</span>"
            "</a>"
        )
    return f"<div class='exhum-drafted-chip-wrap'>{''.join(chip_html)}</div>"


def render_drafted_chips_component(
    selected_agents: List[str], available_agents: Dict[str, str]
) -> None:
    with st.container(key="drafted_council_chips"):
        for index in range(0, len(selected_agents), 2):
            batch = selected_agents[index : index + 2]
            columns = st.columns(len(batch))
            for col, aid in zip(columns, batch):
                legend_name = available_agents.get(aid, aid)
                with col:
                    if st.button(
                        f"{legend_name}  x",
                        key=f"remove_drafted_{aid}",
                        help=f"Remove {legend_name} from the drafted council",
                        use_container_width=True,
                    ):
                        remove_legend_selection(aid)
                        st.rerun()


def build_telemetry_snapshot(
    messages: List[Dict[str, Any]],
    selected_agents: List[str],
    available_agents: Dict[str, str],
    latest_metrics: Optional[Dict[str, Any]] = None,
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
    prompt_tokens = 0
    completion_tokens = 0
    total_context_tokens = estimated_tokens
    if latest_metrics:
        prompt_tokens = int(latest_metrics.get("prompt_tokens") or 0)
        completion_tokens = int(latest_metrics.get("completion_tokens") or 0)
        total_context_tokens = int(
            latest_metrics.get("total_tokens")
            or (prompt_tokens + completion_tokens)
            or estimated_tokens
        )
    context_pct = min(100.0, (total_context_tokens / context_limit) * 100.0) if total_context_tokens else 0.0
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
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_context_tokens": total_context_tokens,
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
    mode_slug = mode_class.replace("-", "_")
    has_session_activity = bool(messages)
    latest_telemetry_snapshot: Dict[str, Any] = {"status": "idle", "metrics": None}
    if has_session_activity:
        latest_telemetry_snapshot = asyncio.run(api.fetch_latest_telemetry())
    latest_metrics = latest_telemetry_snapshot.get("metrics") if isinstance(latest_telemetry_snapshot, dict) else None
    latest_metrics = latest_metrics if isinstance(latest_metrics, dict) else None
    telemetry_status = (
        str(latest_telemetry_snapshot.get("status", "idle")).lower()
        if isinstance(latest_telemetry_snapshot, dict)
        else "idle"
    )
    session_metrics = latest_metrics if has_session_activity else None
    session_telemetry_status = telemetry_status if has_session_activity else "idle"
    t = build_telemetry_snapshot(messages, selected_agents, available_agents, session_metrics)
    services_snapshot = asyncio.run(api.fetch_services_status())
    st.session_state["services_status_snapshot"] = services_snapshot
    overall_status = html.escape(str(services_snapshot.get("status", "STANDBY")).upper())
    overall_status_slug = "".join(
        ch if ch.isalnum() else "-" for ch in overall_status.lower()
    ).strip("-") or "standby"
    service_rows = services_snapshot.get("services", [])

    services_html = ""
    for service in service_rows:
        service_name = html.escape(str(service.get("name", "Unknown Service")))
        service_status = html.escape(str(service.get("status", "OFFLINE")).upper())
        latency_ms = service.get("latency_ms")
        latency_label = f"{int(latency_ms)}ms" if isinstance(latency_ms, (int, float)) else "--"
        detail = str(service.get("detail", "") or "").strip()
        detail_html = (
            f"<div class='exhum-service-detail'>{html.escape(detail)}</div>"
            if detail and service_status != "ONLINE"
            else ""
        )
        status_class = (
            "exhum-service-online" if service_status == "ONLINE" else "exhum-service-offline"
        )
        services_html += (
            "<div class='exhum-service-row'>"
            f"<div class='exhum-service-main'><span class='exhum-service-name'>{service_name}</span>"
            f"<span class='exhum-service-pill {status_class}'>{service_status}</span></div>"
            f"<div class='exhum-service-latency'>NET RTT: {html.escape(latency_label)}</div>"
            f"{detail_html}"
            "</div>"
        )

    if not services_html:
        services_html = "<span class='exhum-telemetry-kicker'>OPEN SERVICES TO RUN LIVE CHECKS</span>"

    airtime_html = ""
    for row in t["airtime_rows"]:
        label = html.escape(str(row["label"]))
        words = int(row["words"])
        pct = max(2.0, float(row["pct"])) if words > 0 else 0.0
        airtime_html += (
            "<div class='exhum-air-row'>"
            f"<span class='exhum-air-label'>{label}</span>"
            "<div class='exhum-air-track'>"
            f"<div class='exhum-air-fill' style='width:{pct:.1f}%'></div>"
            "</div>"
            f"<span class='exhum-air-value'>{words} WDS</span>"
            "</div>"
        )
    if not airtime_html:
        airtime_html = "<span class='exhum-telemetry-kicker'>NO AIR-TIME DATA YET</span>"

    entropy_display = f"<div class='exhum-telemetry-value'>{t['entropy']:.2f}</div>"
    if st.session_state.target_entropy > 1.0:
        entropy_display += "<span class='exhum-critical-warning'>⚠️ CRITICAL INSTABILITY</span>"

    if session_metrics and session_telemetry_status == "ok":
        gen_time_value = session_metrics.get("generation_duration_ms")
        throughput_value = session_metrics.get("tokens_per_second")
        ttft_value = session_metrics.get("ttft_ms")
        neural_rows = [
            ("GEN TIME", f"{int(gen_time_value)}ms" if isinstance(gen_time_value, (int, float)) else "---"),
            ("THROUGHPUT", f"{float(throughput_value):.2f} TPS" if isinstance(throughput_value, (int, float)) else "---"),
            ("TTFT", f"{int(ttft_value)}ms" if isinstance(ttft_value, (int, float)) else "---"),
        ]
    else:
        neural_rows = [
            ("GEN TIME", "IDLE"),
            ("THROUGHPUT", "---"),
            ("TTFT", "---"),
        ]

    neural_html = "".join(
        (
            "<div class='exhum-neural-row'>"
            f"<span class='exhum-neural-label'>{html.escape(label)}</span>"
            f"<span class='exhum-neural-value'>{html.escape(value)}</span>"
            "</div>"
        )
        for label, value in neural_rows
    )

    context_fill_class = "exhum-ctx-fill-green"
    if t["context_pct"] >= 80.0:
        context_fill_class = "exhum-ctx-fill-red"
    elif t["context_pct"] >= 50.0:
        context_fill_class = "exhum-ctx-fill-yellow"

    remaining_html = (
        f"<div class='exhum-telemetry-shell {mode_class}'>"
        "<div class='exhum-telemetry-block'>"
        "<span class='exhum-telemetry-kicker'>Neural Processing</span>"
        f"{neural_html}"
        "</div>"
        "<div class='exhum-telemetry-block'>"
        "<span class='exhum-telemetry-kicker'>Context Saturation</span>"
        f"<div class='exhum-telemetry-value exhum-context-label'>PROMPT: {t['prompt_tokens']} | COMP: {t['completion_tokens']} | TOTAL: {t['total_context_tokens']} / 8192</div>"
        "<div class='exhum-ctx-track'>"
        f"<div class='exhum-ctx-fill {context_fill_class}' style='width:{t['context_pct']:.1f}%'></div>"
        "</div>"
        "</div>"
        "<div class='exhum-telemetry-block'>"
        "<span class='exhum-telemetry-kicker'>Session Cost</span>"
        f"<div class='exhum-telemetry-value'>&gt; COST: <span class='exhum-telemetry-emphasis'>${t['burn_usd']:.6f}</span></div>"
        "</div>"
        "<div class='exhum-telemetry-block'>"
        f"<span class='exhum-telemetry-kicker'>Semantic Diversity (Target: {float(st.session_state.target_entropy):.2f})</span>"
        + entropy_display
        + "</div>"
        "<div class='exhum-telemetry-block'>"
        "<span class='exhum-telemetry-kicker'>Vocal Share</span>"
        f"{airtime_html}"
        "</div>"
        "</div>"
    )
    with st.container(key=f"{mode_slug}_system_status_card"):
        st.markdown(
            (
                "<div class='exhum-system-status-shell'>"
                "<div class='exhum-system-status-summary'>"
                "<div class='exhum-system-status-left'>"
                "<span class='exhum-telemetry-dot'></span>"
                "<span class='exhum-system-status-label'>System Status</span>"
                "</div>"
                f"<span class='exhum-system-status-pill exhum-system-status-pill-{overall_status_slug}'>{overall_status}</span>"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        with st.container(key=f"{mode_slug}_services_toggle_row"):
            label_col, toggle_col = st.columns([0.72, 0.28], gap="small")
            with label_col:
                st.markdown(
                    "<div class='exhum-services-toggle-label'>SERVICES</div>",
                    unsafe_allow_html=True,
                )
            with toggle_col:
                show_services = st.toggle(
                    "Show Services",
                    key=f"{mode_slug}_services_toggle",
                    label_visibility="collapsed",
                )
        if show_services:
            st.markdown(services_html, unsafe_allow_html=True)
    st.markdown(remaining_html, unsafe_allow_html=True)


def render_speaker_card_html(
    name: str,
    avatar_url: str,
    accent: str,
    turns: int,
    progress: float,
    progress_text: str,
    archetype: str = "",
    detail_href: str = "",
) -> str:
    progress_pct = max(0.0, min(100.0, progress * 100.0))
    safe_name = html.escape(name)
    safe_status = html.escape(progress_text.upper())
    safe_arch = html.escape(archetype) if archetype else ""
    turns_label = f"{turns} turn{'s' if turns != 1 else ''}"
    arch_html = f"<span class='exhum-speaker-archetype'>{safe_arch}</span>" if safe_arch else ""
    card_html = (
        f"<div class='exhum-speaker'>"
        f"<div class='exhum-avatar' style='background:{accent}22; color:{accent}; width:40px; height:40px; font-size:14px;'>"
        f"<img class='exhum-avatar-img' src='{avatar_url}' alt='{safe_name}' />"
        "</div>"
        "<div style='flex:1;min-width:0;display:flex;flex-direction:column;'>"
        f"<span style='font-size:0.95rem;font-weight:700;line-height:1.2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>{safe_name}</span>"
        f"{arch_html}"
        "</div>"
        "<div class='exhum-speaker-progress-wrap'>"
        "<div class='exhum-speaker-progress-track'>"
        f"<div class='exhum-speaker-progress-fill' style='width:{progress_pct:.1f}%;'></div>"
        "</div>"
        "<div class='exhum-speaker-progress-footer'>"
        f"<span class='exhum-speaker-progress-text'>{safe_status}</span>"
        f"<span class='exhum-speaker-count'>{turns_label}</span>"
        "</div>"
        "</div>"
        "</div>"
    )
    if detail_href:
        return f"<a class='exhum-speaker-link' href='{html.escape(detail_href, quote=True)}' target='_self'>{card_html}</a>"
    return card_html


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
