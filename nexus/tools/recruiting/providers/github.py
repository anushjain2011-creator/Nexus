from __future__ import annotations

import os
from typing import Any

import requests

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class GitHubProvider(RecruitingProvider):

    name = "github"

    BASE_URL = "https://api.github.com"

    def __init__(
        self,
        token: str | None = None,
    ):

        self.token = token or os.getenv(
            "GITHUB_TOKEN"
        )

    @property
    def headers(self):

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Nexus",
        }

        if self.token:
            headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        return headers

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        query = self.build_query(
            role,
            location,
            skills,
        )

        response = requests.get(
            f"{self.BASE_URL}/search/users",
            headers=self.headers,
            params={
                "q": query,
                "per_page": min(limit, 100),
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        candidates = []

        for item in data.get(
            "items",
            [],
        ):

            profile = self.user(
                item["login"]
            )

            if profile is None:
                continue

            candidates.append(
                self.to_candidate(
                    profile
                )
            )

        return candidates

    def user(
        self,
        username: str,
    ) -> dict[str, Any] | None:

        response = requests.get(
            f"{self.BASE_URL}/users/{username}",
            headers=self.headers,
            timeout=30,
        )

        if response.status_code != 200:
            return None

        return response.json()

    def build_query(
        self,
        role: str,
        location: str | None,
        skills: list[str] | None,
    ) -> str:

        parts = [role]

        if location:
            parts.append(
                f"location:{location}"
            )

        if skills:
            parts.extend(skills)

        return " ".join(parts)

    def to_candidate(
        self,
        profile: dict,
    ) -> Candidate:

        name = profile.get(
            "name"
        ) or profile["login"]

        split = name.split(
            maxsplit=1
        )

        first = split[0]

        last = (
            split[1]
            if len(split) > 1
            else ""
        )

        return Candidate(
            id=str(profile["id"]),
            first_name=first,
            last_name=last,
            email=profile.get("email"),
            location=profile.get("location"),
            title=profile.get("bio"),
            summary=profile.get("bio") or "",
            source=self.name,
            links={
                "github": profile[
                    "html_url"
                ]
            },
        )

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
