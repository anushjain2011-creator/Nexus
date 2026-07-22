"""
FinanceAgent — "Can we afford this?"

Owns budget lines and spend tracking. Publishes 'budget.exceeded' when a
change would blow the budget, which other agents (e.g. RiskAgent) can
subscribe to — this is the cascade described in the design doc:
BudgetExceeded -> Finance -> Risk -> Planning.
"""

from __future__ import annotations

from typing import Any

from nexus.core.base_agent import BaseAgent
from nexus.core.registry import register_agent


@register_agent
class FinanceAgent(BaseAgent):
    name = "finance_agent"
    description = (
        "You track the project's budget: allocations, spend, and remaining "
        "funds. You flag when a proposed action would exceed budget and "
        "suggest concrete tradeoffs (cut elsewhere, delay, or reduce scope)."
    )

    def tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "add_budget_line",
                "description": "Create a new budget category with an allocation.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "allocated": {"type": "number"},
                    },
                    "required": ["category", "allocated"],
                },
            },
            {
                "name": "record_spend",
                "description": "Record spending against a budget line by category name.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["category", "amount"],
                },
            },
        ]

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        if tool_name == "add_budget_line":
            line = self.world.add_budget_line(
                category=tool_input["category"],
                allocated=tool_input["allocated"],
            )
            return {"budget_id": line.id, "status": "created"}

        if tool_name == "record_spend":
            category = tool_input["category"]
            amount = tool_input["amount"]
            line = next(
                (b for b in self.world.budget_lines.values()
                 if b.category.lower() == category.lower()),
                None,
            )
            if line is None:
                line = self.world.add_budget_line(category=category, allocated=0.0)
            line.spent += amount

            if self.world.budget_remaining() < 0 and self.bus:
                self.bus.publish(
                    "budget.exceeded",
                    remaining=self.world.budget_remaining(),
                    category=category,
                )
            return {
                "category": line.category,
                "spent": line.spent,
                "budget_remaining": self.world.budget_remaining(),
            }

        raise ValueError(f"Unknown tool: {tool_name}")
