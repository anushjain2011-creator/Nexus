"""
world_model/resource.py

Resource model for Nexus.

Represents any consumable or allocatable project resource:
- Team members
- Equipment
- Cloud infrastructure
- Facilities
- Budgets
- AI Agents
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

class ResourceType(str, Enum):
    PERSON = "person"
    EQUIPMENT = "equipment"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    FACILITY = "facility"
    VEHICLE = "vehicle"
    CLOUD = "cloud"
    DATA = "data"
    AI_AGENT = "ai_agent"
    OTHER = "other"


class ResourceStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    RETIRED = "retired"


# ---------------------------------------------------------
# Resource
# ---------------------------------------------------------

@dataclass
class Resource:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    name: str = ""

    description: str = ""

    type: ResourceType = ResourceType.OTHER

    status: ResourceStatus = ResourceStatus.AVAILABLE

    owner: Optional[str] = None

    location: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    available_from: Optional[datetime] = None

    available_until: Optional[datetime] = None

    capacity: float = 1.0

    allocated: float = 0.0

    hourly_cost: float = 0.0

    daily_cost: float = 0.0

    utilization: float = 0.0

    skills: List[str] = field(default_factory=list)

    certifications: List[str] = field(default_factory=list)

    assigned_tasks: List[str] = field(default_factory=list)

    assigned_projects: List[str] = field(default_factory=list)

    maintenance_log: List[Dict] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    @property
    def available_capacity(self):

        return max(0.0, self.capacity - self.allocated)

    # -----------------------------------------------------

    @property
    def is_available(self):

        return (
            self.status == ResourceStatus.AVAILABLE
            and self.available_capacity > 0
        )

    # -----------------------------------------------------

    def allocate(self, amount: float):

        self.allocated = min(
            self.capacity,
            self.allocated + amount,
        )

        self.utilization = round(
            (self.allocated / self.capacity) * 100,
            2,
        )

        if self.allocated > 0:
            self.status = ResourceStatus.IN_USE

        self.touch()

    # -----------------------------------------------------

    def release(self, amount: float):

        self.allocated = max(
            0.0,
            self.allocated - amount,
        )

        self.utilization = round(
            (self.allocated / self.capacity) * 100,
            2,
        )

        if self.allocated == 0:
            self.status = ResourceStatus.AVAILABLE

        self.touch()

    # -----------------------------------------------------

    def reserve(self):

        self.status = ResourceStatus.RESERVED

        self.touch()

    # -----------------------------------------------------

    def start_maintenance(self, reason: str):

        self.status = ResourceStatus.MAINTENANCE

        self.maintenance_log.append({
            "started": datetime.utcnow().isoformat(),
            "reason": reason,
        })

        self.touch()

    # -----------------------------------------------------

    def finish_maintenance(self):

        self.status = ResourceStatus.AVAILABLE

        if self.maintenance_log:

            self.maintenance_log[-1]["completed"] = (
                datetime.utcnow().isoformat()
            )

        self.touch()

    # -----------------------------------------------------

    def retire(self):

        self.status = ResourceStatus.RETIRED

        self.touch()

    # -----------------------------------------------------

    def assign_task(self, task_id: str):

        if task_id not in self.assigned_tasks:

            self.assigned_tasks.append(task_id)

            self.touch()

    # -----------------------------------------------------

    def remove_task(self, task_id: str):

        if task_id in self.assigned_tasks:

            self.assigned_tasks.remove(task_id)

            self.touch()

    # -----------------------------------------------------

    def assign_project(self, project_id: str):

        if project_id not in self.assigned_projects:

            self.assigned_projects.append(project_id)

            self.touch()

    # -----------------------------------------------------

    def add_skill(self, skill: str):

        if skill not in self.skills:

            self.skills.append(skill)

            self.touch()

    # -----------------------------------------------------

    def add_certification(self, cert: str):

        if cert not in self.certifications:

            self.certifications.append(cert)

            self.touch()

    # -----------------------------------------------------

    def estimated_cost(self, hours: float):

        return round(
            hours * self.hourly_cost,
            2,
        )

    # -----------------------------------------------------

    def daily_estimated_cost(self, days: float):

        return round(
            days * self.daily_cost,
            2,
        )

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "status": self.status.value,
            "capacity": self.capacity,
            "allocated": self.allocated,
            "available_capacity": self.available_capacity,
            "utilization": self.utilization,
            "tasks": len(self.assigned_tasks),
            "projects": len(self.assigned_projects),
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
            f"<Resource "
            f"name='{self.name}' "
            f"type='{self.type.value}' "
            f"status='{self.status.value}'>"
        )
