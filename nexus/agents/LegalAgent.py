"""
LegalAgent — "Are we compliant and protected?"

Responsible for reviewing contracts, identifying legal risks,
monitoring compliance requirements, and ensuring project decisions
align with applicable laws, regulations, and organizational policies.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class LegalAgent(BaseAgent):
    name = "legal_agent"
    description = (
        "You identify legal risks, review contracts, monitor compliance, "
        "and help ensure project decisions meet legal and regulatory requirements."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def review_contracts(self) -> AgentResponse:
        """
        Review contracts for legal concerns.
        """

        return self.run(
            "Review all current project contracts and agreements. "
            "Identify ambiguous language, missing clauses, liability "
            "concerns, intellectual property issues, payment terms, "
            "termination conditions, and other legal risks."
        )

    def compliance_review(self) -> AgentResponse:
        """
        Evaluate regulatory compliance.
        """

        return self.run(
            "Review the current project and determine whether there are "
            "any regulatory, licensing, privacy, accessibility, security, "
            "or industry-specific compliance requirements that must be met."
        )

    def identify_legal_risks(self) -> AgentResponse:
        """
        Identify legal exposure.
        """

        return self.run(
            "Analyze the project for legal risks including contracts, "
            "vendors, intellectual property, employment, procurement, "
            "privacy, and compliance obligations. Recommend mitigation "
            "strategies where appropriate."
        )

    def review_policy_changes(self) -> AgentResponse:
        """
        Determine whether project policies need updating.
        """

        return self.run(
            "Review current organizational policies and determine whether "
            "any should be updated based on the project's legal or "
            "regulatory requirements."
        )

    def approve_agreement(self) -> AgentResponse:
        """
        Evaluate whether an agreement is ready for approval.
        """

        return self.run(
            "Review the proposed agreement and determine whether it is "
            "ready for approval. Identify any remaining concerns or "
            "recommended revisions before execution."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to legal events affecting the project.
        """

        return self.run(
            f"A legal event occurred: '{description}'. "
            "Determine how this impacts contracts, compliance, project "
            "risk, intellectual property, vendors, or organizational "
            "policies. Recommend the appropriate response."
        )
