"""
TalentManager

Central recruiting service used by the HiringAgent.
"""

from __future__ import annotations

from typing import Iterable

from nexus.talent.matching import CandidateMatcher
from nexus.talent.pipeline import HiringPipeline
from nexus.talent.scoring import CandidateScorer
from nexus.talent.search import TalentSearch

from nexus.tools.recruiting.manager import RecruitingManager


class TalentManager:

    def __init__(self):

        self.providers = RecruitingManager()

        self.search_engine = TalentSearch(
            self.providers
        )

        self.matcher = CandidateMatcher()

        self.scorer = CandidateScorer()

        self.pipeline = HiringPipeline()

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ):

        return self.search_engine.search(
            role=role,
            location=location,
            skills=skills,
            limit=limit,
        )

    def import_resumes(
        self,
        resumes: Iterable,
    ):

        candidates = []

        for resume in resumes:

            candidate = self.matcher.resume_to_candidate(
                resume
            )

            candidates.append(candidate)

        return candidates

    def match_candidates(
        self,
        candidates,
        role: str,
    ):

        return self.matcher.match(
            candidates,
            role,
        )

    def score_candidates(
        self,
        candidates,
        role: str,
    ):

        return self.scorer.score(
            candidates,
            role,
        )

    def rank_candidates(
        self,
        candidates,
    ):

        return sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

    def shortlist(
        self,
        candidates,
        limit: int = 5,
    ):

        ranked = self.rank_candidates(
            candidates
        )

        return ranked[:limit]

    def best_candidate(
        self,
        candidates,
    ):

        ranked = self.rank_candidates(
            candidates
        )

        if not ranked:
            return None

        return ranked[0]

    def schedule_interview(
        self,
        candidate,
        interviewer=None,
        when=None,
    ):

        return self.pipeline.schedule_interview(
            candidate,
            interviewer,
            when,
        )

    def move_candidate(
        self,
        candidate,
        stage: str,
    ):

        return self.pipeline.move_candidate(
            candidate,
            stage,
        )

    def candidate_status(
        self,
        candidate,
    ):

        return self.pipeline.status(
            candidate
        )

    def create_offer(
        self,
        candidate,
        salary: float,
    ):

        return self.pipeline.create_offer(
            candidate,
            salary,
        )

    def onboard(
        self,
        candidate,
    ):

        return self.pipeline.onboard(
            candidate
        )

    def register_provider(
        self,
        provider,
    ):

        self.providers.register(
            provider
        )

    def available_providers(self):

        return self.providers.providers()

    def search_and_score(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 10,
    ):

        candidates = self.search_candidates(
            role=role,
            location=location,
            skills=skills,
            limit=limit,
        )

        candidates = self.score_candidates(
            candidates,
            role,
        )

        return self.rank_candidates(
            candidates
        )
