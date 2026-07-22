"""
RetrospectiveAgent — "What did we learn?"

Responsible for analyzing completed milestones and projects,
capturing lessons learned, identifying successes and failures,
and recommending improvements for future work.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class RetrospectiveAgent(BaseAgent):
    name = "retrospective_agent"
    description = (
        "You analyze completed work, identify lessons learned, evaluate "
        "project performance, and recommend improvements for future "
        "projects."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def analyze_project(self) -> AgentResponse:
        """
        Perform a complete project retrospective.
        """

        return self.run(
            "Review the completed project. Analyze objectives, "
            "deliverables, milestones, budget, schedule, risks, "
            "team performance, and stakeholder satisfaction. "
            "Summarize the overall outcome."
        )

    def identify_successes(self) -> AgentResponse:
        """
        Highlight what went well.
        """

        return self.run(
            "Review the completed project and identify the practices, "
            "decisions, processes, and accomplishments that contributed "
            "to project success."
        )

    def identify_failures(self) -> AgentResponse:
        """
        Identify problems encountered.
        """

        return self.run(
            "Review the completed project and identify mistakes, "
            "missed opportunities, process failures, communication "
            "issues, technical problems, and planning shortcomings."
        )

    def recommend_improvements(self) -> AgentResponse:
        """
        Recommend improvements for future projects.
        """

        return self.run(
            "Based on the retrospective findings, recommend practical "
            "improvements to planning, execution, communication, "
            "resource management, budgeting, quality assurance, and "
            "overall project management."
        )

    def document_lessons_learned(self) -> AgentResponse:
        """
        Capture lessons learned.
        """

        return self.run(
            "Create a lessons learned report that captures key insights, "
            "best practices, recurring issues, successful strategies, "
            "and recommendations for future projects."
        )

    def evaluate_team_performance(self) -> AgentResponse:
        """
        Evaluate overall team performance.
        """

        return self.run(
            "Evaluate how the project team performed throughout the "
            "project. Identify strengths, collaboration successes, "
            "resource challenges, and opportunities for improvement."
        )

    def close_project(self) -> AgentResponse:
        """
        Determine whether the project is ready for closure.
        """

        return self.run(
            "Review the project and determine whether it is ready to "
            "be formally closed. Verify that deliverables are complete, "
            "outstanding risks have been addressed, documentation is "
            "finished, and lessons learned have been captured."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to retrospective events.
        """

        return self.run(
            f"A retrospective event occurred: '{description}'. "
            "Determine what can be learned from this event, how future "
            "projects can avoid similar issues, and whether project "
            "processes should be updated."
        )
