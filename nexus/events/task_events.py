from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskEventType(str, Enum):
    CREATED = "task.created"
    UPDATED = "task.updated"
    DELETED = "task.deleted"

    ASSIGNED = "task.assigned"
    UNASSIGNED = "task.unassigned"

    READY = "task.ready"
    STARTED = "task.started"
    PAUSED = "task.paused"
    BLOCKED = "task.blocked"
    UNBLOCKED = "task.unblocked"

    COMPLETED = "task.completed"
    FAILED = "task.failed"
    CANCELLED = "task.cancelled"

    DEPENDENCY_ADDED = "task.dependency_added"
    DEPENDENCY_REMOVED = "task.dependency_removed"

    PROGRESS_UPDATED = "task.progress_updated"


@dataclass(slots=True)
class TaskEvent:
    event_type: TaskEventType

    task_id: str

    project_id: str | None = None

    source: str = "system"

    data: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    id: str = field(default_factory=lambda: str(uuid4()))

    actor: str | None = None

    correlation_id: str | None = None

    version: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.event_type.value,
            "task_id": self.task_id,
            "project_id": self.project_id,
            "source": self.source,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def created(cls, task_id: str, source: str, **data):
        return cls(
            event_type=TaskEventType.CREATED,
            task_id=task_id,
            source=source,
            data=data,
        )

    @classmethod
    def assigned(
        cls,
        task_id: str,
        source: str,
        assignee: str,
    ):
        return cls(
            event_type=TaskEventType.ASSIGNED,
            task_id=task_id,
            source=source,
            data={"assignee": assignee},
        )

    @classmethod
    def started(cls, task_id: str, source: str):
        return cls(
            event_type=TaskEventType.STARTED,
            task_id=task_id,
            source=source,
        )

    @classmethod
    def completed(
        cls,
        task_id: str,
        source: str,
        duration: float | None = None,
    ):
        return cls(
            event_type=TaskEventType.COMPLETED,
            task_id=task_id,
            source=source,
            data={"duration": duration},
        )

    @classmethod
    def failed(
        cls,
        task_id: str,
        source: str,
        reason: str,
    ):
        return cls(
            event_type=TaskEventType.FAILED,
            task_id=task_id,
            source=source,
            data={"reason": reason},
        )

    @classmethod
    def progress(
        cls,
        task_id: str,
        source: str,
        progress: float,
    ):
        return cls(
            event_type=TaskEventType.PROGRESS_UPDATED,
            task_id=task_id,
            source=source,
            data={"progress": progress},
        )
