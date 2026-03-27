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
- **LLM Engine:** Llama 3 via Groq for low-latency inference  

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

- Backend: Render  
- Frontend: Streamlit Cloud  
- Domain: exhum.ntemposd.me