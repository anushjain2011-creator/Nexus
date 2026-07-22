"""
world_model/milestone.py

Milestone model for Nexus.

A Milestone represents a major phase or deliverable within a
project. It groups tasks together and tracks overall progress.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


# ---------------------------------------------------------
# Enums
# ---------------------------------------------------------

class MilestoneStatus(str, Enum):
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------
# Milestone
# ---------------------------------------------------------

@dataclass
class Milestone:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    title: str = ""

    description: str = ""

    owner: Optional[str] = None

    status: MilestoneStatus = MilestoneStatus.NOT_STARTED

    priority: int = 5

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    start_date: Optional[datetime] = None

    due_date: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    progress: float = 0.0

    task_ids: List[str] = field(default_factory=list)

    dependency_ids: List[str] = field(default_factory=list)

    deliverables: List[str] = field(default_factory=list)

    success_criteria: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    def start(self):

        self.status = MilestoneStatus.ACTIVE

        if self.start_date is None:
            self.start_date = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def complete(self):

        self.status = MilestoneStatus.COMPLETED

        self.progress = 100

        self.completed_at = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def cancel(self):

        self.status = MilestoneStatus.CANCELLED

        self.touch()

    # -----------------------------------------------------

    def block(self, reason: str):

        self.status = MilestoneStatus.BLOCKED

        self.metadata["block_reason"] = reason

        self.touch()

    # -----------------------------------------------------

    def unblock(self):

        if self.status == MilestoneStatus.BLOCKED:
            self.status = MilestoneStatus.ACTIVE

        self.metadata.pop("block_reason", None)

        self.touch()

    # -----------------------------------------------------

    def add_task(self, task_id: str):

        if task_id not in self.task_ids:

            self.task_ids.append(task_id)

            self.touch()

    # -----------------------------------------------------

    def remove_task(self, task_id: str):

        if task_id in self.task_ids:

            self.task_ids.remove(task_id)

            self.touch()

    # -----------------------------------------------------

    def add_dependency(self, milestone_id: str):

        if milestone_id not in self.dependency_ids:

            self.dependency_ids.append(milestone_id)

            self.touch()

    # -----------------------------------------------------

    def add_deliverable(self, deliverable: str):

        self.deliverables.append(deliverable)

        self.touch()

    # -----------------------------------------------------

    def add_success_criteria(self, criteria: str):

        self.success_criteria.append(criteria)

        self.touch()

    # -----------------------------------------------------

    def update_progress(self, completed_tasks: int, total_tasks: int):

        if total_tasks == 0:

            self.progress = 0

        else:

            self.progress = round(
                completed_tasks / total_tasks * 100,
                2,
            )

        if self.progress >= 100:

            self.complete()

        else:

            self.touch()

    # -----------------------------------------------------

    def is_ready(self, completed_milestones: List[str]):

        return all(
            dep in completed_milestones
            for dep in self.dependency_ids
        )

    # -----------------------------------------------------

    def is_overdue(self):

        if self.due_date is None:

            return False

        return (
            datetime.utcnow() > self.due_date
            and self.status != MilestoneStatus.COMPLETED
        )

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "progress": self.progress,
            "tasks": len(self.task_ids),
            "dependencies": len(self.dependency_ids),
            "deliverables": len(self.deliverables),
        }

    # -----------------------------------------------------

    def to_dict(self):

        return asdict(self)

    # -----------------------------------------------------

    @classmethod
    def from_dict(cls, data):

        return cls(**data)

    # -----------------------------------------------------

    def __repr__(self):

        return (
            f"<Milestone "
            f"title='{self.title}' "
            f"status='{self.status.value}' "
            f"progress={self.progress}%>"
        )
