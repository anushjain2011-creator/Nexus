"""
NegotiationAgent — "How do we reach the best agreement?"

Responsible for negotiating with vendors, partners, clients,
and stakeholders. It recommends negotiation strategies,
evaluates offers, and helps reach agreements that align
with project objectives.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class NegotiationAgent(BaseAgent):
    name = "negotiation_agent"
    description = (
        "You develop negotiation strategies, evaluate offers, resolve "
        "conflicts, and help achieve agreements that benefit the project."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def prepare_negotiation(self) -> AgentResponse:
        """
        Prepare for an upcoming negotiation.
        """

        return self.run(
            "Review the current project objectives, procurement needs, "
            "budget constraints, and stakeholder priorities. Develop a "
            "negotiation strategy including objectives, acceptable "
            "trade-offs, risks, and fallback positions."
        )

    def evaluate_offer(self) -> AgentResponse:
        """
        Evaluate a proposed offer or agreement.
        """

        return self.run(
            "Review the proposed offer or agreement. Identify strengths, "
            "weaknesses, financial impact, legal considerations, risks, "
            "and recommended negotiation points."
        )

    def recommend_terms(self) -> AgentResponse:
        """
        Recommend contract or agreement terms.
        """

        return self.run(
            "Recommend favorable contract terms, pricing structures, "
            "payment schedules, delivery expectations, service-level "
            "agreements, and termination conditions."
        )

    def resolve_conflict(self) -> AgentResponse:
        """
        Recommend a conflict resolution strategy.
        """

        return self.run(
            "Review the current disagreement between parties. Recommend "
            "a negotiation strategy that resolves the conflict while "
            "protecting project objectives and maintaining relationships."
        )

    def assess_leverage(self) -> AgentResponse:
        """
        Identify negotiation leverage.
        """

        return self.run(
            "Analyze the current negotiation and identify sources of "
            "leverage, bargaining power, risks, concessions, and "
            "opportunities to improve the outcome."
        )

    def summarize_agreement(self) -> AgentResponse:
        """
        Summarize the negotiated agreement.
        """

        return self.run(
            "Summarize the negotiated agreement, highlighting key terms, "
            "responsibilities, deadlines, financial commitments, and any "
            "remaining open issues."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to negotiation-related events.
        """

        return self.run(
            f"A negotiation event occurred: '{description}'. "
            "Determine how this affects ongoing negotiations, vendor "
            "relationships, contracts, or partnerships. Recommend the "
            "best negotiation strategy moving forward."
        )
