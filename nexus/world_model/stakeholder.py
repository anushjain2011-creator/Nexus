"""
world_model/stakeholder.py

Stakeholder model for Nexus.

Represents internal and external stakeholders involved in a
project, including communication preferences, influence,
approval authority, and engagement tracking.
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

class StakeholderRole(str, Enum):
    EXECUTIVE = "executive"
    PROJECT_MANAGER = "project_manager"
    TEAM_MEMBER = "team_member"
    CUSTOMER = "customer"
    CLIENT = "client"
    VENDOR = "vendor"
    SPONSOR = "sponsor"
    LEGAL = "legal"
    ADVISOR = "advisor"
    INVESTOR = "investor"
    OTHER = "other"


class CommunicationPreference(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    PHONE = "phone"
    SMS = "sms"
    MEETING = "meeting"
    NONE = "none"


class ApprovalLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    FINAL = "final"


# ---------------------------------------------------------
# Stakeholder
# ---------------------------------------------------------

@dataclass
class Stakeholder:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    name: str = ""

    organization: str = ""

    title: str = ""

    email: str = ""

    phone: str = ""

    role: StakeholderRole = StakeholderRole.OTHER

    communication_preference: CommunicationPreference = (
        CommunicationPreference.EMAIL
    )

    approval_level: ApprovalLevel = ApprovalLevel.NONE

    influence: int = 3          # 1–5

    interest: int = 3           # 1–5

    availability: float = 1.0   # 0.0–1.0

    active: bool = True

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    notes: List[str] = field(default_factory=list)

    responsibilities: List[str] = field(default_factory=list)

    projects: List[str] = field(default_factory=list)

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    last_contact: Optional[datetime] = None

    next_follow_up: Optional[datetime] = None

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    def add_note(self, note: str):

        self.notes.append(note)

        self.touch()

    # -----------------------------------------------------

    def add_responsibility(self, responsibility: str):

        if responsibility not in self.responsibilities:

            self.responsibilities.append(responsibility)

            self.touch()

    # -----------------------------------------------------

    def remove_responsibility(self, responsibility: str):

        if responsibility in self.responsibilities:

            self.responsibilities.remove(responsibility)

            self.touch()

    # -----------------------------------------------------

    def assign_project(self, project_id: str):

        if project_id not in self.projects:

            self.projects.append(project_id)

            self.touch()

    # -----------------------------------------------------

    def remove_project(self, project_id: str):

        if project_id in self.projects:

            self.projects.remove(project_id)

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

    def record_contact(self):

        self.last_contact = datetime.utcnow()

        self.touch()

    # -----------------------------------------------------

    def set_follow_up(self, when: datetime):

        self.next_follow_up = when

        self.touch()

    # -----------------------------------------------------

    def deactivate(self):

        self.active = False

        self.touch()

    # -----------------------------------------------------

    def activate(self):

        self.active = True

        self.touch()

    # -----------------------------------------------------

    @property
    def engagement_score(self):

        return round(
            (
                self.influence +
                self.interest
            ) / 2,
            2,
        )

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "organization": self.organization,
            "approval_level": self.approval_level.value,
            "communication": self.communication_preference.value,
            "engagement": self.engagement_score,
            "active": self.active,
            "projects": len(self.projects),
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
            f"<Stakeholder "
            f"name='{self.name}' "
            f"role='{self.role.value}' "
            f"active={self.active}>"
        )
