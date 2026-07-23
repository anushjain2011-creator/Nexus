"""
QAAgent — "Is the work complete and correct?"

Responsible for verifying deliverables, validating acceptance
criteria, identifying defects, ensuring quality standards are met,
and confirming milestones are ready to be completed.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class QAAgent(BaseAgent):
    name = "qa_agent"
    description = (
        "You verify project quality, validate deliverables, identify "
        "defects, and ensure work satisfies project requirements."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def review_deliverables(self) -> AgentResponse:
        """
        Review completed deliverables.
        """

        return self.run(
            "Review all completed deliverables. Verify they satisfy the "
            "project requirements, technical specifications, and quality "
            "expectations. Identify any deficiencies."
        )

    def validate_acceptance_criteria(self) -> AgentResponse:
        """
        Validate project acceptance criteria.
        """

        return self.run(
            "Review every completed task and milestone. Confirm whether "
            "all acceptance criteria have been satisfied and identify any "
            "remaining work."
        )

    def identify_defects(self) -> AgentResponse:
        """
        Identify quality issues.
        """

        return self.run(
            "Review the current project and identify defects, missing "
            "requirements, inconsistencies, quality concerns, or areas "
            "requiring additional testing."
        )

    def verify_milestones(self) -> AgentResponse:
        """
        Verify milestone completion.
        """

        return self.run(
            "Review each completed milestone and determine whether it is "
            "ready to be officially closed. Highlight any outstanding "
            "issues preventing completion."
        )

    def recommend_improvements(self) -> AgentResponse:
        """
        Recommend quality improvements.
        """

        return self.run(
            "Analyze the project's quality and recommend improvements to "
            "processes, testing, documentation, implementation, or "
            "deliverables."
        )

    def generate_quality_report(self) -> AgentResponse:
        """
        Generate a QA report.
        """

        return self.run(
            "Generate a project quality report summarizing completed "
            "reviews, outstanding issues, defect trends, milestone "
            "status, and overall project quality."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to quality-related events.
        """

        return self.run(
            f"A quality event occurred: '{description}'. "
            "Determine how this impacts project quality, completed work, "
            "acceptance criteria, and milestone readiness. Recommend "
            "corrective actions."
        )
