"""
BuilderAgent — "How do we build it?"

Responsible for turning the project plan into a concrete implementation
strategy. It generates implementation phases, technical requirements,
architecture decisions, and reacts to technical changes during the
project lifecycle.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class BuilderAgent(BaseAgent):
    name = "builder_agent"
    description = (
        "You convert project goals and plans into technical implementation "
        "plans, architecture decisions, and development tasks."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def create_implementation_plan(self) -> AgentResponse:
        """
        Create the initial implementation roadmap from the existing project
        tasks and milestones.
        """

        return self.run(
            "Review the current project plan and produce a complete "
            "implementation roadmap. Break the work into logical phases, "
            "identify dependencies, estimate implementation effort, and "
            "record architecture decisions using add_decision where "
            "appropriate."
        )

    def define_requirements(self) -> AgentResponse:
        """
        Generate technical requirements for the project.
        """

        return self.run(
            "Review the project goal and existing tasks. Produce a list of "
            "functional requirements, non-functional requirements, external "
            "dependencies, assumptions, and implementation constraints."
        )

    def review_architecture(self) -> AgentResponse:
        """
        Review whether the current architecture still supports the project.
        """

        return self.run(
            "Review the current implementation approach for scalability, "
            "maintainability, security, performance, and technical risk. "
            "Record any recommendations as project decisions."
        )

    def estimate_effort(self) -> AgentResponse:
        """
        Estimate implementation effort across the current work.
        """

        return self.run(
            "Estimate the implementation effort for every major task and "
            "milestone. Highlight work that appears underestimated or "
            "likely to delay the project."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        React to technical events affecting implementation.
        """

        return self.run(
            f"A technical event occurred: '{description}'. "
            "Determine how this impacts implementation, architecture, "
            "dependencies, and project tasks. Update the implementation "
            "plan accordingly."
        )
