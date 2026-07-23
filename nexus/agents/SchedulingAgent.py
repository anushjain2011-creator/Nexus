"""
SchedulingAgent — "When should the work happen?"

Responsible for coordinating schedules, sequencing tasks,
managing milestones, resolving scheduling conflicts, and
keeping the project on track.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class SchedulingAgent(BaseAgent):
    name = "scheduling_agent"
    description = (
        "You coordinate project schedules, task sequencing, milestones, "
        "resource availability, and deadlines."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def build_schedule(self) -> AgentResponse:
        """
        Create the initial project schedule.
        """

        return self.run(
            "Review the project plan and build a realistic project "
            "schedule. Sequence tasks based on dependencies, assign "
            "target dates, and identify the critical path."
        )

    def optimize_schedule(self) -> AgentResponse:
        """
        Improve the project schedule.
        """

        return self.run(
            "Review the current project schedule and identify "
            "opportunities to shorten delivery time, improve resource "
            "utilization, and reduce scheduling conflicts."
        )

    def review_deadlines(self) -> AgentResponse:
        """
        Evaluate project deadlines.
        """

        return self.run(
            "Review all deadlines and milestones. Identify overdue tasks, "
            "upcoming deadlines, schedule risks, and recommend any "
            "necessary adjustments."
        )

    def resolve_conflicts(self) -> AgentResponse:
        """
        Resolve scheduling conflicts.
        """

        return self.run(
            "Review the project schedule for resource conflicts, "
            "dependency conflicts, overlapping work, and timeline "
            "issues. Recommend the best resolution."
        )

    def forecast_completion(self) -> AgentResponse:
        """
        Estimate project completion.
        """

        return self.run(
            "Based on the current schedule, estimate the project's "
            "completion date. Highlight any tasks or milestones that "
            "could delay delivery."
        )

    def rebalance_work(self) -> AgentResponse:
        """
        Reassign work to improve scheduling.
        """

        return self.run(
            "Review task assignments and redistribute work where "
            "appropriate to improve schedule efficiency and reduce "
            "delivery risk."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to scheduling events.
        """

        return self.run(
            f"A scheduling event occurred: '{description}'. "
            "Determine how this affects the project timeline, task "
            "dependencies, milestones, and resource availability. "
            "Recommend schedule updates."
        )
