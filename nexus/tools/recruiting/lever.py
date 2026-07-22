from __future__ import annotations

from nexus.talent.candidate import Candidate

from .base import RecruitingProvider


class LeverProvider(
    RecruitingProvider,
):

    name = "lever"

    def __init__(
        self,
        api_key: str | None = None,
    ):

        self.api_key = api_key

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        return []

    def publish_job(
        self,
        job,
    ):

        return None

    def update_job(
        self,
        job,
    ):

        return None

    def close_job(
        self,
        job_id: str,
    ):

        return None
