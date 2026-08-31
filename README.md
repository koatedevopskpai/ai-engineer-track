# AI Engineer Track — Agentic RAG Support System

Production-style LLM application demonstrating the end-to-end RAG stack: **triage → retrieval →
grounded answering → confidence routing**, backed by a pgvector store and a FastAPI service layer.

This repo is the **foundation build** of a personal AI engineering portfolio. It focuses on a
single vertical slice that works — an agent-driven support assistant — and is deliberately
incremental: each phase builds on the last with real, measured decisions.

---

## What it does

A support ticket enters the system and is handled by a small LangGraph agent:

1. **Triage** — classifies the ticket as L1 / L2 / L3.
2. **Resolve** — retrieves grounded context from the knowledge base and drafts an answer.
3. **QA** — scores the draft's confidence and **routes**: `done` if confident, `escalate` if not.

The agent is **deterministic-first**: local models by default, with a model router that can switch
to an OpenAI-compatible endpoint without changing the agent code.

---

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌───────────┐
│   Ticket    │───▶│   Triage     │───▶│   Retrieve+Resolve │───▶│   QA/route │
└─────────────┘    └──────────────┘    └─────────────────┘    └───────────┘
                                             │                        │
                                    pgvector (PG16)           done / escalate
```

| Component | File | Role |
|---|---|---|
| Agent graph | `code/agent.py` | LangGraph state machine: triage → resolve → qa → route |
| Model router | `code/model_router.py` | Switch between local (Ollama) and OpenAI-compatible providers via `MODEL_PROVIDER` |
| Retrieval | `code/retrieve.py` | pgvector cosine similarity search over embedded knowledge chunks |
| Ingestion | `code/ingest.py` | Chunk + embed `corpus.txt` into the vector store (500-token chunks, 50-token overlap) |
| API layer | `code/main.py` | FastAPI service with `/health` and `/echo` endpoints |
| Data store | `code/docker-compose.yml` | pgvector (PG16) on port 5433 |

---

## Quick start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) with a model pulled (`ollama pull llama3.2`) — or an
  OpenAI-compatible API key

### 1. Start the vector store

```bash
docker compose -f code/docker-compose.yml up -d
```

### 2. Install dependencies

```bash
pip install -r code/requirements.txt   # add if you want a requirements file
```

### 3. Configure the model provider

```bash
cp code/.env.example .env
# MODEL_PROVIDER=ollama            → local, free
# MODEL_PROVIDER=opencode          → OpenAI-compatible (set OPENCODE_API_KEY)
```

### 4. Ingest the knowledge base

```bash
python code/ingest.py
```

### 5. Run the agent

```bash
python code/agent.py
```

### 6. (Optional) Serve the API

```bash
uvicorn code.main:app --reload
# GET  /health
# POST /echo   {"text": "hi", "repeat": 2}
```

---

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `MODEL_PROVIDER` | `ollama` | `ollama` (local) or `opencode` (OpenAI-compatible) |
| `OLLAMA_MODEL` | `llama3.2` | Local model name |
| `OPENCODE_API_KEY` | *(empty)* | Key for OpenAI-compatible provider — **never commit a real key** |
| `PGVECTOR_DSN` | `postgresql://ai:ai@localhost:5433/rag` | Vector store connection |

> **Security:** all secrets live in `.env` (git-ignored). `.env.example` ships with empty values
> only. See the companion `ai-engineer-track-build-01` for the full guardrail/eval layer.

---

## Portfolio context

This is **build 01 of a three-part track**:

| Build | Repo | Focus |
|---|---|---|
| 01 | `ai-engineer-track` | This repo — working vertical slice: agent + RAG + API |
| 02 | `ai-engineer-track-build-01` | Production hardening: guardrails, evals, HITL approval, Docker |
| 03 | `ai-engineer-track-build-02` | Agentic workflow on n8n: 3-way document match with cost/ROI analysis |

---

## Roadmap / known limitations
- **Local-first by design:** defaults to Ollama for free, offline runs; the router makes swapping
  providers trivial.
- **Confidence is heuristic** in this build; `build-01` replaces it with RAGAS-grounded scoring.
- **No auth** on the API yet — add a middleware layer before any real deployment.

---

## License
MIT — free to use, learn from, and build on.

---

*Built as part of a personal AI engineering portfolio. Questions or feedback welcome via issues.*