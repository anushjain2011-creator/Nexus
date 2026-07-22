from __future__ import annotations

import requests

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class GreenhouseProvider(RecruitingProvider):

    name = "greenhouse"

    BASE_URL = "https://harvest.greenhouse.io/v1"

    def __init__(
        self,
        api_key: str,
    ):

        self.api_key = api_key

    @property
    def auth(self):

        return (
            self.api_key,
            "",
        )

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        response = requests.get(
            f"{self.BASE_URL}/candidates",
            auth=self.auth,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        candidates = []

        for item in data[:limit]:

            candidates.append(
                Candidate(
                    id=str(item.get("id")),
                    first_name=item.get(
                        "first_name",
                        "",
                    ),
                    last_name=item.get(
                        "last_name",
                        "",
                    ),
                    email=item.get(
                        "email",
                        "",
                    ),
                    source=self.name,
                )
            )

        return candidates

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
