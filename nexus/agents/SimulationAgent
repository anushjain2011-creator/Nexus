"""
SimulationAgent — "What happens if something changes?"

Responsible for modeling hypothetical scenarios before changes are
made to the real project. It evaluates schedule, budget, staffing,
risks, and dependencies to predict likely outcomes.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class SimulationAgent(BaseAgent):
    name = "simulation_agent"
    description = (
        "You simulate project changes and forecast their impact before "
        "they are applied to the real project."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def simulate_delay(
        self,
        duration: str,
    ) -> AgentResponse:
        """
        Simulate the impact of a project delay.
        """

        return self.run(
            f"Simulate delaying the project by {duration}. "
            "Determine the impact on milestones, deadlines, "
            "dependencies, budget, risks, and overall delivery."
        )

    def simulate_budget_change(
        self,
        amount: float,
    ) -> AgentResponse:
        """
        Simulate a budget increase or decrease.
        """

        return self.run(
            f"Simulate changing the project budget by {amount}. "
            "Determine how this affects staffing, scope, timeline, "
            "deliverables, and project success."
        )

    def simulate_resource_change(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Simulate staffing changes.
        """

        return self.run(
            f"Simulate this staffing change: '{description}'. "
            "Determine how it affects workload, delivery dates, "
            "resource utilization, and project risks."
        )

    def simulate_vendor_change(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Simulate vendor or supplier events.
        """

        return self.run(
            f"Simulate this vendor event: '{description}'. "
            "Evaluate impacts on procurement, schedule, costs, "
            "dependencies, and overall project execution."
        )

    def simulate_scope_change(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Simulate adding or removing project scope.
        """

        return self.run(
            f"Simulate this scope change: '{description}'. "
            "Estimate the effects on effort, milestones, staffing, "
            "budget, and delivery."
        )

    def compare_scenarios(
        self,
        first: str,
        second: str,
    ) -> AgentResponse:
        """
        Compare two possible project scenarios.
        """

        return self.run(
            f"Compare these two project scenarios.\n\n"
            f"Scenario A: {first}\n"
            f"Scenario B: {second}\n\n"
            "Determine which option has the lower risk, better cost, "
            "better schedule, and greater likelihood of success."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Simulate the long-term impact of a project event.
        """

        return self.run(
            f"A project event occurred: '{description}'. "
            "Simulate the short-term and long-term consequences if no "
            "action is taken, and recommend the best mitigation strategy."
        )
