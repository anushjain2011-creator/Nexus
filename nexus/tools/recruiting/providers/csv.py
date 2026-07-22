from __future__ import annotations

import csv
from pathlib import Path

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class CSVProvider(RecruitingProvider):

    name = "csv"

    def __init__(
        self,
        file: str,
    ):

        self.file = Path(file)

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        candidates = []

        if not self.file.exists():
            return candidates

        with self.file.open(
            newline="",
            encoding="utf-8",
        ) as csvfile:

            reader = csv.DictReader(
                csvfile
            )

            for row in reader:

                candidate = Candidate(
                    id=row.get("id", ""),
                    first_name=row.get(
                        "first_name",
                        "",
                    ),
                    last_name=row.get(
                        "last_name",
                        "",
                    ),
                    email=row.get(
                        "email",
                        "",
                    ),
                    location=row.get(
                        "location",
                        "",
                    ),
                    title=row.get(
                        "title",
                        "",
                    ),
                    summary=row.get(
                        "summary",
                        "",
                    ),
                    source=self.name,
                )

                if role:

                    text = (
                        f"{candidate.title} "
                        f"{candidate.summary}"
                    ).lower()

                    if role.lower() not in text:
                        continue

                if location:

                    if (
                        candidate.location.lower()
                        != location.lower()
                    ):
                        continue

                candidates.append(
                    candidate
                )

                if len(candidates) >= limit:
                    break

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
