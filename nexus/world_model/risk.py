"""
world_model/risk.py

Risk model for Nexus.

Supports:
- Probability & impact scoring
- Automatic severity calculation
- Mitigation planning
- Ownership
- Escalation
- Event history
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

class RiskStatus(str, Enum):
    OPEN = "open"
    MONITORING = "monitoring"
    MITIGATED = "mitigated"
    CLOSED = "closed"


class RiskCategory(str, Enum):
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    LEGAL = "legal"
    SCHEDULE = "schedule"
    RESOURCE = "resource"
    SECURITY = "security"
    OPERATIONAL = "operational"
    OTHER = "other"


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------
# Risk
# ---------------------------------------------------------

@dataclass
class Risk:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    title: str = ""

    description: str = ""

    category: RiskCategory = RiskCategory.OTHER

    owner: Optional[str] = None

    status: RiskStatus = RiskStatus.OPEN

    severity: RiskSeverity = RiskSeverity.LOW

    # 1–5 scale
    probability: int = 1

    # 1–5 scale
    impact: int = 1

    mitigation: str = ""

    contingency: str = ""

    trigger: str = ""

    metadata: Dict = field(default_factory=dict)

    related_tasks: List[str] = field(default_factory=list)

    related_milestones: List[str] = field(default_factory=list)

    event_history: List[Dict] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    closed_at: Optional[datetime] = None

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    @property
    def score(self):

        return self.probability * self.impact

    # -----------------------------------------------------

    def calculate_severity(self):

        score = self.score

        if score >= 20:
            self.severity = RiskSeverity.CRITICAL

        elif score >= 12:
            self.severity = RiskSeverity.HIGH

        elif score >= 6:
            self.severity = RiskSeverity.MEDIUM

        else:
            self.severity = RiskSeverity.LOW

        self.touch()

    # -----------------------------------------------------

    def update_probability(self, value: int):

        self.probability = max(1, min(5, value))

        self.calculate_severity()

    # -----------------------------------------------------

    def update_impact(self, value: int):

        self.impact = max(1, min(5, value))

        self.calculate_severity()

    # -----------------------------------------------------

    def assign_owner(self, owner: str):

        self.owner = owner

        self.touch()

    # -----------------------------------------------------

    def set_mitigation(self, plan: str):

        self.mitigation = plan

        self.touch()

    # -----------------------------------------------------

    def set_contingency(self, plan: str):

        self.contingency = plan

        self.touch()

    # -----------------------------------------------------

    def monitor(self):

        self.status = RiskStatus.MONITORING

        self.touch()

    # -----------------------------------------------------

    def mitigate(self):

        self.status = RiskStatus.MITIGATED

        self.touch()

    # -----------------------------------------------------

    def close(self):

        self.status = RiskStatus.CLOSED

        self.closed_at = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def escalate(self):

        self.metadata["escalated"] = True

        self.event_history.append({
            "time": datetime.utcnow().isoformat(),
            "action": "escalated"
        })

        self.touch()

    # -----------------------------------------------------

    def add_related_task(self, task_id: str):

        if task_id not in self.related_tasks:

            self.related_tasks.append(task_id)

            self.touch()

    # -----------------------------------------------------

    def add_related_milestone(self, milestone_id: str):

        if milestone_id not in self.related_milestones:

            self.related_milestones.append(milestone_id)

            self.touch()

    # -----------------------------------------------------

    def record_event(
        self,
        action: str,
        details: Optional[Dict] = None,
    ):

        self.event_history.append({
            "time": datetime.utcnow().isoformat(),
            "action": action,
            "details": details or {},
        })

        self.touch()

    # -----------------------------------------------------

    def is_high_priority(self):

        return self.severity in (
            RiskSeverity.HIGH,
            RiskSeverity.CRITICAL,
        )

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "title": self.title,
            "category": self.category.value,
            "status": self.status.value,
            "severity": self.severity.value,
            "score": self.score,
            "owner": self.owner,
            "tasks": len(self.related_tasks),
            "milestones": len(self.related_milestones),
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
            f"<Risk "
            f"title='{self.title}' "
            f"severity='{self.severity.value}' "
            f"score={self.score}>"
        )
