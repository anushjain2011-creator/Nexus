"""
world_model/budget.py

Budget model for Nexus.

Tracks:
- Budget categories
- Allocations
- Spending
- Remaining funds
- Burn rate
- Forecasts
- Variance
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from uuid import uuid4


# ---------------------------------------------------------
# Enums
# ---------------------------------------------------------

class BudgetStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    EXCEEDED = "exceeded"
    CLOSED = "closed"


# ---------------------------------------------------------
# Budget
# ---------------------------------------------------------

@dataclass
class Budget:

    id: str = field(default_factory=lambda: str(uuid4()))

    project_id: Optional[str] = None

    category: str = "General"

    currency: str = "USD"

    allocated: float = 0.0

    spent: float = 0.0

    committed: float = 0.0

    reserved: float = 0.0

    forecast: float = 0.0

    status: BudgetStatus = BudgetStatus.PLANNED

    owner: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    notes: str = ""

    metadata: Dict = field(default_factory=dict)

    # -----------------------------------------------------

    def touch(self):

        self.updated_at = datetime.utcnow()

    # -----------------------------------------------------

    @property
    def remaining(self):

        return self.allocated - self.spent

    # -----------------------------------------------------

    @property
    def available(self):

        return self.allocated - (
            self.spent +
            self.committed +
            self.reserved
        )

    # -----------------------------------------------------

    @property
    def utilization(self):

        if self.allocated == 0:
            return 0

        return round(
            (self.spent / self.allocated) * 100,
            2,
        )

    # -----------------------------------------------------

    def allocate(self, amount: float):

        self.allocated += amount

        self.status = BudgetStatus.ACTIVE

        self.touch()

    # -----------------------------------------------------

    def spend(self, amount: float):

        self.spent += amount

        if self.spent > self.allocated:

            self.status = BudgetStatus.EXCEEDED

        self.touch()

    # -----------------------------------------------------

    def commit(self, amount: float):

        self.committed += amount

        self.touch()

    # -----------------------------------------------------

    def reserve(self, amount: float):

        self.reserved += amount

        self.touch()

    # -----------------------------------------------------

    def release_commitment(self, amount: float):

        self.committed = max(
            0,
            self.committed - amount,
        )

        self.touch()

    # -----------------------------------------------------

    def release_reservation(self, amount: float):

        self.reserved = max(
            0,
            self.reserved - amount,
        )

        self.touch()

    # -----------------------------------------------------

    def close(self):

        self.status = BudgetStatus.CLOSED

        self.touch()

    # -----------------------------------------------------

    def forecast_total(self, expected_future_spend: float):

        self.forecast = (
            self.spent +
            expected_future_spend
        )

        self.touch()

    # -----------------------------------------------------

    def variance(self):

        return round(
            self.forecast - self.allocated,
            2,
        )

    # -----------------------------------------------------

    def burn_rate(
        self,
        elapsed_days: int,
    ):

        if elapsed_days <= 0:

            return 0

        return round(
            self.spent / elapsed_days,
            2,
        )

    # -----------------------------------------------------

    def days_remaining(
        self,
        elapsed_days: int,
    ):

        burn = self.burn_rate(elapsed_days)

        if burn == 0:

            return None

        return round(
            self.remaining / burn,
            1,
        )

    # -----------------------------------------------------

    def is_over_budget(self):

        return self.spent > self.allocated

    # -----------------------------------------------------

    def summary(self):

        return {
            "id": self.id,
            "category": self.category,
            "allocated": self.allocated,
            "spent": self.spent,
            "remaining": self.remaining,
            "available": self.available,
            "forecast": self.forecast,
            "variance": self.variance(),
            "utilization": self.utilization,
            "status": self.status.value,
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
            f"<Budget "
            f"category='{self.category}' "
            f"spent={self.spent:.2f} "
            f"allocated={self.allocated:.2f}>"
        )
