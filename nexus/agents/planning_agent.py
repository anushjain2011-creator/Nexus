"""
PlanningAgent — "What should happen next?"

Takes a goal (or a change to the project, like a delay) and creates or
updates tasks in the WorldModel. This is the agent used in the Intent
Engine step: goal in, task graph out.
"""

from __future__ import annotations

from typing import Any

from nexus.core.base_agent import BaseAgent
from nexus.core.registry import register_agent


@register_agent
class PlanningAgent(BaseAgent):
    name = "planning_agent"
    description = (
        "You create and adjust the project's task plan. Given a goal or a "
        "change in circumstances, you decide what tasks are needed, in what "
        "order, and with what dependencies. You are decisive and concrete — "
        "you produce real tasks, not vague advice."
    )

    def tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "create_task",
                "description": "Add a new task to the project plan.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "owner": {"type": "string",
                                  "description": "Role or person responsible, e.g. 'Hardware Engineer'"},
                        "deadline": {"type": "string",
                                     "description": "ISO date or relative like 'Day 10'"},
                        "cost": {"type": "number"},
                        "depends_on": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Task IDs this task depends on",
                        },
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "update_task_status",
                "description": "Change the status of an existing task.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": ["todo", "in_progress", "blocked", "done"],
                        },
                    },
                    "required": ["task_id", "status"],
                },
            },
        ]

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        if tool_name == "create_task":
            task = self.world.add_task(
                title=tool_input["title"],
                owner=tool_input.get("owner"),
                deadline=tool_input.get("deadline"),
                cost=tool_input.get("cost", 0.0),
                depends_on=tool_input.get("depends_on", []),
            )
            if self.bus:
                self.bus.publish("task.created", task_id=task.id, title=task.title)
            return {"task_id": task.id, "status": "created"}

        if tool_name == "update_task_status":
            task = self.world.update_task(
                tool_input["task_id"], status=tool_input["status"]
            )
            if self.bus:
                self.bus.publish(f"task.{task.status}", task_id=task.id,
                                  title=task.title)
            return {"task_id": task.id, "status": task.status}

        raise ValueError(f"Unknown tool: {tool_name}")
