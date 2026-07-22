"""
world_model/project.py

Core Project model for Nexus.

The Project is the root object of the WorldModel and owns
tasks, milestones, risks, budgets, resources, decisions,
vendors, and stakeholders.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    BLOCKED = "blocked"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Project:

    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    description: str = ""

    owner: Optional[str] = None

    status: ProjectStatus = ProjectStatus.PLANNING

    priority: ProjectPriority = ProjectPriority.NORMAL

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    start_date: Optional[datetime] = None

    due_date: Optional[datetime] = None

    completion: float = 0.0

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    objectives: List[str] = field(default_factory=list)

    assumptions: List[str] = field(default_factory=list)

    constraints: List[str] = field(default_factory=list)

    # Relationships

    task_ids: List[str] = field(default_factory=list)

    milestone_ids: List[str] = field(default_factory=list)

    budget_ids: List[str] = field(default_factory=list)

    risk_ids: List[str] = field(default_factory=list)

    stakeholder_ids: List[str] = field(default_factory=list)

    vendor_ids: List[str] = field(default_factory=list)

    resource_ids: List[str] = field(default_factory=list)

    decision_ids: List[str] = field(default_factory=list)

    event_ids: List[str] = field(default_factory=list)

    # -------------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -------------------------------------------------------

    def add_task(self, task_id: str):

        if task_id not in self.task_ids:
            self.task_ids.append(task_id)
            self.touch()

    # -------------------------------------------------------

    def remove_task(self, task_id: str):

        if task_id in self.task_ids:
            self.task_ids.remove(task_id)
            self.touch()

    # -------------------------------------------------------

    def add_milestone(self, milestone_id: str):

        if milestone_id not in self.milestone_ids:
            self.milestone_ids.append(milestone_id)
            self.touch()

    # -------------------------------------------------------

    def add_budget(self, budget_id: str):

        if budget_id not in self.budget_ids:
            self.budget_ids.append(budget_id)
            self.touch()

    # -------------------------------------------------------

    def add_risk(self, risk_id: str):

        if risk_id not in self.risk_ids:
            self.risk_ids.append(risk_id)
            self.touch()

    # -------------------------------------------------------

    def add_stakeholder(self, stakeholder_id: str):

        if stakeholder_id not in self.stakeholder_ids:
            self.stakeholder_ids.append(stakeholder_id)
            self.touch()

    # -------------------------------------------------------

    def add_vendor(self, vendor_id: str):

        if vendor_id not in self.vendor_ids:
            self.vendor_ids.append(vendor_id)
            self.touch()

    # -------------------------------------------------------

    def add_resource(self, resource_id: str):

        if resource_id not in self.resource_ids:
            self.resource_ids.append(resource_id)
            self.touch()

    # -------------------------------------------------------

    def add_decision(self, decision_id: str):

        if decision_id not in self.decision_ids:
            self.decision_ids.append(decision_id)
            self.touch()

    # -------------------------------------------------------

    def add_event(self, event_id: str):

        self.event_ids.append(event_id)

        self.touch()

    # -------------------------------------------------------

    def progress(self, completed_tasks: int, total_tasks: int):

        if total_tasks == 0:

            self.completion = 0

        else:

            self.completion = round(
                completed_tasks / total_tasks * 100,
                2,
            )

        if self.completion == 100:

            self.status = ProjectStatus.COMPLETED

        self.touch()

    # -------------------------------------------------------

    def is_overdue(self):

        if self.due_date is None:
            return False

        return (
            datetime.utcnow() > self.due_date
            and self.status != ProjectStatus.COMPLETED
        )

    # -------------------------------------------------------

    def to_dict(self):

        return asdict(self)

    # -------------------------------------------------------

    @classmethod
    def from_dict(cls, data: Dict):

        return cls(**data)

    # -------------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "priority": self.priority.value,
            "completion": self.completion,
            "tasks": len(self.task_ids),
            "milestones": len(self.milestone_ids),
            "risks": len(self.risk_ids),
            "budgets": len(self.budget_ids),
            "stakeholders": len(self.stakeholder_ids),
            "vendors": len(self.vendor_ids),
            "resources": len(self.resource_ids),
        }

    # -------------------------------------------------------

    def __repr__(self):

        return (
            f"<Project "
            f"name={self.name!r} "
            f"status={self.status.value!r} "
            f"completion={self.completion}%>"
        )
