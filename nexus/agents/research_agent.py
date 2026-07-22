"""
ResearchAgent — "What already exists?"

Summarizes findings and attaches them to the WorldModel's knowledge log,
optionally linked to a specific task. In this MVP it reasons from the
instruction text you give it (e.g. text you've already pulled from a
search); wiring in a live web-search tool is a natural next step.
"""

from __future__ import annotations

from typing import Any

from nexus.core.base_agent import BaseAgent
from nexus.core.registry import register_agent


@register_agent
class ResearchAgent(BaseAgent):
    name = "research_agent"
    description = (
        "You analyze information relevant to the project and record concise, "
        "decision-useful findings. Prefer a few sharp findings over a long "
        "list — each finding should be something the team could act on."
    )

    def tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "record_finding",
                "description": "Save a research finding to the shared knowledge base.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "note": {"type": "string"},
                        "source": {"type": "string"},
                        "related_task_id": {"type": "string"},
                    },
                    "required": ["note"],
                },
            }
        ]

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        if tool_name == "record_finding":
            self.world.add_knowledge(
                note=tool_input["note"],
                source=tool_input.get("source"),
                related_task_id=tool_input.get("related_task_id"),
            )
            if self.bus:
                self.bus.publish("research.found", note=tool_input["note"])
            return {"status": "recorded"}

        raise ValueError(f"Unknown tool: {tool_name}")
