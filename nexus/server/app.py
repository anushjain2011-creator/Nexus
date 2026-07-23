"""
Nexus API server — exposes the WorldModel as JSON for the React dashboard,
and provides endpoints to bootstrap a project and trigger events, so the
dashboard can show the system reacting live.

Run:
    pip install -r requirements.txt fastapi uvicorn
    cp .env.example .env   # fill in OPENAI_API_KEY etc.
    python -m nexus.server.app

Then open web/index.html (or run the Vite dev server, see web/README.md)
and it will poll http://localhost:8000/api/world for live state.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nexus.core.runtime import NexusRuntime
from nexus.agents.executive_agent import ExecutiveAgent
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent

app = FastAPI(title="Nexus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_runtime() -> NexusRuntime:
    """Create a fresh runtime with all agents registered."""
    runtime = NexusRuntime()

    # Keep a rolling log of bus events for the dashboard's live ticker.
    runtime.bus.subscribe("*", lambda e: _event_feed.append(
        {"kind": e.kind, "payload": e.payload, "at": e.at}
    ))

    executive = ExecutiveAgent(runtime)
    planning = PlanningAgent(runtime)
    research = ResearchAgent(runtime)
    finance = FinanceAgent(runtime)
    risk = RiskAgent(runtime)

    runtime.register_agent(executive)
    runtime.register_agent(planning)
    runtime.register_agent(research)
    runtime.register_agent(finance)
    runtime.register_agent(risk)

    return runtime


# Single shared project state for this demo server.
_event_feed: list[dict] = []
_runtime = _build_runtime()


def _get_executive() -> ExecutiveAgent:
    return _runtime.registry.get("executive")


class BootstrapRequest(BaseModel):
    goal: str
    deadline: Optional[str] = None
    budget: Optional[float] = None


class EventRequest(BaseModel):
    description: str


@app.get("/api/world")
def get_world():
    """Full current state — the dashboard polls this."""
    data = _runtime.world.to_dict()
    data["events"] = _event_feed[-50:]  # most recent 50 for the ticker
    return data


@app.post("/api/bootstrap")
def bootstrap(req: BootstrapRequest):
    """Kick off the Intent Engine: goal -> tasks + budget + risks."""
    try:
        exec_agent = _get_executive()
        results = exec_agent.bootstrap_from_goal(
            goal=req.goal, deadline=req.deadline, budget=req.budget
        )
    except Exception as exc:  # surface backend/config errors to the UI
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "results": [
            {"agent": r.agent_name, "summary": r.summary} for r in results
        ],
        "world": _runtime.world.to_dict(),
    }


@app.post("/api/event")
def trigger_event(req: EventRequest):
    """Simulate a mid-project problem and let agents adapt the plan."""
    try:
        exec_agent = _get_executive()
        results = exec_agent.handle_event(req.description)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "results": [
            {"agent": r.agent_name, "summary": r.summary} for r in results
        ],
        "world": _runtime.world.to_dict(),
    }


@app.post("/api/reset")
def reset():
    """Clear state back to an empty project — useful between demo runs."""
    global _runtime, _event_feed
    _event_feed = []
    _runtime = _build_runtime()
    return {"status": "reset"}


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "base_url": os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1",
    }
