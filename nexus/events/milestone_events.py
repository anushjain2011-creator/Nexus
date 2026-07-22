from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class MilestoneEventType(str, Enum):
    CREATED = "milestone.created"
    UPDATED = "milestone.updated"
    DELETED = "milestone.deleted"

    STARTED = "milestone.started"
    COMPLETED = "milestone.completed"

    REOPENED = "milestone.reopened"

    TASK_ADDED = "milestone.task_added"
    TASK_REMOVED = "milestone.task_removed"

    DEADLINE_CHANGED = "milestone.deadline_changed"

    OWNER_CHANGED = "milestone.owner_changed"

    PROGRESS_UPDATED = "milestone.progress_updated"


@dataclass(slots=True)
class MilestoneEvent:
    event_type: MilestoneEventType

    milestone_id: str

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
            "milestone_id": self.milestone_id,
            "project_id": self.project_id,
            "source": self.source,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def created(cls, milestone_id: str, source: str, **data):
        return cls(
            event_type=MilestoneEventType.CREATED,
            milestone_id=milestone_id,
            source=source,
            data=data,
        )

    @classmethod
    def started(cls, milestone_id: str, source: str):
        return cls(
            event_type=MilestoneEventType.STARTED,
            milestone_id=milestone_id,
            source=source,
        )

    @classmethod
    def completed(
        cls,
        milestone_id: str,
        source: str,
        completed_by: str | None = None,
    ):
        return cls(
            event_type=MilestoneEventType.COMPLETED,
            milestone_id=milestone_id,
            source=source,
            data={"completed_by": completed_by},
        )

    @classmethod
    def progress(
        cls,
        milestone_id: str,
        source: str,
        progress: float,
    ):
        return cls(
            event_type=MilestoneEventType.PROGRESS_UPDATED,
            milestone_id=milestone_id,
            source=source,
            data={"progress": progress},
        )

    @classmethod
    def deadline_changed(
        cls,
        milestone_id: str,
        source: str,
        old_deadline: str,
        new_deadline: str,
    ):
        return cls(
            event_type=MilestoneEventType.DEADLINE_CHANGED,
            milestone_id=milestone_id,
            source=source,
            data={
                "old_deadline": old_deadline,
                "new_deadline": new_deadline,
            },
        )

    @classmethod
    def task_added(
        cls,
        milestone_id: str,
        source: str,
        task_id: str,
    ):
        return cls(
            event_type=MilestoneEventType.TASK_ADDED,
            milestone_id=milestone_id,
            source=source,
            data={"task_id": task_id},
        )

    @classmethod
    def task_removed(
        cls,
        milestone_id: str,
        source: str,
        task_id: str,
    ):
        return cls(
            event_type=MilestoneEventType.TASK_REMOVED,
            milestone_id=milestone_id,
            source=source,
            data={"task_id": task_id},
        )
