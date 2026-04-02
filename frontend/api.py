"""
EXHUMED – async API helpers for the FastAPI backend.
All HTTP calls live here; the rest of the app stays HTTP-free.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import httpx
import streamlit as st

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 120.0
DEFAULT_LOCAL_BACKEND_URL = "http://localhost:8000"


def _normalize_backend_url(raw_url: str) -> str:
    return raw_url.strip().rstrip("/")


def get_backend_url() -> str:
    secret_url = ""
    env_url = ""

    try:
        secret_url = str(st.secrets.get("BACKEND_URL", "")).strip()
    except Exception:
        secret_url = ""

    env_url = os.getenv("BACKEND_URL", "").strip()

    backend_url = secret_url or env_url
    if backend_url:
        return _normalize_backend_url(backend_url)

    # Keep local development convenient, but do not pretend this is valid in hosted envs.
    return DEFAULT_LOCAL_BACKEND_URL


BACKEND_URL = get_backend_url()


@st.cache_data(ttl=120, show_spinner=False)
def _probe_backend_cached(backend_url: str) -> Tuple[bool, str]:
    try:
        with httpx.Client() as client:
            response = client.get(f"{backend_url}/", timeout=10)
            response.raise_for_status()
        return True, ""
    except Exception as exc:
        logger.error("Backend probe failed for %s: %s", backend_url, exc)
        if backend_url == DEFAULT_LOCAL_BACKEND_URL:
            return (
                False,
                "Backend unreachable at http://localhost:8000. Start the FastAPI backend locally, "
                "or set BACKEND_URL to your Railway public URL.",
            )
        return False, (
            f"Backend unreachable at {backend_url}. Check that the configured Railway public URL is correct and live."
        )


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_agents_from_backend_cached(backend_url: str) -> Dict[str, Any]:
    try:
        with httpx.Client() as client:
            response = client.get(f"{backend_url}/agents", timeout=10)
            response.raise_for_status()
            return response.json()
    except Exception as exc:
        logger.error("Error fetching agents: %s", exc)
        if backend_url == DEFAULT_LOCAL_BACKEND_URL:
            message = (
                "Backend unreachable at http://localhost:8000. Start the FastAPI backend locally, "
                "or set BACKEND_URL to your Railway public URL."
            )
        else:
            message = f"Could not reach backend at {backend_url}."
        return {
            "agents": [],
            "_error": message,
        }


async def probe_backend() -> Tuple[bool, str]:
    return _probe_backend_cached(BACKEND_URL)


@st.cache_data(ttl=45, show_spinner=False)
def _fetch_services_status_cached(backend_url: str) -> Dict[str, Any]:
    try:
        with httpx.Client() as client:
            response = client.get(f"{backend_url}/services-status", timeout=20)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {"status": "DEGRADED", "services": []}
    except Exception as exc:
        logger.warning("Error fetching service status: %s", exc)
        return {
            "status": "DEGRADED",
            "services": [
                {
                    "name": "Redis",
                    "status": "OFFLINE",
                    "latency_ms": None,
                    "detail": "Status check unavailable",
                },
                {
                    "name": "Vector",
                    "status": "OFFLINE",
                    "latency_ms": None,
                    "detail": "Status check unavailable",
                },
                {
                    "name": "Inference",
                    "status": "OFFLINE",
                    "latency_ms": None,
                    "detail": "Status check unavailable",
                },
            ],
        }


async def fetch_services_status() -> Dict[str, Any]:
    return _fetch_services_status_cached(BACKEND_URL)


@st.cache_data(ttl=5, show_spinner=False)
def _fetch_latest_telemetry_cached(backend_url: str) -> Dict[str, Any]:
    try:
        with httpx.Client() as client:
            response = client.get(f"{backend_url}/telemetry/latest", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {"status": "idle", "metrics": None}
    except Exception as exc:
        logger.warning("Error fetching latest telemetry: %s", exc)
        return {"status": "idle", "metrics": None}


async def fetch_latest_telemetry() -> Dict[str, Any]:
    return _fetch_latest_telemetry_cached(BACKEND_URL)


async def fetch_agents_from_backend() -> Dict[str, List[Dict[str, str]]]:
    return _fetch_agents_from_backend_cached(BACKEND_URL)


async def fetch_session_topic(session_id: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/sessions/{session_id}/topic", timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return str(data.get("topic", "")).strip()
    except Exception:
        return ""


async def push_session_topic(session_id: str, topic: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/sessions/{session_id}/topic",
                json={"topic": topic},
                timeout=10,
            )
            response.raise_for_status()
            return True
    except Exception as exc:
        logger.warning("Failed to push topic to backend: %s", exc)
        return False


async def clear_session(session_id: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{BACKEND_URL}/sessions/{session_id}",
                timeout=10,
            )
            response.raise_for_status()
            return True
    except Exception as exc:
        logger.warning("Failed to clear session %s on backend: %s", session_id, exc)
        return False


async def process_agent_turn(
    session_id: str,
    topic: str,
    agent_id: str,
    temperature: float = 0.7,
    turn_number: Optional[int] = None,
) -> Optional[dict]:
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "session_id": session_id,
                "topic": topic,
                "agent_id": agent_id,
                "temperature": temperature,
            }
            if turn_number is not None:
                payload["turn_number"] = turn_number
            response = await client.post(
                f"{BACKEND_URL}/process-turn",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        st.error(f"Timeout for {agent_id}. Try again.")
        return None
    except httpx.HTTPError as exc:
        detail = "Unknown error"
        try:
            detail = exc.response.json().get("detail", detail)
        except Exception:
            pass
        st.error(f"Error for {agent_id}: {detail}")
        return None
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        return None


async def download_pdf_export(session_id: str) -> Optional[bytes]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_URL}/export-pdf/{session_id}", timeout=30
            )
            response.raise_for_status()
            return response.content
    except Exception as exc:
        st.error(f"Error downloading PDF: {exc}")
        return None
