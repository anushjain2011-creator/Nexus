"""
CommunicationsAgent — "Who needs to know what?"

Responsible for keeping stakeholders informed, generating project
updates, preparing executive summaries, coordinating announcements,
and ensuring communication remains clear throughout the project.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class CommunicationsAgent(BaseAgent):
    name = "communications_agent"
    description = (
        "You manage project communications by generating stakeholder "
        "updates, executive summaries, meeting notes, and important "
        "project announcements."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def stakeholder_update(self) -> AgentResponse:
        """
        Generate a stakeholder update.
        """

        return self.run(
            "Review the current project and prepare a stakeholder update. "
            "Summarize progress, completed work, upcoming milestones, "
            "current risks, budget status, and required decisions."
        )

    def executive_summary(self) -> AgentResponse:
        """
        Generate an executive summary.
        """

        return self.run(
            "Prepare an executive summary highlighting overall project "
            "health, major accomplishments, outstanding risks, budget "
            "status, timeline, and strategic recommendations."
        )

    def meeting_agenda(self) -> AgentResponse:
        """
        Create a meeting agenda.
        """

        return self.run(
            "Review the current project and generate a meeting agenda. "
            "Include project updates, blockers, risks, decisions, "
            "action items, and discussion topics."
        )

    def meeting_minutes(self) -> AgentResponse:
        """
        Generate meeting minutes.
        """

        return self.run(
            "Generate professional meeting minutes summarizing decisions "
            "made, action items assigned, outstanding questions, and "
            "follow-up tasks."
        )

    def announcement(self) -> AgentResponse:
        """
        Generate a project announcement.
        """

        return self.run(
            "Generate a project announcement describing significant "
            "project updates, milestone completions, schedule changes, "
            "or important organizational news."
        )

    def crisis_update(self) -> AgentResponse:
        """
        Generate a communication during project issues.
        """

        return self.run(
            "Review the current project risks and recent events. "
            "Prepare a clear and professional update explaining the "
            "situation, expected impact, mitigation efforts, and next "
            "steps for stakeholders."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to communication-related events.
        """

        return self.run(
            f"A project communication event occurred: '{description}'. "
            "Determine who should be informed, what information should "
            "be communicated, the appropriate communication method, and "
            "the recommended timing."
        )
