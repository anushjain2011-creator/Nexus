"""
DataAgent — "Is our data accurate and available?"

Responsible for managing project data, maintaining reporting
pipelines, ensuring data quality, synchronizing information
between systems, and supporting analytics across the project.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class DataAgent(BaseAgent):
    name = "data_agent"
    description = (
        "You manage project data, reporting pipelines, integrations, "
        "data quality, and information availability across the project."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def audit_data(self) -> AgentResponse:
        """
        Review project data for accuracy and completeness.
        """

        return self.run(
            "Review all project data. Identify missing information, "
            "duplicate records, inconsistent values, outdated data, "
            "and recommend corrections."
        )

    def synchronize_sources(self) -> AgentResponse:
        """
        Synchronize external project systems.
        """

        return self.run(
            "Review all connected project systems and determine whether "
            "their data is synchronized. Identify conflicts, stale "
            "records, and synchronization failures."
        )

    def generate_report(self) -> AgentResponse:
        """
        Generate a project data report.
        """

        return self.run(
            "Generate a comprehensive project data report including "
            "project metrics, budgets, milestones, tasks, risks, "
            "resources, and current project status."
        )

    def validate_integrity(self) -> AgentResponse:
        """
        Validate project data integrity.
        """

        return self.run(
            "Validate the integrity of the project's data. Check for "
            "broken relationships, invalid references, missing owners, "
            "inconsistent statuses, and corrupted records."
        )

    def optimize_pipeline(self) -> AgentResponse:
        """
        Improve data collection and reporting.
        """

        return self.run(
            "Review the project's reporting and data pipelines. "
            "Recommend improvements that increase reliability, "
            "performance, automation, and maintainability."
        )

    def recommend_integrations(self) -> AgentResponse:
        """
        Recommend external integrations.
        """

        return self.run(
            "Review the project's workflows and recommend useful "
            "integrations with external systems such as GitHub, Jira, "
            "Slack, Notion, calendars, email, or other services."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to data-related events.
        """

        return self.run(
            f"A data event occurred: '{description}'. "
            "Determine how this affects project data, reporting, "
            "integrations, synchronization, and information quality. "
            "Recommend appropriate actions."
        )
