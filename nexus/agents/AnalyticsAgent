"""
AnalyticsAgent — "How are we doing?"

Responsible for monitoring project health, tracking KPIs,
measuring progress, identifying trends, and generating
performance reports.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class AnalyticsAgent(BaseAgent):
    name = "analytics_agent"
    description = (
        "You evaluate project performance by tracking progress, "
        "KPIs, milestones, risks, budgets, and overall project health."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def project_health(self) -> AgentResponse:
        """
        Evaluate overall project health.
        """

        return self.run(
            "Review the current project. Assess schedule, budget, task "
            "completion, risks, milestones, and overall health. "
            "Provide an overall health score and explain the reasoning."
        )

    def progress_report(self) -> AgentResponse:
        """
        Summarize project progress.
        """

        return self.run(
            "Generate a detailed progress report showing completed work, "
            "active work, blocked tasks, upcoming milestones, and overall "
            "completion percentage."
        )

    def track_kpis(self) -> AgentResponse:
        """
        Measure key performance indicators.
        """

        return self.run(
            "Review the project and identify the most relevant KPIs. "
            "Calculate each KPI using the available project data and "
            "highlight areas that require attention."
        )

    def forecast_completion(self) -> AgentResponse:
        """
        Predict project completion.
        """

        return self.run(
            "Analyze the current project schedule and estimate the "
            "expected completion date. Highlight any delays or schedule "
            "risks."
        )

    def identify_bottlenecks(self) -> AgentResponse:
        """
        Detect blockers affecting delivery.
        """

        return self.run(
            "Review all active tasks, dependencies, and milestones. "
            "Identify bottlenecks slowing progress and recommend actions "
            "to improve delivery."
        )

    def generate_dashboard(self) -> AgentResponse:
        """
        Prepare dashboard metrics.
        """

        return self.run(
            "Generate dashboard metrics summarizing project status, "
            "budget utilization, task completion, milestone progress, "
            "resource usage, and risk exposure."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to project events.
        """

        return self.run(
            f"A project event occurred: '{description}'. "
            "Determine how this event impacts project metrics, KPIs, "
            "health, forecasts, and overall progress."
        )
