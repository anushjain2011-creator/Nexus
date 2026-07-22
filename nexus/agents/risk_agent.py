"""
RiskAgent — "What could go wrong?"

Records risks and their severity/mitigation. Also demonstrates the
event-driven cascade: if wired to an EventBus, it can subscribe to events
like 'task.blocked' or 'budget.exceeded' and automatically create a risk
entry without being explicitly asked — see `auto_subscribe()`.
"""

from __future__ import annotations

from typing import Any

from nexus.core.base_agent import BaseAgent
from nexus.core.event_bus import Event
from nexus.core.registry import register_agent


@register_agent
class RiskAgent(BaseAgent):
    name = "risk_agent"
    description = (
        "You identify risks to the project's timeline, budget, or outcome, "
        "rate their severity, and propose a mitigation. Be specific about "
        "what could go wrong and why, not generic warnings."
    )

    def tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "log_risk",
                "description": "Record a project risk.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                        "related_task_id": {"type": "string"},
                        "mitigation": {"type": "string"},
                    },
                    "required": ["description", "severity"],
                },
            }
        ]

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        if tool_name == "log_risk":
            risk = self.world.add_risk(
                description=tool_input["description"],
                severity=tool_input["severity"],
                related_task_id=tool_input.get("related_task_id"),
                mitigation=tool_input.get("mitigation"),
            )
            if self.bus:
                self.bus.publish("risk.detected", risk_id=risk.id,
                                  severity=risk.severity)
            return {"risk_id": risk.id, "status": "logged"}

        raise ValueError(f"Unknown tool: {tool_name}")

    def auto_subscribe(self) -> None:
        """Wire this agent to automatically evaluate risk when budget or
        task events fire elsewhere in the system. Call once after
        construction if you want the cascading behavior."""
        if not self.bus:
            return

        def on_budget_exceeded(event: Event) -> None:
            self.run(
                f"Budget was just exceeded: {event.payload}. "
                f"Log an appropriate risk with a mitigation suggestion."
            )

        def on_task_blocked(event: Event) -> None:
            self.run(
                f"A task was just blocked: {event.payload}. "
                f"Log an appropriate risk with a mitigation suggestion."
            )

        self.bus.subscribe("budget.exceeded", on_budget_exceeded)
        self.bus.subscribe("task.blocked", on_task_blocked)
