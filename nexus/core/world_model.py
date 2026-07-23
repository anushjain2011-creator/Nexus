"""
WorldModel — the shared, connected state that every agent reads from and
writes to. This is what makes agents behave like one system instead of
independent chatbots: they all see the same goals, tasks, budget, risks,
and people, and changes by one agent are visible to all others.

Kept intentionally simple (in-memory + JSON-serializable) so it can be
swapped for a real database later (e.g. a Sub0-backed store) without
changing agent code.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Task:
    id: str = field(default_factory=lambda: _new_id("task"))
    title: str = ""
    status: str = "todo"  # todo | in_progress | blocked | done
    owner: Optional[str] = None
    deadline: Optional[str] = None
    cost: float = 0.0
    depends_on: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)


@dataclass
class Risk:
    id: str = field(default_factory=lambda: _new_id("risk"))
    description: str = ""
    severity: str = "medium"  # low | medium | high
    related_task_id: Optional[str] = None
    mitigation: Optional[str] = None
    created_at: str = field(default_factory=_now)


@dataclass
class BudgetLine:
    id: str = field(default_factory=lambda: _new_id("budget"))
    category: str = ""
    allocated: float = 0.0
    spent: float = 0.0


@dataclass
class Person:
    id: str = field(default_factory=lambda: _new_id("person"))
    name: str = ""
    role: str = ""


class WorldModel:
    """
    In-memory connected state store. Not thread-safe by design — intended
    to be owned by a single orchestrator process that dispatches to agents
    sequentially or via async tasks that serialize writes.
    """

    def __init__(self, goal: str = "", deadline: Optional[str] = None,
                 budget: float = 0.0):
        self.goal = goal
        self.deadline = deadline
        self.budget_total = budget

        self.tasks: dict[str, Task] = {}
        self.risks: dict[str, Risk] = {}
        self.budget_lines: dict[str, BudgetLine] = {}
        self.people: dict[str, Person] = {}
        self.knowledge: list[dict[str, Any]] = []  # freeform notes/findings
        self.log: list[dict[str, Any]] = []  # audit trail of changes

    # ---- mutation helpers -------------------------------------------------

    def add_task(self, **kwargs) -> Task:
        t = Task(**kwargs)
        self.tasks[t.id] = t
        self._record("task_created", {"task_id": t.id, "title": t.title})
        return t

    def update_task(self, task_id: str, **updates) -> Task:
        t = self.tasks[task_id]
        for k, v in updates.items():
            setattr(t, k, v)
        t.updated_at = _now()
        self._record("task_updated", {"task_id": task_id, "updates": updates})
        return t

    def add_risk(self, **kwargs) -> Risk:
        r = Risk(**kwargs)
        self.risks[r.id] = r
        self._record("risk_added", {"risk_id": r.id, "description": r.description})
        return r

    def add_budget_line(self, **kwargs) -> BudgetLine:
        b = BudgetLine(**kwargs)
        self.budget_lines[b.id] = b
        self._record("budget_line_added", {"budget_id": b.id, "category": b.category})
        return b

    def add_person(self, **kwargs) -> Person:
        p = Person(**kwargs)
        self.people[p.id] = p
        self._record("person_added", {"person_id": p.id, "name": p.name})
        return p

    def add_knowledge(self, note: str, source: Optional[str] = None,
                       related_task_id: Optional[str] = None) -> None:
        self.knowledge.append({
            "note": note,
            "source": source,
            "related_task_id": related_task_id,
            "created_at": _now(),
        })
        self._record("knowledge_added", {"note": note})

    def _record(self, kind: str, payload: dict[str, Any]) -> None:
        self.log.append({"kind": kind, "payload": payload, "at": _now()})

    # ---- read helpers -------------------------------------------------

    def budget_spent(self) -> float:
        return sum(b.spent for b in self.budget_lines.values())

    def budget_remaining(self) -> float:
        return self.budget_total - self.budget_spent()

    def blocked_tasks(self) -> list[Task]:
        return [t for t in self.tasks.values() if t.status == "blocked"]

    def high_severity_risks(self) -> list[Risk]:
        return [r for r in self.risks.values() if r.severity == "high"]

    def update(self, values: dict[str, Any]) -> None:
        """Apply a shallow dict of field updates, e.g. {'goal': ..., 'deadline': ...,
        'budget': 1000}. Unknown keys are ignored."""
        for key, value in values.items():
            if key == "budget":
                self.budget_total = value
            elif hasattr(self, key):
                setattr(self, key, value)
        self._record("world.updated", values)

    def get_state(self) -> dict[str, Any]:
        """Alias for to_dict(), used by NexusRuntime/callers that want the
        current world state as a plain dict."""
        return self.to_dict()
        
    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "deadline": self.deadline,
            "budget_total": self.budget_total,
            "budget_spent": self.budget_spent(),
            "tasks": [asdict(t) for t in self.tasks.values()],
            "risks": [asdict(r) for r in self.risks.values()],
            "budget_lines": [asdict(b) for b in self.budget_lines.values()],
            "people": [asdict(p) for p in self.people.values()],
            "knowledge": self.knowledge,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def summary_for_prompt(self) -> str:
        """A compact text summary suitable for injecting into an LLM prompt
        so agents have shared situational awareness without the full dump."""
        lines = [
            f"Goal: {self.goal}",
            f"Deadline: {self.deadline}",
            f"Budget: {self.budget_spent():.2f} / {self.budget_total:.2f} spent"
            f" ({self.budget_remaining():.2f} remaining)",
            f"Tasks: {len(self.tasks)} total, "
            f"{sum(1 for t in self.tasks.values() if t.status == 'done')} done, "
            f"{len(self.blocked_tasks())} blocked",
            f"Risks: {len(self.risks)} total, "
            f"{len(self.high_severity_risks())} high severity",
        ]
        if self.blocked_tasks():
            lines.append("Blocked tasks: " + ", ".join(
                t.title for t in self.blocked_tasks()))
        if self.high_severity_risks():
            lines.append("High severity risks: " + ", ".join(
                r.description for r in self.high_severity_risks()))
        return "\n".join(lines)
