"""
world_model/decision.py

Decision model for Nexus.

Tracks human and AI decisions for explainable execution.
Every important decision made by Nexus should be logged so
future agents can understand why something happened.
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

class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"
    SUPERSEDED = "superseded"


class DecisionSource(str, Enum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"


# ---------------------------------------------------------
# Decision
# ---------------------------------------------------------

@dataclass
class Decision:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    milestone_id: Optional[str] = None

    task_id: Optional[str] = None

    title: str = ""

    description: str = ""

    source: DecisionSource = DecisionSource.AI

    status: DecisionStatus = DecisionStatus.PROPOSED

    made_by: str = ""

    approved_by: Optional[str] = None

    confidence: float = 0.0

    rationale: str = ""

    implementation_plan: str = ""

    impact: str = ""

    expected_benefit: str = ""

    tradeoffs: List[str] = field(default_factory=list)

    alternatives: List[str] = field(default_factory=list)

    assumptions: List[str] = field(default_factory=list)

    supporting_evidence: List[str] = field(default_factory=list)

    affected_tasks: List[str] = field(default_factory=list)

    affected_risks: List[str] = field(default_factory=list)

    affected_resources: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    approved_at: Optional[datetime] = None

    implemented_at: Optional[datetime] = None

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    def approve(self, approver: str):

        self.status = DecisionStatus.APPROVED

        self.approved_by = approver

        self.approved_at = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def reject(self, reason: str):

        self.status = DecisionStatus.REJECTED

        self.metadata["rejection_reason"] = reason

        self.touch()

    # -----------------------------------------------------

    def implement(self):

        self.status = DecisionStatus.IMPLEMENTED

        self.implemented_at = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def supersede(self, replacement_id: str):

        self.status = DecisionStatus.SUPERSEDED

        self.metadata["replacement"] = replacement_id

        self.touch()

    # -----------------------------------------------------

    def set_confidence(self, value: float):

        self.confidence = max(
            0.0,
            min(1.0, value),
        )

        self.touch()

    # -----------------------------------------------------

    def add_alternative(self, alternative: str):

        self.alternatives.append(alternative)

        self.touch()

    # -----------------------------------------------------

    def add_tradeoff(self, tradeoff: str):

        self.tradeoffs.append(tradeoff)

        self.touch()

    # -----------------------------------------------------

    def add_assumption(self, assumption: str):

        self.assumptions.append(assumption)

        self.touch()

    # -----------------------------------------------------

    def add_evidence(self, evidence: str):

        self.supporting_evidence.append(evidence)

        self.touch()

    # -----------------------------------------------------

    def affect_task(self, task_id: str):

        if task_id not in self.affected_tasks:

            self.affected_tasks.append(task_id)

            self.touch()

    # -----------------------------------------------------

    def affect_risk(self, risk_id: str):

        if risk_id not in self.affected_risks:

            self.affected_risks.append(risk_id)

            self.touch()

    # -----------------------------------------------------

    def affect_resource(self, resource_id: str):

        if resource_id not in self.affected_resources:

            self.affected_resources.append(resource_id)

            self.touch()

    # -----------------------------------------------------

    @property
    def is_high_confidence(self):

        return self.confidence >= 0.85

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value,
            "source": self.source.value,
            "confidence": self.confidence,
            "alternatives": len(self.alternatives),
            "tradeoffs": len(self.tradeoffs),
            "affected_tasks": len(self.affected_tasks),
            "affected_risks": len(self.affected_risks),
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
            f"<Decision "
            f"title='{self.title}' "
            f"status='{self.status.value}' "
            f"confidence={self.confidence:.2f}>"
        )
