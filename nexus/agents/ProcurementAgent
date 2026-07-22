"""
ProcurementAgent — "What do we need to buy, and from whom?"

Responsible for sourcing vendors, evaluating suppliers, comparing
quotes, managing procurement risks, and ensuring required resources
are available for project execution.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class ProcurementAgent(BaseAgent):
    name = "procurement_agent"
    description = (
        "You manage vendor selection, purchasing decisions, supplier "
        "evaluation, and procurement planning throughout the project."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def identify_procurement_needs(self) -> AgentResponse:
        """
        Determine which goods or services must be acquired.
        """

        return self.run(
            "Review the current project plan and implementation roadmap. "
            "Identify all products, services, equipment, software, and "
            "external resources that must be procured."
        )

    def compare_vendors(self) -> AgentResponse:
        """
        Compare available vendors.
        """

        return self.run(
            "Review the project's procurement requirements. Compare "
            "potential vendors based on cost, quality, reliability, "
            "lead time, support, and overall project fit."
        )

    def recommend_supplier(self) -> AgentResponse:
        """
        Recommend the best supplier.
        """

        return self.run(
            "Based on the available procurement information, recommend "
            "the most appropriate supplier for each procurement need and "
            "justify the recommendation."
        )

    def evaluate_procurement_risks(self) -> AgentResponse:
        """
        Identify procurement-related risks.
        """

        return self.run(
            "Review all vendors and procurement plans. Identify supply "
            "chain risks, delivery risks, pricing concerns, dependency "
            "risks, and possible mitigation strategies."
        )

    def optimize_procurement(self) -> AgentResponse:
        """
        Improve procurement efficiency.
        """

        return self.run(
            "Analyze current procurement plans. Recommend opportunities "
            "to reduce costs, shorten delivery times, consolidate vendors, "
            "or improve purchasing efficiency."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to procurement events.
        """

        return self.run(
            f"A procurement event occurred: '{description}'. "
            "Determine how this affects suppliers, purchasing plans, "
            "project timelines, costs, and risks. Recommend the best "
            "course of action."
        )
