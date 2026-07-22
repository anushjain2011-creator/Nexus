from __future__ import annotations

from abc import ABC, abstractmethod

from nexus.talent.candidate import Candidate


class RecruitingProvider(ABC):

    name = "provider"

    @abstractmethod
    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:
        ...

    def get_candidate(
        self,
        candidate_id: str,
    ) -> Candidate | None:

        return None

    def publish_job(
        self,
        job,
    ):

        raise NotImplementedError

    def update_job(
        self,
        job,
    ):

        raise NotImplementedError

    def close_job(
        self,
        job_id: str,
    ):

        raise NotImplementedError
