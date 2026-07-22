"""
world_model/task.py

Task model for Nexus.

A Task is the smallest executable unit in the system.
Tasks are owned by an Agent and executed by the
ExecutionEngine.
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

class TaskStatus(str, Enum):
    TODO = "todo"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------
# Task
# ---------------------------------------------------------

@dataclass
class Task:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    milestone_id: Optional[str] = None

    parent_task: Optional[str] = None

    title: str = ""

    description: str = ""

    goal: str = ""

    owner: Optional[str] = None

    assigned_agent: Optional[str] = None

    status: TaskStatus = TaskStatus.TODO

    priority: TaskPriority = TaskPriority.NORMAL

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    due_date: Optional[datetime] = None

    estimated_hours: float = 0.0

    actual_hours: float = 0.0

    progress: float = 0.0

    dependencies: List[str] = field(default_factory=list)

    blockers: List[str] = field(default_factory=list)

    subtasks: List[str] = field(default_factory=list)

    required_skills: List[str] = field(default_factory=list)

    required_resources: List[str] = field(default_factory=list)

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    outputs: Dict = field(default_factory=dict)

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    def start(self):

        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.touch()

    # -----------------------------------------------------

    def complete(self):

        self.status = TaskStatus.COMPLETED
        self.progress = 100
        self.completed_at = datetime.utcnow()
        self.touch()

    # -----------------------------------------------------

    def fail(self, reason: str):

        self.status = TaskStatus.FAILED
        self.metadata["failure_reason"] = reason
        self.touch()

    # -----------------------------------------------------

    def block(self, reason: str):

        self.status = TaskStatus.BLOCKED
        self.blockers.append(reason)
        self.touch()

    # -----------------------------------------------------

    def unblock(self):

        self.blockers.clear()

        if self.status == TaskStatus.BLOCKED:
            self.status = TaskStatus.READY

        self.touch()

    # -----------------------------------------------------

    def cancel(self):

        self.status = TaskStatus.CANCELLED
        self.touch()

    # -----------------------------------------------------

    def set_progress(self, value: float):

        self.progress = max(0, min(100, value))

        if self.progress == 100:
            self.complete()
        else:
            self.touch()

    # -----------------------------------------------------

    def add_dependency(self, task_id: str):

        if task_id not in self.dependencies:
            self.dependencies.append(task_id)

        self.touch()

    # -----------------------------------------------------

    def remove_dependency(self, task_id: str):

        if task_id in self.dependencies:
            self.dependencies.remove(task_id)

        self.touch()

    # -----------------------------------------------------

    def add_subtask(self, task_id: str):

        if task_id not in self.subtasks:
            self.subtasks.append(task_id)

        self.touch()

    # -----------------------------------------------------

    def assign_owner(self, owner: str):

        self.owner = owner
        self.touch()

    # -----------------------------------------------------

    def assign_agent(self, agent: str):

        self.assigned_agent = agent
        self.touch()

    # -----------------------------------------------------

    def log_output(self, key: str, value):

        self.outputs[key] = value
        self.touch()

    # -----------------------------------------------------

    def add_tag(self, tag: str):

        if tag not in self.tags:
            self.tags.append(tag)

        self.touch()

    # -----------------------------------------------------

    def remove_tag(self, tag: str):

        if tag in self.tags:
            self.tags.remove(tag)

        self.touch()

    # -----------------------------------------------------

    def is_ready(self, completed_tasks: List[str]):

        return all(dep in completed_tasks for dep in self.dependencies)

    # -----------------------------------------------------

    def is_overdue(self):

        if self.due_date is None:
            return False

        return (
            datetime.utcnow() > self.due_date
            and self.status != TaskStatus.COMPLETED
        )

    # -----------------------------------------------------

    def duration(self):

        if self.started_at and self.completed_at:
            return (
                self.completed_at - self.started_at
            ).total_seconds()

        return None

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "priority": self.priority.value,
            "owner": self.owner,
            "agent": self.assigned_agent,
            "progress": self.progress,
            "dependencies": len(self.dependencies),
            "subtasks": len(self.subtasks),
            "blockers": len(self.blockers),
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
            f"<Task "
            f"title='{self.title}' "
            f"status='{self.status.value}' "
            f"progress={self.progress}%>"
        )
