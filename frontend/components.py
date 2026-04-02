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

import pandas as pd
import streamlit as st

import api

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = Path(__file__).resolve().parent
LEGENDS_REGISTRY_PATH = FRONTEND_DIR / "agents_registry.json"
LOGO_PATH = BASE_DIR / "static" / "logo.png"
ACCENT_COLORS = ["#ff6b00", "#1f2937", "#0ea5a4", "#2563eb", "#16a34a"]


def build_hidden_index_table(rows: List[Dict[str, str]]) -> pd.DataFrame:
    table = pd.DataFrame(rows)
    table.index = [""] * len(table.index)
    return table


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


def render_drafted_chips_component(
    selected_agents: List[str], available_agents: Dict[str, str]
) -> None:
    with st.container(key="drafted_council_chips"):
        for index in range(0, len(selected_agents), 2):
            batch = selected_agents[index : index + 2]
            columns = st.columns(2)
            for col, aid in zip(columns, batch):
                legend_name = available_agents.get(aid, aid)
                with col:
                    st.button(
                        f"{legend_name}  x",
                        key=f"remove_drafted_{aid}",
                        help=f"Remove {legend_name} from the drafted council",
                        use_container_width=True,
                        on_click=remove_legend_selection,
                        args=(aid,),
                    )


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
    key_prefix: str = "exhum_telemetry",
    fetch_live: bool = False,
) -> None:
    mode_slug = key_prefix
    has_session_activity = bool(messages)
    latest_telemetry_snapshot: Dict[str, Any] = {"status": "idle", "metrics": None}
    if fetch_live and has_session_activity:
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
    if fetch_live:
        services_snapshot = asyncio.run(api.fetch_services_status())
    else:
        services_snapshot = {
            "status": "STANDBY",
            "services": [],
            "detail": "Live checks are paused to keep the UI responsive.",
        }
    st.session_state["services_status_snapshot"] = services_snapshot
    overall_status = str(services_snapshot.get("status", "STANDBY")).upper()
    overall_status_slug = overall_status.lower()
    service_rows = services_snapshot.get("services", [])
    online_services = sum(
        1 for service in service_rows if str(service.get("status", "")).upper() == "ONLINE"
    )
    service_count = len(service_rows)

    if session_metrics and session_telemetry_status == "ok":
        gen_time_value = session_metrics.get("generation_duration_ms")
        throughput_value = session_metrics.get("tokens_per_second")
        ttft_value = session_metrics.get("ttft_ms")
        neural_rows = [
            ("GEN TIME", f"{int(gen_time_value)}ms" if isinstance(gen_time_value, (int, float)) else "N/A"),
            ("THROUGHPUT", f"{float(throughput_value):.2f} TPS" if isinstance(throughput_value, (int, float)) else "N/A"),
            ("TTFT", f"{int(ttft_value)}ms" if isinstance(ttft_value, (int, float)) else "N/A"),
        ]
    else:
        neural_rows = [
            ("GEN TIME", "IDLE"),
            ("THROUGHPUT", "N/A"),
            ("TTFT", "N/A"),
        ]
    with st.container(key=f"{mode_slug}_panel"):
        with st.container(key=f"{mode_slug}_system_status_card"):
            with st.container(key=f"{mode_slug}_system_status_header"):
                st.markdown(
                    "<div class='exhum-telemetry-section-heading exhum-telemetry-section-heading-compact'>"
                    "<span class='exhum-telemetry-section-kicker'>Services</span>"
                    f"<span class='exhum-telemetry-section-title'><span class='exhum-telemetry-status-dot exhum-telemetry-status-dot-{overall_status_slug}' aria-hidden='true'></span>System Status</span>"
                    "</div>",
                    unsafe_allow_html=True,
                )

            with st.expander(f"Services ({online_services}/{service_count or 0})", expanded=False):
                if not service_rows:
                    st.info("Open services to run live checks.")
                else:
                    service_table_rows: List[Dict[str, str]] = []
                    service_notes: List[str] = []
                    for service in service_rows:
                        service_name = str(service.get("name", "Unknown Service"))
                        service_status = str(service.get("status", "OFFLINE")).upper()
                        latency_ms = service.get("latency_ms")
                        latency_label = (
                            f"{int(latency_ms)} ms"
                            if isinstance(latency_ms, (int, float))
                            else "--"
                        )
                        detail = str(service.get("detail", "") or "").strip()
                        service_table_rows.append(
                            {
                                "Service": service_name,
                                "Net RTT": latency_label,
                            }
                        )
                        if detail and service_status != "ONLINE":
                            service_notes.append(f"{service_name}: {detail}")

                    st.table(build_hidden_index_table(service_table_rows))
                    for note in service_notes:
                        st.caption(note)

        st.markdown(
            "<div class='exhum-telemetry-section-heading'>"
            "<span class='exhum-telemetry-section-kicker'>Inference</span>"
            "<span class='exhum-telemetry-section-title'>Neural Processing</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        with st.container(key=f"{mode_slug}_neural_block"):
            st.table(
                build_hidden_index_table(
                    [
                        {
                            "Metric": label,
                            "Value": value,
                        }
                        for label, value in neural_rows
                    ]
                )
            )

        st.markdown(
            "<div class='exhum-telemetry-section-heading'>"
            "<span class='exhum-telemetry-section-kicker'>Capacity</span>"
            "<span class='exhum-telemetry-section-title'>Context Saturation</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        with st.container(key=f"{mode_slug}_context_block"):
            st.progress(min(max(t["context_pct"] / 100.0, 0.0), 1.0))
            st.table(
                build_hidden_index_table(
                    [
                        {"Metric": "Prompt", "Value": str(t["prompt_tokens"])} ,
                        {"Metric": "Completion", "Value": str(t["completion_tokens"])} ,
                        {"Metric": "Total", "Value": f"{t['total_context_tokens']} / 8192"},
                    ]
                )
            )

        st.markdown(
            "<div class='exhum-telemetry-section-heading'>"
            "<span class='exhum-telemetry-section-kicker'>Spend</span>"
            "<span class='exhum-telemetry-section-title'>Session Cost</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        with st.container(key=f"{mode_slug}_cost_block"):
            st.markdown(
                "<div class='exhum-telemetry-cost-card'>"
                "<div class='exhum-telemetry-cost-topline'>"
                "<span class='exhum-telemetry-cost-kicker'>Estimated Burn</span>"
                "<span class='exhum-telemetry-cost-unit'>USD</span>"
                "</div>"
                f"<div class='exhum-telemetry-cost-value'>${t['burn_usd']:.6f}</div>"
                "<div class='exhum-telemetry-cost-caption'>Session-level spend estimate based on generated token volume.</div>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='exhum-telemetry-section-heading'>"
            "<span class='exhum-telemetry-section-kicker'>Behavior</span>"
            "<span class='exhum-telemetry-section-title'>Semantic Diversity</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        current_entropy = float(t["entropy"])
        target_entropy = float(st.session_state.target_entropy)
        entropy_scale_max = 1.5
        current_ratio = max(0.0, min(1.0, current_entropy / entropy_scale_max))
        target_ratio = max(0.0, min(1.0, target_entropy / entropy_scale_max))
        similarity_ratio = max(0.0, 1.0 - abs(current_entropy - target_entropy) / entropy_scale_max)
        similarity_label = "Aligned"
        if similarity_ratio < 0.85:
            similarity_label = "Tracking"
        if similarity_ratio < 0.6:
            similarity_label = "Off Target"

        with st.container(key=f"{mode_slug}_entropy_block"):
            st.markdown(
                "<div class='exhum-telemetry-entropy-card'>"
                "<div class='exhum-telemetry-entropy-topline'>"
                "<span class='exhum-telemetry-entropy-kicker'>Entropy Match</span>"
                f"<span class='exhum-telemetry-entropy-status'>{similarity_label}</span>"
                "</div>"
                "<div class='exhum-telemetry-entropy-values'>"
                f"<div class='exhum-telemetry-entropy-value-block'><span class='exhum-telemetry-entropy-value-label'>Current</span><span class='exhum-telemetry-entropy-value'>{current_entropy:.2f}</span></div>"
                f"<div class='exhum-telemetry-entropy-value-block'><span class='exhum-telemetry-entropy-value-label'>Target</span><span class='exhum-telemetry-entropy-value'>{target_entropy:.2f}</span></div>"
                "</div>"
                "<div class='exhum-telemetry-entropy-progress'>"
                "<div class='exhum-telemetry-entropy-progress-labels'>"
                "<span>Similarity</span>"
                f"<span>{similarity_ratio * 100:.0f}%</span>"
                "</div>"
                "<div class='exhum-telemetry-entropy-track'>"
                f"<div class='exhum-telemetry-entropy-fill' style='width:{similarity_ratio * 100:.1f}%'></div>"
                f"<div class='exhum-telemetry-entropy-target-marker' style='left:{target_ratio * 100:.1f}%'></div>"
                f"<div class='exhum-telemetry-entropy-current-marker' style='left:{current_ratio * 100:.1f}%'></div>"
                "</div>"
                "<div class='exhum-telemetry-entropy-caption'>Target marker shows requested diversity. Current marker shows live semantic spread.</div>"
                "</div>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='exhum-telemetry-section-heading'>"
            "<span class='exhum-telemetry-section-kicker'>Participation</span>"
            "<span class='exhum-telemetry-section-title'>Vocal Share</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        with st.container(key=f"{mode_slug}_airtime_block"):
            if not t["airtime_rows"]:
                st.info("No air-time data yet.")
            else:
                st.table(
                    build_hidden_index_table(
                        [
                            {
                                "Speaker": str(row["label"]),
                                "Words": str(int(row["words"])),
                                "Share": f"{max(0.0, float(row['pct'])):.0f}%",
                            }
                            for row in t["airtime_rows"]
                        ]
                    )
                )


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

# ── Entropy slider ───────────────────────────────────────────────────────────

def render_entropy_slider_control() -> None:
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.5,
        step=0.05,
        key="target_entropy",
        label_visibility="collapsed",
    )
