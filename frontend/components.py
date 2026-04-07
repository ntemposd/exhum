"""
EXHUMED – reusable UI helpers and data utilities.
Pure functions + Streamlit widgets; no page-level layout here.
"""

import asyncio
import base64
import html
import json
import logging
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
SESSION_COST_HELPER_TEXT = "Spend estimate based on token volume."
LLAMA_31_8B_INSTANT_INPUT_USD_PER_MILLION = 0.05
LLAMA_31_8B_INSTANT_OUTPUT_USD_PER_MILLION = 0.08


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
                        legend_name,
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
    metrics_history: List[Dict[str, Any]] = []
    request_rows: List[Dict[str, Any]] = []
    for msg in messages:
        words = len(str(msg.get("message", "")).split())
        total_words += words
        aid = str(msg.get("agent_id", ""))
        agent_words[aid] = agent_words.get(aid, 0) + words
        execution_metrics = msg.get("execution_metrics")
        if isinstance(execution_metrics, dict):
            metrics_history.append(execution_metrics)
            prompt_value = int(execution_metrics.get("prompt_tokens") or 0)
            completion_value = int(execution_metrics.get("completion_tokens") or 0)
            total_value = int(
                (prompt_value + completion_value)
                or execution_metrics.get("total_tokens")
                or 0
            )
            turn_number = msg.get("turn_number")
            row_turn = int(turn_number) if isinstance(turn_number, int) else (len(request_rows) + 1)
            request_rows.append(
                {
                    "request": f"T{row_turn:02d}",
                    "prompt": prompt_value,
                    "completion": completion_value,
                    "total": total_value,
                }
            )

    estimated_tokens = int(total_words / 0.75) if total_words else 0
    context_limit = 8192
    prompt_tokens = sum(int(item.get("prompt_tokens") or 0) for item in metrics_history)
    completion_tokens = sum(int(item.get("completion_tokens") or 0) for item in metrics_history)
    total_tokens = sum(
        int(item.get("total_tokens") or ((item.get("prompt_tokens") or 0) + (item.get("completion_tokens") or 0)) or 0)
        for item in metrics_history
    )

    request_prompt_tokens = 0
    request_completion_tokens = 0
    request_total_tokens = estimated_tokens
    if latest_metrics:
        request_prompt_tokens = int(latest_metrics.get("prompt_tokens") or 0)
        request_completion_tokens = int(latest_metrics.get("completion_tokens") or 0)
        request_total_tokens = int(
            (request_prompt_tokens + request_completion_tokens)
            or latest_metrics.get("total_tokens")
            or estimated_tokens
        )

    if not metrics_history and latest_metrics:
        prompt_tokens = int(latest_metrics.get("prompt_tokens") or 0)
        completion_tokens = int(latest_metrics.get("completion_tokens") or 0)
        total_tokens = int(
            latest_metrics.get("total_tokens")
            or (prompt_tokens + completion_tokens)
            or estimated_tokens
        )
        request_rows.append(
            {
                "request": "T01",
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": total_tokens,
            }
        )

    aggregate_total_tokens = total_tokens or estimated_tokens
    request_context_pct = (
        (request_total_tokens / context_limit) * 100.0
        if request_total_tokens
        else 0.0
    )
    token_usage_caption = (
        "Each row is one model request. Window is measured per request against the 8k context limit."
        if request_rows
        else "No request metrics yet."
    )
    input_cost_per_token = LLAMA_31_8B_INSTANT_INPUT_USD_PER_MILLION / 1_000_000.0
    output_cost_per_token = LLAMA_31_8B_INSTANT_OUTPUT_USD_PER_MILLION / 1_000_000.0

    if prompt_tokens or completion_tokens:
        burn_usd = (
            prompt_tokens * input_cost_per_token
            + completion_tokens * output_cost_per_token
        )
    else:
        # When prompt/completion telemetry is unavailable, use a blended rate across total estimated tokens.
        blended_cost_per_token = (
            (LLAMA_31_8B_INSTANT_INPUT_USD_PER_MILLION + LLAMA_31_8B_INSTANT_OUTPUT_USD_PER_MILLION)
            / 2.0
            / 1_000_000.0
        )
        burn_usd = aggregate_total_tokens * blended_cost_per_token

    generation_samples = [
        int(item.get("generation_duration_ms"))
        for item in metrics_history
        if isinstance(item.get("generation_duration_ms"), (int, float))
    ]
    queue_samples = [
        int(item.get("queue_time_ms"))
        for item in metrics_history
        if isinstance(item.get("queue_time_ms"), (int, float))
    ]
    prompt_time_samples = [
        int(item.get("prompt_time_ms"))
        for item in metrics_history
        if isinstance(item.get("prompt_time_ms"), (int, float))
    ]
    ttft_samples = [
        int(item.get("ttft_ms"))
        for item in metrics_history
        if isinstance(item.get("ttft_ms"), (int, float))
    ]

    avg_generation_ms = (
        sum(generation_samples) / len(generation_samples)
        if generation_samples
        else None
    )
    avg_queue_ms = sum(queue_samples) / len(queue_samples) if queue_samples else None
    avg_prompt_ms = sum(prompt_time_samples) / len(prompt_time_samples) if prompt_time_samples else None
    avg_ttft_ms = sum(ttft_samples) / len(ttft_samples) if ttft_samples else None
    total_generation_ms = sum(generation_samples)
    session_tps = (
        completion_tokens / (total_generation_ms / 1000.0)
        if completion_tokens and total_generation_ms > 0
        else None
    )

    st.session_state.estimated_tokens = estimated_tokens
    st.session_state.session_burn_usd = burn_usd

    display_agents = list(selected_agents)
    for aid in agent_words:
        if aid and aid not in display_agents:
            display_agents.append(aid)

    airtime_rows = sorted(
        [
            {
                "label": available_agents.get(aid, aid) or aid,
                "words": agent_words.get(aid, 0),
                "pct": (agent_words.get(aid, 0) / total_words * 100.0) if total_words else 0.0,
            }
            for aid in display_agents
        ],
        key=lambda r: r["words"],
        reverse=True,
    )

    return {
        "latency_ms": float(st.session_state.last_inference_latency_ms),
        "estimated_tokens": estimated_tokens,
        "perf_turns": len(metrics_history),
        "avg_generation_ms": avg_generation_ms,
        "session_tps": session_tps,
        "avg_queue_ms": avg_queue_ms,
        "avg_prompt_ms": avg_prompt_ms,
        "avg_ttft_ms": avg_ttft_ms,
        "request_prompt_tokens": request_prompt_tokens,
        "request_completion_tokens": request_completion_tokens,
        "request_total_tokens": request_total_tokens,
        "request_count": len(request_rows),
        "request_rows": request_rows,
        "context_limit": context_limit,
        "request_context_pct": request_context_pct,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": aggregate_total_tokens,
        "token_usage_caption": token_usage_caption,
        "burn_usd": burn_usd,
        "entropy": (
            float(st.session_state.debate_entropy)
            if isinstance(st.session_state.debate_entropy, (int, float))
            else None
        ),
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

    if t["perf_turns"] > 0:
        gen_time_value = t.get("avg_generation_ms")
        throughput_value = t.get("session_tps")
        queue_time_value = t.get("avg_queue_ms")
        prompt_time_value = t.get("avg_prompt_ms")
        ttft_value = t.get("avg_ttft_ms")
        neural_rows = [
            ("GEN TIME (AVG)", f"{int(round(gen_time_value))}ms" if isinstance(gen_time_value, (int, float)) else "N/A"),
            ("QUEUE (AVG)", f"{int(round(queue_time_value))}ms" if isinstance(queue_time_value, (int, float)) else "N/A"),
            ("PROMPT (AVG)", f"{int(round(prompt_time_value))}ms" if isinstance(prompt_time_value, (int, float)) else "N/A"),
            ("TTF (AVG)", f"{int(round(ttft_value))}ms" if isinstance(ttft_value, (int, float)) else "N/A"),
            ("SESSION TPS", f"{float(throughput_value):.2f} TPS" if isinstance(throughput_value, (int, float)) else "N/A"),
        ]
    else:
        neural_rows = [
            ("GEN TIME (AVG)", "IDLE"),
            ("QUEUE (AVG)", "N/A"),
            ("PROMPT (AVG)", "N/A"),
            ("TTF (AVG)", "N/A"),
            ("SESSION TPS", "N/A"),
        ]
    with st.container(key=f"{mode_slug}_panel"):
        with st.container(key=f"{mode_slug}_system_status_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
                f"<span class='exhum-telemetry-section-title'><span class='exhum-telemetry-status-dot exhum-telemetry-status-dot-{overall_status_slug}' aria-hidden='true'></span>System Status</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            with st.container(key=f"{mode_slug}_system_status_card"):
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

        with st.container(key=f"{mode_slug}_neural_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
                "<span class='exhum-telemetry-section-title'>Model Performance</span>"
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

        with st.container(key=f"{mode_slug}_context_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
                "<span class='exhum-telemetry-section-title'>Token Usage</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            with st.container(key=f"{mode_slug}_context_block"):
                with st.container(key=f"{mode_slug}_context_shell", border=True):
                    request_count = int(t["request_count"])
                    request_label = "Request" if request_count == 1 else "Requests"
                    st.markdown(
                        "<div class='exhum-telemetry-token-header'>"
                        "<div class='exhum-telemetry-context-topline'>"
                        f"<div class='exhum-telemetry-context-value'>{t['total_tokens']} Tokens</div>"
                        f"<span class='exhum-telemetry-context-pct'>{request_count} {request_label}</span>"
                        "</div>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                    token_rows = [
                        {
                            "Turn": str(row["request"]),
                            "Prompt": str(int(row["prompt"])),
                            "Comp": str(int(row["completion"])),
                            "Total": str(int(row["total"])),
                        }
                        for row in t["request_rows"]
                    ]
                    token_rows.append(
                        {
                            "Turn": "Total",
                            "Prompt": str(int(t["prompt_tokens"])),
                            "Comp": str(int(t["completion_tokens"])),
                            "Total": str(int(t["total_tokens"])),
                        }
                    )
                    st.table(build_hidden_index_table(token_rows))
                    st.markdown(
                        "<div class='exhum-telemetry-token-note exhum-telemetry-cost-caption'>Each turn is one model request.</div>",
                        unsafe_allow_html=True,
                    )

        with st.container(key=f"{mode_slug}_cost_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
                "<span class='exhum-telemetry-section-title'>Session Cost</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            with st.container(key=f"{mode_slug}_cost_block"):
                st.markdown(
                    "<div class='exhum-telemetry-cost-card'>"
                    f"<div class='exhum-telemetry-cost-value'>${t['burn_usd']:.6f}</div>"
                    f"<div class='exhum-telemetry-cost-caption'>{SESSION_COST_HELPER_TEXT}</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )

        with st.container(key=f"{mode_slug}_entropy_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
                "<span class='exhum-telemetry-section-title'>Debate Diversity</span>"
                "</div>",
                unsafe_allow_html=True,
            )
            entropy_value = t.get("entropy")
            current_entropy = float(entropy_value) if isinstance(entropy_value, (int, float)) else None
            observed_ratio = max(0.0, min(1.0, current_entropy)) if current_entropy is not None else 0.0
            spread_label = "No Data"
            left_value_label = "0.00"
            if current_entropy is not None:
                left_value_label = f"{observed_ratio * 100:.0f}%"
                spread_label = "High Spread"
                if current_entropy < 0.7:
                    spread_label = "Moderate"
                if current_entropy < 0.35:
                    spread_label = "Low Spread"

            with st.container(key=f"{mode_slug}_entropy_block"):
                st.markdown(
                    "<div class='exhum-telemetry-entropy-card'>"
                    "<div class='exhum-telemetry-entropy-topline'>"
                    f"<span class='exhum-telemetry-entropy-value-inline'>{left_value_label}</span>"
                    f"<span class='exhum-telemetry-entropy-status'>{spread_label}</span>"
                    "</div>"
                    "<div class='exhum-telemetry-entropy-progress'>"
                    "<div class='exhum-telemetry-entropy-track'>"
                    f"<div class='exhum-telemetry-entropy-fill' style='width:{observed_ratio * 100:.1f}%'></div>"
                    "</div>"
                    "<div class='exhum-telemetry-entropy-caption'>Diversity calculated as average pairwise Jaccard entropy between a response and the immediately preceding one.</div>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )

        with st.container(key=f"{mode_slug}_airtime_section"):
            st.markdown(
                "<div class='exhum-telemetry-section-heading'>"
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
