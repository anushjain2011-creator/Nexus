from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class RiskEventType(str, Enum):
    CREATED = "risk.created"
    UPDATED = "risk.updated"

    IDENTIFIED = "risk.identified"

    SCORE_CHANGED = "risk.score_changed"
    SEVERITY_CHANGED = "risk.severity_changed"

    OWNER_ASSIGNED = "risk.owner_assigned"

    MITIGATION_ADDED = "risk.mitigation_added"

    MONITORING = "risk.monitoring"

    ESCALATED = "risk.escalated"

    MITIGATED = "risk.mitigated"

    CLOSED = "risk.closed"


@dataclass(slots=True)
class RiskEvent:
    event_type: RiskEventType

    risk_id: str

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
            "risk_id": self.risk_id,
            "project_id": self.project_id,
            "source": self.source,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def created(cls, risk_id: str, source: str, **data):
        return cls(
            event_type=RiskEventType.CREATED,
            risk_id=risk_id,
            source=source,
            data=data,
        )

    @classmethod
    def identified(
        cls,
        risk_id: str,
        source: str,
        title: str,
        severity: str,
    ):
        return cls(
            event_type=RiskEventType.IDENTIFIED,
            risk_id=risk_id,
            source=source,
            data={
                "title": title,
                "severity": severity,
            },
        )

    @classmethod
    def score_changed(
        cls,
        risk_id: str,
        source: str,
        old_score: int,
        new_score: int,
    ):
        return cls(
            event_type=RiskEventType.SCORE_CHANGED,
            risk_id=risk_id,
            source=source,
            data={
                "old_score": old_score,
                "new_score": new_score,
            },
        )

    @classmethod
    def owner_assigned(
        cls,
        risk_id: str,
        source: str,
        owner: str,
    ):
        return cls(
            event_type=RiskEventType.OWNER_ASSIGNED,
            risk_id=risk_id,
            source=source,
            data={"owner": owner},
        )

    @classmethod
    def mitigation_added(
        cls,
        risk_id: str,
        source: str,
        mitigation: str,
    ):
        return cls(
            event_type=RiskEventType.MITIGATION_ADDED,
            risk_id=risk_id,
            source=source,
            data={"mitigation": mitigation},
        )

    @classmethod
    def escalated(
        cls,
        risk_id: str,
        source: str,
        level: str,
    ):
        return cls(
            event_type=RiskEventType.ESCALATED,
            risk_id=risk_id,
            source=source,
            data={"level": level},
        )

    @classmethod
    def mitigated(
        cls,
        risk_id: str,
        source: str,
    ):
        return cls(
            event_type=RiskEventType.MITIGATED,
            risk_id=risk_id,
            source=source,
        )

    @classmethod
    def closed(
        cls,
        risk_id: str,
        source: str,
    ):
        return cls(
            event_type=RiskEventType.CLOSED,
            risk_id=risk_id,
            source=source,
        )
