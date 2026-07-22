"""Finance agent implementation."""

from __future__ import annotations

from typing import Any, Mapping

from nexus.core.base_agent import BaseAgent

class FinanceAgent(BaseAgent):
    def __init__(self, name: str = 'finance') -> None:
        super().__init__(name)

    def act(self, context: Mapping[str, Any]) -> dict[str, Any]:
        budget = context.get('budget', 'unknown')
        return {
            'role': 'finance',
            'analysis': f"Finance review completed for budget: {budget}",
        }
