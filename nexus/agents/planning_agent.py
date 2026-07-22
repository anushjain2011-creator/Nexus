"""Planning agent implementation."""

from __future__ import annotations

from typing import Any, Mapping

from nexus.core.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    def __init__(self, name: str = 'planning') -> None:
        super().__init__(name)

    def act(self, context: Mapping[str, Any]) -> dict[str, Any]:
        goals = context.get('goals', ['complete task'])
        return {
            'role': 'planning',
            'plan': f"Draft plan for goals: {goals}",
        }
