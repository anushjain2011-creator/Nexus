from __future__ import annotations

import requests

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class LeverProvider(RecruitingProvider):

    name = "lever"

    BASE_URL = "https://api.lever.co/v1"

    def __init__(
        self,
        api_key: str,
    ):

        self.api_key = api_key

    @property
    def headers(self):

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        response = requests.get(
            f"{self.BASE_URL}/candidates",
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        candidates = []

        for item in data.get(
            "data",
            [],
        )[:limit]:

            name = item.get(
                "name",
                "",
            )

            parts = name.split(
                maxsplit=1,
            )

            first = parts[0] if parts else ""

            last = (
                parts[1]
                if len(parts) > 1
                else ""
            )

            candidates.append(
                Candidate(
                    id=str(item.get("id")),
                    first_name=first,
                    last_name=last,
                    email=item.get(
                        "emails",
                        [{}],
                    )[0].get(
                        "value",
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
