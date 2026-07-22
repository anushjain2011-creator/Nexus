"""
HiringAgent — "Who should we hire?"

Responsible for workforce planning, recruiting, candidate evaluation,
interview planning, and onboarding recommendations.

The HiringAgent coordinates the TalentManager instead of talking
directly to recruiting providers.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel

from nexus.talent.manager import TalentManager


@register_agent
class HiringAgent(BaseAgent):
    name = "hiring_agent"

    description = (
        "You identify staffing needs, recruit candidates, evaluate resumes, "
        "recommend interviews, and manage the hiring process."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

        self.talent = TalentManager()

    #
    # Workforce Planning
    #

    def identify_hiring_needs(self) -> AgentResponse:

        return self.run(
            "Review the project. Determine whether additional people "
            "are needed based on workload, deadlines, required skills, "
            "budget, and project objectives."
        )

    def define_roles(self) -> AgentResponse:

        return self.run(
            "Create detailed role definitions for every recommended hire. "
            "Include responsibilities, skills, experience, qualifications, "
            "and expected outcomes."
        )

    #
    # Recruiting
    #

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
    ):

        return self.talent.search_candidates(
            role=role,
            location=location,
            skills=skills,
        )

    def import_resumes(
        self,
        resumes: list,
    ):

        return self.talent.import_resumes(resumes)

    #
    # Evaluation
    #

    def score_candidates(
        self,
        candidates,
        role: str,
    ):

        return self.talent.score_candidates(
            candidates,
            role,
        )

    def shortlist_candidates(
        self,
        candidates,
        limit: int = 5,
    ):

        return self.talent.shortlist(
            candidates,
            limit,
        )

    def recommend_candidate(
        self,
        candidates,
    ):

        return self.talent.best_candidate(candidates)

    #
    # Interviews
    #

    def generate_interview_questions(
        self,
        role: str,
    ) -> AgentResponse:

        return self.run(
            f"Generate interview questions for a {role}. "
            "Include technical questions, behavioral questions, "
            "culture-fit questions, and evaluation criteria."
        )

    def schedule_interview(
        self,
        candidate,
    ):

        return self.talent.schedule_interview(candidate)

    #
    # Offers
    #

    def recommend_offer(
        self,
        candidate,
    ) -> AgentResponse:

        return self.run(
            f"Prepare a hiring recommendation for {candidate}. "
            "Estimate salary range, onboarding priorities, "
            "potential risks, and hiring justification."
        )

    #
    # Onboarding
    #

    def onboard_candidate(
        self,
        candidate,
    ):

        return self.talent.onboard(candidate)

    #
    # Events
    #

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:

        return self.run(
            f"A hiring event occurred: '{description}'. "
            "Determine how it affects recruiting priorities, "
            "staffing levels, project delivery, and future hiring."
        )
