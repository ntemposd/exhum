"""
Roundtable Legends: FastAPI Backend
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

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

# Load environment variables from the local .env file when present.
load_dotenv(BASE_DIR / ".env")

# Upstash and model config
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
UPSTASH_VECTOR_REST_URL = os.getenv("UPSTASH_VECTOR_REST_URL")
UPSTASH_VECTOR_REST_TOKEN = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct:fastest")
HF_API_BASE_URL = os.getenv("HF_API_BASE_URL", "https://router.huggingface.co/v1")

required_env = [
    "UPSTASH_REDIS_REST_URL",
    "UPSTASH_REDIS_REST_TOKEN",
    "UPSTASH_VECTOR_REST_URL",
    "UPSTASH_VECTOR_REST_TOKEN",
    "HF_TOKEN",
]
missing_env = [name for name in required_env if not os.getenv(name)]
if missing_env:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_env)}")

redis = Redis(url=UPSTASH_REDIS_REST_URL, token=UPSTASH_REDIS_REST_TOKEN)
vector_index = Index(url=UPSTASH_VECTOR_REST_URL, token=UPSTASH_VECTOR_REST_TOKEN)

app = FastAPI(
    title="Roundtable Legends",
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
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


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


class GenerateResponse(BaseModel):
    response: str = Field(..., description="Generated response text")
    telemetry: TelemetryData = Field(..., description="Telemetry metrics")
    message_id: Optional[UUID] = Field(None, description="Message ID if persisted")
    turn_number: Optional[int] = Field(None, description="Turn number if persisted")


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


async def fetch_agent_config(agent_id: str) -> AgentConfig:
    try:
        payload = redis.get(f"agent:{agent_id}")
        if not payload:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found in registry")
        return _parse_agent_payload(agent_id, _decode_redis_value(payload))
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Error fetching agent config for %s: %s", agent_id, exc)
        raise HTTPException(status_code=500, detail="Error fetching agent configuration")


async def fetch_context_messages(session_id: UUID, limit: int = 5) -> List[Dict[str, Any]]:
    try:
        msg_ids = redis.lrange(f"session:{session_id}:messages", -limit, -1) or []
        context: List[Dict[str, Any]] = []

        for raw_msg_id in msg_ids:
            msg_id = _decode_redis_value(raw_msg_id)
            payload = redis.get(f"message:{msg_id}")
            if not payload:
                continue
            item = json.loads(_decode_redis_value(payload))
            context.append(
                {
                    "agent_id": item["agent_id"],
                    "display_name": item.get("display_name", item["agent_id"]),
                    "message": item["message"],
                    "turn_number": item.get("turn_number", 0),
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


async def call_huggingface_api(prompt: str, agent_config: AgentConfig) -> str:
    api_url = f"{HF_API_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "model": HF_MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": agent_config.temperature,
        "max_tokens": agent_config.max_tokens,
        "top_p": 0.95,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

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
                return content or "I need a moment to process this turn."

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
            "Hugging Face status error: status=%s, body=%s",
            exc.response.status_code if exc.response is not None else "unknown",
            error_text,
        )
        raise HTTPException(
            status_code=502,
            detail=f"LLM API error ({exc.response.status_code}): {error_text}",
        )
    except httpx.HTTPError as exc:
        logger.error("Hugging Face transport error: %s", exc)
        raise HTTPException(status_code=502, detail="Error communicating with LLM API")


async def get_next_turn_number(session_id: UUID) -> int:
    try:
        count = redis.llen(f"session:{session_id}:messages")
        return int(count) + 1
    except Exception:
        return 1


async def save_message_to_storage(
    *,
    session_id: UUID,
    agent_id: str,
    display_name: str,
    message: str,
    topic: str,
    turn_number: int,
) -> UUID:
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
        redis.set(f"message:{message_id}", json.dumps(record))
        redis.rpush(f"session:{session_id}:messages", str(message_id))
        redis.expire(f"message:{message_id}", 60 * 60 * 24 * 30)
        redis.expire(f"session:{session_id}:messages", 60 * 60 * 24 * 30)

        return message_id
    except Exception as exc:
        logger.error("Error saving message to Upstash: %s", exc)
        raise HTTPException(status_code=500, detail="Error saving message to Upstash")


async def fetch_session_messages(session_id: UUID) -> List[Dict[str, Any]]:
    msg_ids = redis.lrange(f"session:{session_id}:messages", 0, -1) or []
    messages: List[Dict[str, Any]] = []

    for raw_msg_id in msg_ids:
        msg_id = _decode_redis_value(raw_msg_id)
        payload = redis.get(f"message:{msg_id}")
        if not payload:
            continue
        messages.append(json.loads(_decode_redis_value(payload)))

    messages.sort(key=lambda item: int(item.get("turn_number", 0)))
    return messages


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "name": "Roundtable Legends",
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


@app.get("/sessions/{session_id}/topic")
async def get_session_topic(session_id: UUID) -> Dict[str, Any]:
    topic = await fetch_session_topic(session_id)
    return {"session_id": str(session_id), "topic": topic}


@app.post("/sessions/{session_id}/topic")
async def set_session_topic(session_id: UUID, request: SessionTopicUpdateRequest) -> Dict[str, Any]:
    await save_session_topic(session_id, request.topic)
    return {"status": "ok", "session_id": str(session_id), "topic": request.topic}


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
        return {"status": "ok", "agent_id": request.agent_id}
    except Exception as exc:
        logger.error("Error registering agent %s: %s", request.agent_id, exc)
        raise HTTPException(status_code=500, detail="Error registering agent")


@app.get("/agents")
async def list_agents() -> Dict[str, Any]:
    try:
        ids = redis.smembers("agents:index") or []
        agent_ids = sorted(_decode_redis_value(item) for item in ids)
        agents: List[Dict[str, Any]] = []

        for agent_id in agent_ids:
            payload = redis.get(f"agent:{agent_id}")
            if not payload:
                continue
            agent = _parse_agent_payload(agent_id, _decode_redis_value(payload))
            agents.append(agent.model_dump())

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

    await save_session_topic(request.session_id, request.topic)

    agent_config = await fetch_agent_config(request.agent_id)
    context_messages = await fetch_context_messages(request.session_id, limit=5)
    turn_number = await get_next_turn_number(request.session_id)

    prompt = build_context_prompt(request.topic, context_messages, agent_config)
    generated_message = await call_huggingface_api(prompt, agent_config)

    message_id = await save_message_to_storage(
        session_id=request.session_id,
        agent_id=request.agent_id,
        display_name=agent_config.display_name,
        message=generated_message,
        topic=request.topic,
        turn_number=turn_number,
    )

    return ProcessTurnResponse(
        message_id=message_id,
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
        turn_number = await get_next_turn_number(request.session_id)

        prompt = build_context_prompt(request.topic, context_messages, agent_config)
        generated_message = await call_huggingface_api(prompt, agent_config)
        
        # Calculate latency in milliseconds
        latency_ms = int((time.time() - start_time) * 1000)
        
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
        message_id = await save_message_to_storage(
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
            message_id=message_id,
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
        pdf.cell(0, 10, "Roundtable Legends - Discussion Session", ln=True, align="C")

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

        pdf_path = os.path.join(tempfile.gettempdir(), f"roundtable_{session_id}.pdf")
        pdf.output(pdf_path)

        return FileResponse(
            path=pdf_path,
            filename=f"roundtable_discussion_{session_id}.pdf",
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
