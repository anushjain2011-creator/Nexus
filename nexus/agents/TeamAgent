"""
TeamAgent — "Who should do the work?"

Responsible for assigning people to tasks, balancing workload,
tracking team capacity, identifying skill gaps, and recommending
resource changes throughout the project.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class TeamAgent(BaseAgent):
    name = "team_agent"
    description = (
        "You manage project resources, assign work, balance workloads, "
        "and ensure every task has an appropriate owner."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def assign_tasks(self) -> AgentResponse:
        """
        Assign project tasks to the most appropriate roles or team members.
        """

        return self.run(
            "Review every project task. Ensure each task has an owner. "
            "Assign work based on required skills, workload, and project "
            "priorities using assign_task."
        )

    def review_workload(self) -> AgentResponse:
        """
        Detect overloaded or underutilized team members.
        """

        return self.run(
            "Review current task assignments. Identify overloaded or "
            "underutilized team members and recommend a balanced "
            "distribution of work."
        )

    def identify_skill_gaps(self) -> AgentResponse:
        """
        Identify missing expertise needed for project success.
        """

        return self.run(
            "Review the implementation plan and current team. "
            "Identify missing skills, required expertise, certifications, "
            "or additional staffing needed to complete the project."
        )

    def recommend_hiring(self) -> AgentResponse:
        """
        Recommend new positions or contractors.
        """

        return self.run(
            "Based on the current workload and skill gaps, recommend "
            "additional hiring or contractor support where appropriate."
        )

    def optimize_resources(self) -> AgentResponse:
        """
        Improve overall resource allocation.
        """

        return self.run(
            "Optimize project resource allocation. Recommend moving people "
            "between tasks, reallocating responsibilities, or adjusting "
            "team capacity to improve delivery."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to staffing-related events.
        """

        return self.run(
            f"A team event occurred: '{description}'. "
            "Determine how this affects staffing, assignments, workloads, "
            "and project delivery. Update assignments as needed."
        )
