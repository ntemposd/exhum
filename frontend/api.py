"""
Roundtable Legends – async API helpers for the FastAPI backend.
All HTTP calls live here; the rest of the app stays HTTP-free.
"""

import logging
import os
from typing import Dict, List, Optional

import httpx
import streamlit as st

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 120.0

try:
    BACKEND_URL = str(st.secrets["BACKEND_URL"])
except Exception:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


async def fetch_agents_from_backend() -> Dict[str, List[Dict[str, str]]]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/agents", timeout=10)
            response.raise_for_status()
            return response.json()
    except Exception as exc:
        logger.error("Error fetching agents: %s", exc)
        return {"agents": []}


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


async def process_agent_turn(
    session_id: str,
    topic: str,
    agent_id: str,
    temperature: float = 0.7,
) -> Optional[dict]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/process-turn",
                json={
                    "session_id": session_id,
                    "topic": topic,
                    "agent_id": agent_id,
                    "temperature": temperature,
                },
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
