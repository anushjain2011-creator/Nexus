# Nexus

A lightweight AI agent framework with a live React dashboard.

## Stack

- **Backend**: FastAPI (Python) — `nexus/server/app.py` — port 8000
- **Frontend**: React + Vite — `nexus/web/` — port 5000
- **Agents**: `nexus/agents/` (Executive, Planning, Research, Finance, Risk)
- **Core**: `nexus/core/` — event bus, world model, registry

## Running on Replit

Two workflows run automatically:

| Workflow | Command | Port |
|---|---|---|
| **Start application** | `cd nexus/web && npm run dev` | 5000 (preview) |
| **Backend API** | `python -m uvicorn nexus.server.app:app --host 0.0.0.0 --port 8000` | 8000 |

The Vite dev server proxies `/api/*` requests to the backend, so the frontend uses relative URLs.

## Required secrets

| Secret | Purpose |
|---|---|
| `OPENAI_API_KEY` | Required — powers all agent LLM calls |
| `OPENAI_BASE_URL` | Optional — override the OpenAI endpoint |
| `OPENAI_MODEL` | Optional — defaults to `gpt-4o-mini` |

## Project structure

```
nexus/
  core/         shared engine (event bus, world model, registry, runtime)
  agents/       agent implementations
  server/       FastAPI app (app.py)
  web/          React dashboard (Vite)
tests/          pytest test suite
requirements.txt
```

## User preferences

- Keep the project's existing structure and stack.
