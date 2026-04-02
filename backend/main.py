"""
EXHUMED: FastAPI Backend
Decoupled AI discussion platform with dynamic agent registry.

Storage stack:
- Upstash Redis: agent registry and ordered session message index
- Upstash Vector: discussion message vectors for semantic retrieval
"""

import json
import logging
import os
import re
import string
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fpdf import FPDF
from pydantic import BaseModel, Field
from upstash_redis import Redis
from upstash_vector import Index

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

AGENT_REGISTRY_CACHE_TTL_SECONDS = 60.0
AGENT_CONFIG_CACHE_TTL_SECONDS = 300.0
_agent_registry_cache: Dict[str, Any] = {
    "expires_at": 0.0,
    "agents": [],
}
_agent_config_cache: Dict[str, Dict[str, Any]] = {}

FILE_DIR = Path(__file__).resolve().parent
REPO_ROOT_CANDIDATE = FILE_DIR.parent

# Support two deployment layouts:
# 1) repo-root deploy: /app/backend/main.py
# 2) backend-only deploy: /app/main.py
if (REPO_ROOT_CANDIDATE / "backend" / "main.py").exists():
    BASE_DIR = REPO_ROOT_CANDIDATE
else:
    BASE_DIR = FILE_DIR

STATIC_DIR = BASE_DIR / "static"

# Load environment variables from the local .env file when present.
load_dotenv(BASE_DIR / ".env")

# Upstash and model config
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
UPSTASH_VECTOR_REST_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID", "llama-3.1-8b-instant")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://api.groq.com/openai/v1")

missing_env: List[str] = []
for env_name in (
    "UPSTASH_REDIS_REST_URL",
    "UPSTASH_REDIS_REST_TOKEN",
    "UPSTASH_VECTOR_REST_URL",
    "UPSTASH_VECTOR_REST_TOKEN",
):
    if not os.getenv(env_name):
        missing_env.append(env_name)

if not LLM_API_KEY:
    missing_env.append("LLM_API_KEY")

if missing_env:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_env)}")

redis = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)
vector_index = Index(url=UPSTASH_VECTOR_REST_URL, token=UPSTASH_VECTOR_REST_TOKEN)

app = FastAPI(
    title="EXHUMED",
    version="1.1.0",
    description="Decoupled AI discussion platform with Upstash Redis + Vector",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    logger.warning("Static directory not found at %s; /static route disabled", STATIC_DIR)


class AgentConfig(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier")
    display_name: str = Field(..., description="Human-readable agent name")
    system_prompt: str = Field(..., description="System prompt for the LLM")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=512, ge=50, le=2048)


class ProcessTurnRequest(BaseModel):
    session_id: UUID = Field(..., description="Unique session identifier")
    topic: str = Field(..., min_length=1, max_length=255, description="Discussion topic")
    agent_id: str = Field(..., description="Agent to process turn for")
    turn_number: Optional[int] = Field(default=None, ge=1, description="Turn number if already known")


class ProcessTurnResponse(BaseModel):
    message_id: UUID
    agent_id: str
    display_name: str
    message: str
    turn_number: int
    created_at: datetime


class GenerateRequest(BaseModel):
    session_id: UUID = Field(..., description="Unique session identifier")
    topic: str = Field(..., min_length=1, max_length=255, description="Discussion topic")
    agent_id: str = Field(..., description="Agent to generate response for")
    previous_response: Optional[str] = Field(None, description="Previous agent's response for entropy calculation")


class TelemetryData(BaseModel):
    entropy: float = Field(..., description="Jaccard Similarity Entropy Score (0.0-1.0)")
    latency_ms: int = Field(..., description="Response generation latency in milliseconds")
    word_count: int = Field(..., description="Total word count in generated response")


class ExecutionMetrics(BaseModel):
    generation_duration_ms: Optional[int] = Field(None, description="Provider-reported generation duration in milliseconds")
    prompt_tokens: Optional[int] = Field(None, description="Prompt tokens consumed")
    completion_tokens: Optional[int] = Field(None, description="Completion tokens generated")
    total_tokens: Optional[int] = Field(None, description="Total tokens consumed")
    tokens_per_second: Optional[float] = Field(None, description="Completion throughput in tokens per second")
    ttft_ms: Optional[int] = Field(None, description="Time to first token in milliseconds, if available")
    network_rtt_ms: Optional[int] = Field(None, description="Observed network round-trip for the inference request")
    provider: str = Field(default="llm", description="Current inference provider label")
    updated_at: datetime = Field(..., description="Timestamp of the latest execution metrics")


class GenerateResponse(BaseModel):
    response: str = Field(..., description="Generated response text")
    telemetry: TelemetryData = Field(..., description="Telemetry metrics")
    message_id: Optional[UUID] = Field(None, description="Message ID if persisted")
    turn_number: Optional[int] = Field(None, description="Turn number if persisted")


class ServiceStatus(BaseModel):
    name: str = Field(..., description="Display name of the service")
    status: str = Field(..., description="ONLINE or OFFLINE")
    latency_ms: Optional[int] = Field(None, description="Observed latency in milliseconds")
    detail: Optional[str] = Field(None, description="Optional diagnostic detail")


def _clean_text(text: str) -> str:
    """Clean text for Jaccard Similarity: lowercase, remove punctuation, tokenize into words."""
    # Lowercase and remove punctuation
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    # Tokenize into set of unique words (no duplicates, no empty strings)
    words = set(word for word in text.split() if word.strip())
    return words


def calculate_jaccard_entropy(text1: str, text2: str) -> float:
    """
    Calculate Jaccard Similarity Entropy Index.
    
    Formula:
    - Jaccard Similarity = |Intersection| / |Union|
    - Entropy Score = 1 - Similarity (where 1 = maximum divergence, 0 = identical)
    
    Args:
        text1: First text (usually current response)
        text2: Second text (usually previous response)
    
    Returns:
        float: Entropy score in range [0.0, 1.0]
        - 0.0: Texts are identical (no entropy)
        - 1.0: Texts are completely different (maximum entropy)
    """
    if not text1 or not text2:
        # If either text is empty, return default entropy
        return 0.0 if (not text1 and not text2) else 1.0
    
    # Clean and convert to sets
    words_text1 = _clean_text(text1)
    words_text2 = _clean_text(text2)
    
    if not words_text1 or not words_text2:
        # If either set is empty after cleaning
        return 1.0 if (words_text1 != words_text2) else 0.0
    
    # Calculate Jaccard Similarity using set operations (optimized)
    intersection = len(words_text1 & words_text2)  # Set intersection
    union = len(words_text1 | words_text2)  # Set union
    
    if union == 0:
        jaccard_similarity = 0.0
    else:
        jaccard_similarity = intersection / union
    
    # Convert similarity to entropy: 1 - similarity
    entropy = 1.0 - jaccard_similarity
    
    return round(entropy, 4)





class SessionTopicUpdateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=255)


class AgentRegisterRequest(BaseModel):
    agent_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    system_prompt: str = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=512, ge=50, le=2048)


def _decode_redis_value(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def _parse_agent_payload(agent_id: str, payload: str) -> AgentConfig:
    raw = json.loads(payload)
    return AgentConfig(
        agent_id=agent_id,
        display_name=raw["display_name"],
        system_prompt=raw["system_prompt"],
        temperature=float(raw.get("temperature", 0.7)),
        max_tokens=int(raw.get("max_tokens", 512)),
    )


def invalidate_agent_registry_cache() -> None:
    _agent_registry_cache["expires_at"] = 0.0
    _agent_registry_cache["agents"] = []


def invalidate_agent_config_cache(agent_id: Optional[str] = None) -> None:
    if agent_id is None:
        _agent_config_cache.clear()
        return
    _agent_config_cache.pop(agent_id, None)


def get_cached_agent_registry() -> Optional[List[Dict[str, Any]]]:
    if time.monotonic() >= float(_agent_registry_cache["expires_at"]):
        return None
    cached_agents = _agent_registry_cache.get("agents", [])
    return [dict(agent) for agent in cached_agents]


def set_cached_agent_registry(agents: List[Dict[str, Any]]) -> None:
    _agent_registry_cache["agents"] = [dict(agent) for agent in agents]
    _agent_registry_cache["expires_at"] = time.monotonic() + AGENT_REGISTRY_CACHE_TTL_SECONDS


def get_cached_agent_config(agent_id: str) -> Optional[AgentConfig]:
    cached_item = _agent_config_cache.get(agent_id)
    if not cached_item:
        return None
    if time.monotonic() >= float(cached_item["expires_at"]):
        _agent_config_cache.pop(agent_id, None)
        return None
    cached_config = cached_item["agent_config"]
    if isinstance(cached_config, AgentConfig):
        return cached_config.model_copy(deep=True)
    return None


def set_cached_agent_config(agent_config: AgentConfig) -> None:
    _agent_config_cache[agent_config.agent_id] = {
        "expires_at": time.monotonic() + AGENT_CONFIG_CACHE_TTL_SECONDS,
        "agent_config": agent_config.model_copy(deep=True),
    }


def _load_message_record(raw_entry: Any) -> Optional[Dict[str, Any]]:
    decoded_entry = _decode_redis_value(raw_entry)

    try:
        item = json.loads(decoded_entry)
        if isinstance(item, dict) and "message" in item:
            return item
    except json.JSONDecodeError:
        pass

    try:
        payload = redis.get(f"message:{decoded_entry}")
        if not payload:
            return None
        item = json.loads(_decode_redis_value(payload))
        return item if isinstance(item, dict) else None
    except Exception:
        return None


def _extract_legacy_message_key(raw_entry: Any) -> Optional[str]:
    decoded_entry = _decode_redis_value(raw_entry)

    try:
        item = json.loads(decoded_entry)
        if isinstance(item, dict) and "message" in item:
            return None
    except json.JSONDecodeError:
        pass

    return f"message:{decoded_entry}" if decoded_entry else None


def _safe_int(value: Any) -> Optional[int]:
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_ttft_ms(headers: httpx.Headers) -> Optional[int]:
    candidate_keys = (
        "x-ttft-ms",
        "x-ttft",
        "ttft-ms",
        "openai-processing-ms",
        "x-openai-processing-ms",
    )
    for key in candidate_keys:
        value = headers.get(key)
        parsed = _safe_int(value)
        if parsed is not None:
            return parsed
    return None


def _extract_execution_metrics(
    data: Dict[str, Any],
    headers: httpx.Headers,
    network_rtt_ms: int,
) -> ExecutionMetrics:
    usage = data.get("usage") if isinstance(data, dict) else {}
    usage = usage if isinstance(usage, dict) else {}

    prompt_tokens = _safe_int(usage.get("prompt_tokens"))
    completion_tokens = _safe_int(usage.get("completion_tokens"))
    total_tokens = _safe_int(usage.get("total_tokens"))

    generation_duration_s = (
        _safe_float(usage.get("total_time"))
        or _safe_float(usage.get("completion_time"))
    )
    generation_duration_ms = (
        int(generation_duration_s * 1000) if generation_duration_s is not None else None
    )

    tokens_per_second: Optional[float] = None
    if completion_tokens and generation_duration_s and generation_duration_s > 0:
        tokens_per_second = round(completion_tokens / generation_duration_s, 2)

    return ExecutionMetrics(
        generation_duration_ms=generation_duration_ms,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        tokens_per_second=tokens_per_second,
        ttft_ms=_extract_ttft_ms(headers),
        network_rtt_ms=network_rtt_ms,
        provider="llm",
        updated_at=datetime.now(timezone.utc),
    )


def save_latest_execution_metrics(metrics: ExecutionMetrics) -> None:
    try:
        redis.set("telemetry:latest", metrics.model_dump_json())
    except Exception as exc:
        logger.warning("Unable to persist latest execution telemetry: %s", exc)


def fetch_latest_execution_metrics() -> Optional[ExecutionMetrics]:
    try:
        payload = redis.get("telemetry:latest")
        if not payload:
            return None
        raw = json.loads(_decode_redis_value(payload))
        if isinstance(raw, dict):
            return ExecutionMetrics.model_validate(raw)
    except Exception as exc:
        logger.warning("Unable to load latest execution telemetry: %s", exc)
    return None


async def check_services() -> Dict[str, Any]:
    services: List[ServiceStatus] = []

    redis_started = time.perf_counter()
    try:
        redis.ping()
        redis_latency_ms = int((time.perf_counter() - redis_started) * 1000)
        services.append(
            ServiceStatus(
                name="Redis",
                status="ONLINE",
                latency_ms=redis_latency_ms,
            )
        )
    except Exception as exc:
        logger.warning("Redis health check failed: %s", exc)
        services.append(
            ServiceStatus(
                name="Redis",
                status="OFFLINE",
                detail=str(exc)[:160],
            )
        )

    vector_started = time.perf_counter()
    try:
        vector_index.info()
        vector_latency_ms = int((time.perf_counter() - vector_started) * 1000)
        services.append(
            ServiceStatus(
                name="Vector",
                status="ONLINE",
                latency_ms=vector_latency_ms,
            )
        )
    except Exception as exc:
        logger.warning("Upstash Vector health check failed: %s", exc)
        services.append(
            ServiceStatus(
                name="Vector",
                status="OFFLINE",
                detail=str(exc)[:160],
            )
        )

    inference_started = time.perf_counter()
    try:
        headers = {"Authorization": f"Bearer {LLM_API_KEY}"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(f"{LLM_API_BASE_URL}/models", headers=headers)
            response.raise_for_status()
        inference_latency_ms = int((time.perf_counter() - inference_started) * 1000)
        services.append(
            ServiceStatus(
                name="Inference",
                status="ONLINE",
                latency_ms=inference_latency_ms,
            )
        )
    except Exception as exc:
        logger.warning("Inference health check failed: %s", exc)
        services.append(
            ServiceStatus(
                name="Inference",
                status="OFFLINE",
                detail=str(exc)[:160],
            )
        )

    overall_status = (
        "OPTIMAL" if all(service.status == "ONLINE" for service in services) else "DEGRADED"
    )
    return {
        "status": overall_status,
        "services": [service.model_dump() for service in services],
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_agent_config(agent_id: str) -> AgentConfig:
    try:
        cached_config = get_cached_agent_config(agent_id)
        if cached_config is not None:
            return cached_config

        payload = redis.get(f"agent:{agent_id}")
        if not payload:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found in registry")
        agent_config = _parse_agent_payload(agent_id, _decode_redis_value(payload))
        set_cached_agent_config(agent_config)
        return agent_config
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Error fetching agent config for %s: %s", agent_id, exc)
        raise HTTPException(status_code=500, detail="Error fetching agent configuration")


async def fetch_context_messages(session_id: UUID, limit: int = 5) -> List[Dict[str, Any]]:
    try:
        raw_entries = redis.lrange(f"session:{session_id}:messages", -limit, -1) or []
        context: List[Dict[str, Any]] = []

        for offset, raw_entry in enumerate(raw_entries, start=1):
            item = _load_message_record(raw_entry)
            if not item:
                continue
            context.append(
                {
                    "agent_id": item["agent_id"],
                    "display_name": item.get("display_name", item["agent_id"]),
                    "message": item["message"],
                    "turn_number": item.get("turn_number", offset),
                }
            )

        return context
    except Exception as exc:
        logger.warning("Error fetching context messages for %s: %s", session_id, exc)
        return []


async def save_session_topic(session_id: UUID, topic: str) -> None:
    try:
        redis.set(f"session:{session_id}:topic", topic)
        redis.expire(f"session:{session_id}:topic", 60 * 60 * 24 * 30)
    except Exception as exc:
        logger.warning("Unable to persist topic for session %s: %s", session_id, exc)


async def clear_session_storage(session_id: UUID) -> None:
    session_messages_key = f"session:{session_id}:messages"
    session_topic_key = f"session:{session_id}:topic"

    try:
        raw_entries = redis.lrange(session_messages_key, 0, -1) or []
        legacy_message_keys = [
            message_key
            for raw_entry in raw_entries
            if (message_key := _extract_legacy_message_key(raw_entry))
        ]

        pipeline = redis.pipeline()
        pipeline.delete(session_messages_key)
        pipeline.delete(session_topic_key)
        for message_key in legacy_message_keys:
            pipeline.delete(message_key)
        pipeline.exec()
    except Exception as exc:
        logger.warning("Unable to clear session %s: %s", session_id, exc)
        raise


async def fetch_session_topic(session_id: UUID) -> str:
    try:
        payload = redis.get(f"session:{session_id}:topic")
        if not payload:
            return ""
        return _decode_redis_value(payload)
    except Exception as exc:
        logger.warning("Unable to fetch topic for session %s: %s", session_id, exc)
        return ""


def build_context_prompt(topic: str, context_messages: List[Dict[str, Any]], agent_config: AgentConfig) -> str:
    if not context_messages:
        return (
            f"{agent_config.system_prompt}\n\n"
            f"Discussion topic: {topic}\n"
            "You are taking the first turn. Provide a clear, substantive response."
        )

    context_text = "\n".join(
        [f"Turn {msg.get('turn_number', '-')}, {msg.get('display_name', msg['agent_id'])}: {msg['message']}" for msg in context_messages]
    )

    return (
        f"{agent_config.system_prompt}\n\n"
        f"Discussion topic: {topic}\n"
        "Recent discussion context (latest turns):\n"
        f"{context_text}\n\n"
        "Now contribute the next turn. Keep it concise, concrete, and relevant."
    )


async def call_llm_api(prompt: str, agent_config: AgentConfig) -> tuple[str, ExecutionMetrics]:
    api_url = f"{LLM_API_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {LLM_API_KEY}"}
    payload = {
        "model": LLM_MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": agent_config.temperature,
        "max_tokens": agent_config.max_tokens,
        "top_p": 0.95,
        "stream": False,
    }

    try:
        request_started = time.perf_counter()
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            network_rtt_ms = int((time.perf_counter() - request_started) * 1000)

        if isinstance(data, dict):
            choices = data.get("choices") or []
            if choices:
                message = choices[0].get("message") or {}
                content = message.get("content", "")
                if isinstance(content, list):
                    content = "".join(
                        item.get("text", "") if isinstance(item, dict) else str(item)
                        for item in content
                    )
                content = str(content).strip()
                metrics = _extract_execution_metrics(data, response.headers, network_rtt_ms)
                return content or "I need a moment to process this turn.", metrics

        logger.error("Unexpected LLM API payload: %s", data)
        raise HTTPException(status_code=500, detail="Invalid response from LLM API")
    except HTTPException:
        raise
    except httpx.HTTPStatusError as exc:
        error_text = "Unknown upstream error"
        try:
            data = exc.response.json()
            if isinstance(data, dict):
                error_text = data.get("error") or data.get("message") or str(data)
            else:
                error_text = str(data)
        except Exception:
            error_text = exc.response.text[:300] if exc.response is not None else "No response body"

        logger.error(
            "LLM provider status error: status=%s, body=%s",
            exc.response.status_code if exc.response is not None else "unknown",
            error_text,
        )
        raise HTTPException(
            status_code=502,
            detail=f"LLM API error ({exc.response.status_code}): {error_text}",
        )
    except httpx.HTTPError as exc:
        logger.error("LLM provider transport error: %s", exc)
        raise HTTPException(status_code=502, detail="Error communicating with LLM API")


async def save_message_to_storage(
    *,
    session_id: UUID,
    agent_id: str,
    display_name: str,
    message: str,
    topic: str,
    turn_number: int,
) -> Dict[str, Any]:
    message_id = uuid4()
    created_at = datetime.now(timezone.utc).isoformat()

    record = {
        "id": str(message_id),
        "session_id": str(session_id),
        "agent_id": agent_id,
        "display_name": display_name,
        "message": message,
        "topic": topic,
        "turn_number": turn_number,
        "created_at": created_at,
    }

    try:
        # Persist semantically searchable discussion content to Upstash Vector.
        # Some indexes are configured without embedding support; do not fail the request
        # when vector write is unavailable.
        try:
            vector_index.upsert(
                vectors=[
                    (
                        str(message_id),
                        message,
                        {
                            "session_id": str(session_id),
                            "agent_id": agent_id,
                            "display_name": display_name,
                            "topic": topic,
                            "turn_number": turn_number,
                            "created_at": created_at,
                        },
                    )
                ]
            )
        except Exception as vector_exc:
            logger.warning("Vector upsert skipped: %s", vector_exc)

        # Keep ordered timeline in Redis for deterministic "last 5" and PDF export.
        pipeline = redis.pipeline()
        pipeline.rpush(f"session:{session_id}:messages", json.dumps(record))
        pipeline.expire(f"session:{session_id}:messages", 60 * 60 * 24 * 30)
        pipeline.exec()

        return record
    except Exception as exc:
        logger.error("Error saving message to Upstash: %s", exc)
        raise HTTPException(status_code=500, detail="Error saving message to Upstash")


async def fetch_session_messages(session_id: UUID) -> List[Dict[str, Any]]:
    raw_entries = redis.lrange(f"session:{session_id}:messages", 0, -1) or []
    messages: List[Dict[str, Any]] = []

    for index, raw_entry in enumerate(raw_entries, start=1):
        item = _load_message_record(raw_entry)
        if not item:
            continue
        if "turn_number" not in item:
            item["turn_number"] = index
        messages.append(item)

    messages.sort(key=lambda item: int(item.get("turn_number", 0)))
    return messages


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "name": "EXHUMED",
        "version": "1.1.0",
        "status": "operational",
        "storage": "upstash-redis-vector",
        "endpoints": {
            "process_turn": "/process-turn (POST)",
            "generate_with_telemetry": "/generate (POST) - includes Jaccard Entropy telemetry",
            "export_pdf": "/export-pdf/{session_id} (GET)",
            "list_agents": "/agents (GET)",
            "register_agent": "/agents/register (POST)",
            "get_session_topic": "/sessions/{session_id}/topic (GET)",
            "set_session_topic": "/sessions/{session_id}/topic (POST)",
        },
    }


@app.get("/services-status")
async def services_status() -> Dict[str, Any]:
    return await check_services()


@app.get("/telemetry/latest")
async def latest_telemetry() -> Dict[str, Any]:
    metrics = fetch_latest_execution_metrics()
    if metrics is None:
        return {"status": "idle", "metrics": None}
    return {"status": "ok", "metrics": metrics.model_dump(mode="json")}


@app.get("/sessions/{session_id}/topic")
async def get_session_topic(session_id: UUID) -> Dict[str, Any]:
    topic = await fetch_session_topic(session_id)
    return {"session_id": str(session_id), "topic": topic}


@app.post("/sessions/{session_id}/topic")
async def set_session_topic(session_id: UUID, request: SessionTopicUpdateRequest) -> Dict[str, Any]:
    await save_session_topic(session_id, request.topic)
    return {"status": "ok", "session_id": str(session_id), "topic": request.topic}


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: UUID) -> Dict[str, Any]:
    try:
        await clear_session_storage(session_id)
        return {"status": "ok", "session_id": str(session_id)}
    except Exception as exc:
        logger.error("Error clearing session %s: %s", session_id, exc)
        raise HTTPException(status_code=500, detail="Error clearing session")


@app.post("/agents/register")
async def register_agent(request: AgentRegisterRequest) -> Dict[str, Any]:
    payload = {
        "display_name": request.display_name,
        "system_prompt": request.system_prompt,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
    }

    try:
        redis.set(f"agent:{request.agent_id}", json.dumps(payload))
        redis.sadd("agents:index", request.agent_id)
        invalidate_agent_registry_cache()
        invalidate_agent_config_cache(request.agent_id)
        return {"status": "ok", "agent_id": request.agent_id}
    except Exception as exc:
        logger.error("Error registering agent %s: %s", request.agent_id, exc)
        raise HTTPException(status_code=500, detail="Error registering agent")


@app.get("/agents")
async def list_agents() -> Dict[str, Any]:
    try:
        cached_agents = get_cached_agent_registry()
        if cached_agents is not None:
            return {"agents": cached_agents}

        ids = redis.smembers("agents:index") or []
        agent_ids = sorted(_decode_redis_value(item) for item in ids)
        agents: List[Dict[str, Any]] = []

        for agent_id in agent_ids:
            payload = redis.get(f"agent:{agent_id}")
            if not payload:
                continue
            agent = _parse_agent_payload(agent_id, _decode_redis_value(payload))
            agents.append(agent.model_dump())

        set_cached_agent_registry(agents)
        return {"agents": agents}
    except Exception as exc:
        logger.error("Error listing agents: %s", exc)
        raise HTTPException(status_code=500, detail="Error retrieving agents")


@app.post("/process-turn", response_model=ProcessTurnResponse)
async def process_turn(request: ProcessTurnRequest) -> ProcessTurnResponse:
    logger.info(
        "Processing turn: session=%s, agent=%s, topic=%s",
        request.session_id,
        request.agent_id,
        request.topic,
    )

    agent_config = await fetch_agent_config(request.agent_id)
    context_messages = await fetch_context_messages(request.session_id, limit=5)
    turn_number = request.turn_number or (len(context_messages) + 1)

    prompt = build_context_prompt(request.topic, context_messages, agent_config)
    generated_message, execution_metrics = await call_llm_api(prompt, agent_config)
    save_latest_execution_metrics(execution_metrics)

    stored_message = await save_message_to_storage(
        session_id=request.session_id,
        agent_id=request.agent_id,
        display_name=agent_config.display_name,
        message=generated_message,
        topic=request.topic,
        turn_number=turn_number,
    )

    return ProcessTurnResponse(
        message_id=UUID(str(stored_message["id"])),
        agent_id=request.agent_id,
        display_name=agent_config.display_name,
        message=generated_message,
        turn_number=turn_number,
        created_at=datetime.now(timezone.utc),
    )


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """
    Generate an AI response with Jaccard Similarity Entropy telemetry.
    
    This endpoint produces a response from the specified agent and calculates
    entropy metrics by comparing it against the previous agent's response.
    """
    logger.info(
        "Generating response: session=%s, agent=%s, topic=%s",
        request.session_id,
        request.agent_id,
        request.topic,
    )
    
    start_time = time.time()

    try:
        await save_session_topic(request.session_id, request.topic)
        
        agent_config = await fetch_agent_config(request.agent_id)
        context_messages = await fetch_context_messages(request.session_id, limit=5)
        turn_number = len(context_messages) + 1

        prompt = build_context_prompt(request.topic, context_messages, agent_config)
        generated_message, execution_metrics = await call_llm_api(prompt, agent_config)
        save_latest_execution_metrics(execution_metrics)
        
        # Calculate latency in milliseconds
        latency_ms = execution_metrics.generation_duration_ms or int((time.time() - start_time) * 1000)
        
        # Calculate Jaccard Entropy (0.0 for first turn, or compared to previous response)
        if request.previous_response:
            entropy = calculate_jaccard_entropy(generated_message, request.previous_response)
        else:
            entropy = 0.0  # First turn default
        
        # Calculate word count
        word_count = len(generated_message.split())
        
        # Create telemetry object
        telemetry = TelemetryData(
            entropy=entropy,
            latency_ms=latency_ms,
            word_count=word_count,
        )
        
        # Persist message to storage
        stored_message = await save_message_to_storage(
            session_id=request.session_id,
            agent_id=request.agent_id,
            display_name=agent_config.display_name,
            message=generated_message,
            topic=request.topic,
            turn_number=turn_number,
        )
        
        return GenerateResponse(
            response=generated_message,
            telemetry=telemetry,
            message_id=UUID(str(stored_message["id"])),
            turn_number=turn_number,
        )
        
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Error in /generate endpoint: %s", exc)
        raise HTTPException(status_code=500, detail="Error generating response")


@app.get("/export-pdf/{session_id}")
async def export_pdf(session_id: UUID) -> FileResponse:
    logger.info("Exporting PDF for session: %s", session_id)

    try:
        messages = await fetch_session_messages(session_id)
        if not messages:
            raise HTTPException(status_code=404, detail=f"No messages found for session {session_id}")

        topic = messages[0].get("topic", "N/A")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "EXHUMED - Discussion Session", ln=True, align="C")

        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"Session ID: {session_id}", ln=True)
        pdf.cell(0, 5, f"Topic: {topic}", ln=True)
        pdf.ln(5)

        for msg in messages:
            agent_name = msg.get("display_name", msg.get("agent_id", "Unknown"))

            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(33, 87, 171)
            pdf.cell(0, 4, f"{agent_name} (Turn {msg.get('turn_number', '-')})", ln=True)

            pdf.set_font("Arial", "I", 8)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 3, str(msg.get("created_at", "Unknown")), ln=True)

            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(0, 0, 0)
            text = str(msg.get("message", "")).replace("\n", " ")
            pdf.multi_cell(0, 4, text)
            pdf.ln(2)

        pdf_path = os.path.join(tempfile.gettempdir(), f"exhumed_{session_id}.pdf")
        pdf.output(pdf_path)

        return FileResponse(
            path=pdf_path,
            filename=f"exhumed_discussion_{session_id}.pdf",
            media_type="application/pdf",
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Error generating PDF for %s: %s", session_id, exc)
        raise HTTPException(status_code=500, detail="Error generating PDF export")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error("HTTP Exception: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
