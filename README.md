# 💀 Exhum

Digital exhumation of historical logic. A multi-agent system where historical figures debate each other in real time.

Built as an experiment in orchestrating LLM agents, managing context, and designing structured interactions between systems.

---

## What this does

- Runs multiple AI agents with distinct personas  
- Orchestrates turn-based debates with strict response constraints  
- Tracks system performance (latency, token usage, context limits) in real time  

---

## How it works

- **Backend:** FastAPI orchestrating asynchronous LLM calls  
- **Frontend:** Streamlit interface for interaction and monitoring  
- **LLM Engine:** Configurable OpenAI-compatible LLM provider for low-latency inference  

Each agent follows a constrained dialogue loop (max 60 words), ensuring focused responses and preventing context drift.

---

## Why I built this

To explore how multi-agent systems behave in structured environments, and how product constraints (latency, cost, context) shape system design.

---

## Key ideas

- Multi-agent orchestration  
- Context management  
- Real-time system telemetry  
- Designing constraints for better outputs  

---

## Deployment

- Backend: Railway
- Frontend: Streamlit Cloud
- Domain: exhumed.streamlit.app

---

## Run Locally

This app uses a FastAPI backend and a Streamlit frontend. To run it locally, start both services in separate terminals.

### 1. Create and configure `.env`

Copy `.env.example` to `.env` and add your real credentials for:

- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`
- `UPSTASH_VECTOR_REST_URL`
- `UPSTASH_VECTOR_REST_TOKEN`
- `LLM_API_KEY`

### 2. Install dependencies

On Windows:

```bat
setup.bat
```

On macOS / Linux:

```bash
./setup.sh
```

### 3. Start the backend

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend runs at `http://localhost:8000`.

### 4. Start the frontend

In a new terminal, run:

```bash
streamlit run frontend/app.py --server.port 8501
```

The frontend runs at `http://localhost:8501`.

### 5. Optional: use the virtual environment executables directly

Windows:

```bat
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
.\.venv\Scripts\streamlit.exe run frontend/app.py --server.port 8501
```

macOS / Linux:

```bash
./.venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
./.venv/bin/streamlit run frontend/app.py --server.port 8501
```

### 6. Optional: run with Docker

```bash
docker-compose up --build
```

This starts the backend on `http://localhost:8000` and the frontend on `http://localhost:8501`.
