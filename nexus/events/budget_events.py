from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class BudgetEventType(str, Enum):
    CREATED = "budget.created"

    ALLOCATED = "budget.allocated"
    REALLOCATED = "budget.reallocated"

    SPENT = "budget.spent"
    REFUNDED = "budget.refunded"

    RESERVED = "budget.reserved"
    RELEASED = "budget.released"

    FORECAST_UPDATED = "budget.forecast_updated"

    LIMIT_REACHED = "budget.limit_reached"
    EXCEEDED = "budget.exceeded"

    CLOSED = "budget.closed"


@dataclass(slots=True)
class BudgetEvent:
    event_type: BudgetEventType

    budget_id: str

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
            "budget_id": self.budget_id,
            "project_id": self.project_id,
            "source": self.source,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def allocated(
        cls,
        budget_id: str,
        source: str,
        amount: float,
    ):
        return cls(
            event_type=BudgetEventType.ALLOCATED,
            budget_id=budget_id,
            source=source,
            data={"amount": amount},
        )

    @classmethod
    def reallocated(
        cls,
        budget_id: str,
        source: str,
        from_category: str,
        to_category: str,
        amount: float,
    ):
        return cls(
            event_type=BudgetEventType.REALLOCATED,
            budget_id=budget_id,
            source=source,
            data={
                "from": from_category,
                "to": to_category,
                "amount": amount,
            },
        )

    @classmethod
    def spent(
        cls,
        budget_id: str,
        source: str,
        amount: float,
        description: str = "",
    ):
        return cls(
            event_type=BudgetEventType.SPENT,
            budget_id=budget_id,
            source=source,
            data={
                "amount": amount,
                "description": description,
            },
        )

    @classmethod
    def refunded(
        cls,
        budget_id: str,
        source: str,
        amount: float,
    ):
        return cls(
            event_type=BudgetEventType.REFUNDED,
            budget_id=budget_id,
            source=source,
            data={"amount": amount},
        )

    @classmethod
    def exceeded(
        cls,
        budget_id: str,
        source: str,
        spent: float,
        allocated: float,
    ):
        return cls(
            event_type=BudgetEventType.EXCEEDED,
            budget_id=budget_id,
            source=source,
            data={
                "spent": spent,
                "allocated": allocated,
                "over": spent - allocated,
            },
        )

    @classmethod
    def forecast_updated(
        cls,
        budget_id: str,
        source: str,
        forecast: float,
    ):
        return cls(
            event_type=BudgetEventType.FORECAST_UPDATED,
            budget_id=budget_id,
            source=source,
            data={"forecast": forecast},
        )
