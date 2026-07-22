from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ProjectEventType(str, Enum):
    CREATED = "project.created"
    UPDATED = "project.updated"
    DELETED = "project.deleted"

    STARTED = "project.started"
    PAUSED = "project.paused"
    COMPLETED = "project.completed"

    OWNER_CHANGED = "project.owner_changed"

    STATUS_CHANGED = "project.status_changed"
    PRIORITY_CHANGED = "project.priority_changed"

    MILESTONE_ADDED = "project.milestone_added"
    MILESTONE_COMPLETED = "project.milestone_completed"

    TASK_ADDED = "project.task_added"
    TASK_REMOVED = "project.task_removed"

    BUDGET_UPDATED = "project.budget_updated"

    RISK_ADDED = "project.risk_added"

    DECISION_RECORDED = "project.decision_recorded"


@dataclass(slots=True)
class ProjectEvent:
    event_type: ProjectEventType

    project_id: str

    source: str

    data: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    id: str = field(default_factory=lambda: str(uuid4()))

    version: int = 1

    correlation_id: str | None = None

    actor: str | None = None

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "type": self.event_type.value,
            "project_id": self.project_id,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "actor": self.actor,
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def created(cls, project_id: str, source: str, **data):

        return cls(
            event_type=ProjectEventType.CREATED,
            project_id=project_id,
            source=source,
            data=data,
        )

    @classmethod
    def updated(cls, project_id: str, source: str, **data):

        return cls(
            event_type=ProjectEventType.UPDATED,
            project_id=project_id,
            source=source,
            data=data,
        )

    @classmethod
    def completed(cls, project_id: str, source: str, **data):

        return cls(
            event_type=ProjectEventType.COMPLETED,
            project_id=project_id,
            source=source,
            data=data,
        )

    @classmethod
    def status_changed(
        cls,
        project_id: str,
        source: str,
        old_status: str,
        new_status: str,
    ):

        return cls(
            event_type=ProjectEventType.STATUS_CHANGED,
            project_id=project_id,
            source=source,
            data={
                "old_status": old_status,
                "new_status": new_status,
            },
        )
