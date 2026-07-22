"""
world_model/vendor.py

Vendor model for Nexus.

Represents suppliers, contractors, and service providers.
Supports procurement, legal review, budgeting, and vendor
performance analytics.
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

class VendorStatus(str, Enum):
    PROSPECT = "prospect"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class VendorCategory(str, Enum):
    SOFTWARE = "software"
    HARDWARE = "hardware"
    CONSULTING = "consulting"
    MANUFACTURING = "manufacturing"
    MARKETING = "marketing"
    LOGISTICS = "logistics"
    LEGAL = "legal"
    FINANCE = "finance"
    OTHER = "other"


class ContractStatus(str, Enum):
    NONE = "none"
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"


# ---------------------------------------------------------
# Vendor
# ---------------------------------------------------------

@dataclass
class Vendor:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    name: str = ""

    category: VendorCategory = VendorCategory.OTHER

    status: VendorStatus = VendorStatus.PROSPECT

    contract_status: ContractStatus = ContractStatus.NONE

    contact_name: str = ""

    email: str = ""

    phone: str = ""

    website: str = ""

    address: str = ""

    account_manager: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    contract_start: Optional[datetime] = None

    contract_end: Optional[datetime] = None

    payment_terms: str = ""

    currency: str = "USD"

    estimated_cost: float = 0.0

    total_paid: float = 0.0

    outstanding_balance: float = 0.0

    lead_time_days: int = 0

    sla_days: int = 0

    quality_score: float = 5.0

    delivery_score: float = 5.0

    communication_score: float = 5.0

    reliability_score: float = 5.0

    risk_score: float = 0.0

    approved: bool = False

    preferred: bool = False

    notes: List[str] = field(default_factory=list)

    contracts: List[str] = field(default_factory=list)

    deliverables: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    @property
    def performance_score(self):

        return round(
            (
                self.quality_score +
                self.delivery_score +
                self.communication_score +
                self.reliability_score
            ) / 4,
            2,
        )

    # -----------------------------------------------------

    def approve(self):

        self.approved = True
        self.touch()

    # -----------------------------------------------------

    def revoke_approval(self):

        self.approved = False
        self.touch()

    # -----------------------------------------------------

    def make_preferred(self):

        self.preferred = True
        self.touch()

    # -----------------------------------------------------

    def remove_preferred(self):

        self.preferred = False
        self.touch()

    # -----------------------------------------------------

    def activate(self):

        self.status = VendorStatus.ACTIVE
        self.touch()

    # -----------------------------------------------------

    def suspend(self):

        self.status = VendorStatus.SUSPENDED
        self.touch()

    # -----------------------------------------------------

    def terminate(self):

        self.status = VendorStatus.TERMINATED
        self.contract_status = ContractStatus.TERMINATED
        self.touch()

    # -----------------------------------------------------

    def record_payment(self, amount: float):

        self.total_paid += amount
        self.outstanding_balance = max(
            0,
            self.outstanding_balance - amount,
        )
        self.touch()

    # -----------------------------------------------------

    def add_contract(self, contract_id: str):

        if contract_id not in self.contracts:

            self.contracts.append(contract_id)

            self.touch()

    # -----------------------------------------------------

    def add_deliverable(self, deliverable: str):

        self.deliverables.append(deliverable)

        self.touch()

    # -----------------------------------------------------

    def add_note(self, note: str):

        self.notes.append(note)

        self.touch()

    # -----------------------------------------------------

    def set_risk_score(self, score: float):

        self.risk_score = max(
            0,
            min(100, score),
        )

        self.touch()

    # -----------------------------------------------------

    def update_scores(
        self,
        quality=None,
        delivery=None,
        communication=None,
        reliability=None,
    ):

        if quality is not None:
            self.quality_score = quality

        if delivery is not None:
            self.delivery_score = delivery

        if communication is not None:
            self.communication_score = communication

        if reliability is not None:
            self.reliability_score = reliability

        self.touch()

    # -----------------------------------------------------

    def contract_expired(self):

        if self.contract_end is None:
            return False

        return datetime.utcnow() > self.contract_end

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "status": self.status.value,
            "contract": self.contract_status.value,
            "performance": self.performance_score,
            "risk": self.risk_score,
            "approved": self.approved,
            "preferred": self.preferred,
            "paid": self.total_paid,
            "balance": self.outstanding_balance,
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
            f"<Vendor "
            f"name='{self.name}' "
            f"status='{self.status.value}' "
            f"performance={self.performance_score}>"
        )
