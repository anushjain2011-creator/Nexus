from __future__ import annotations

import requests

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class BambooHRProvider(RecruitingProvider):

    name = "bamboohr"

    def __init__(
        self,
        company: str,
        api_key: str,
    ):

        self.company = company

        self.api_key = api_key

    @property
    def base_url(self):

        return (
            f"https://api.bamboohr.com/api/gateway.php/"
            f"{self.company}/v1"
        )

    @property
    def auth(self):

        return (
            self.api_key,
            "x",
        )

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        response = requests.get(
            f"{self.base_url}/employees/directory",
            auth=self.auth,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        candidates = []

        for item in data.get(
            "employees",
            [],
        )[:limit]:

            candidates.append(
                Candidate(
                    id=str(item.get("id")),
                    first_name=item.get(
                        "firstName",
                        "",
                    ),
                    last_name=item.get(
                        "lastName",
                        "",
                    ),
                    email=item.get(
                        "workEmail",
                        "",
                    ),
                    title=item.get(
                        "jobTitle",
                        "",
                    ),
                    location=item.get(
                        "location",
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
