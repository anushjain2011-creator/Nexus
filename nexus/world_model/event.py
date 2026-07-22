"""
world_model/event.py

Core Event model for Nexus.

Every change to the WorldModel should generate an Event.
Events are published through the EventBus and consumed by
Hooks, Agents, Analytics, Audit, and Simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


# =========================================================
# Enums
# =========================================================

class EventSeverity(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    SYSTEM = "system"
    PROJECT = "project"
    TASK = "task"
    MILESTONE = "milestone"
    BUDGET = "budget"
    RISK = "risk"
    RESOURCE = "resource"
    COMMUNICATION = "communication"
    SECURITY = "security"
    ANALYTICS = "analytics"
    DECISION = "decision"
    SIMULATION = "simulation"
    OTHER = "other"


class EventStatus(str, Enum):
    CREATED = "created"
    PUBLISHED = "published"
    PROCESSED = "processed"
    FAILED = "failed"
    ARCHIVED = "archived"


# =========================================================
# Event
# =========================================================

@dataclass
class Event:

    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    category: EventCategory = EventCategory.SYSTEM

    severity: EventSeverity = EventSeverity.INFO

    status: EventStatus = EventStatus.CREATED

    timestamp: datetime = field(default_factory=datetime.utcnow)

    source: str = ""

    project_id: Optional[str] = None

    milestone_id: Optional[str] = None

    task_id: Optional[str] = None

    workflow_id: Optional[str] = None

    correlation_id: Optional[str] = None

    actor: Optional[str] = None

    payload: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    tags: List[str] = field(default_factory=list)

    parent_event: Optional[str] = None

    child_events: List[str] = field(default_factory=list)

    retries: int = 0

    processed_at: Optional[datetime] = None

    # -----------------------------------------------------

    def publish(self):

        self.status = EventStatus.PUBLISHED

    # -----------------------------------------------------

    def processed(self):

        self.status = EventStatus.PROCESSED

        self.processed_at = datetime.utcnow()

    # -----------------------------------------------------

    def failed(self, reason: str):

        self.status = EventStatus.FAILED

        self.metadata["failure_reason"] = reason

        self.retries += 1

    # -----------------------------------------------------

    def archive(self):

        self.status = EventStatus.ARCHIVED

    # -----------------------------------------------------

    def add_tag(self, tag: str):

        if tag not in self.tags:

            self.tags.append(tag)

    # -----------------------------------------------------

    def remove_tag(self, tag: str):

        if tag in self.tags:

            self.tags.remove(tag)

    # -----------------------------------------------------

    def set_payload(self, key: str, value: Any):

        self.payload[key] = value

    # -----------------------------------------------------

    def set_metadata(self, key: str, value: Any):

        self.metadata[key] = value

    # -----------------------------------------------------

    def add_child(self, event_id: str):

        if event_id not in self.child_events:

            self.child_events.append(event_id)

    # -----------------------------------------------------

    @property
    def age_seconds(self):

        return (
            datetime.utcnow() -
            self.timestamp
        ).total_seconds()

    # -----------------------------------------------------

    @property
    def is_processed(self):

        return self.status == EventStatus.PROCESSED

    # -----------------------------------------------------

    @property
    def is_failed(self):

        return self.status == EventStatus.FAILED

    # -----------------------------------------------------

    @property
    def is_critical(self):

        return self.severity == EventSeverity.CRITICAL

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "severity": self.severity.value,
            "status": self.status.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "children": len(self.child_events),
            "retries": self.retries,
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
            f"<Event "
            f"name='{self.name}' "
            f"category='{self.category.value}' "
            f"status='{self.status.value}'>"
        )
