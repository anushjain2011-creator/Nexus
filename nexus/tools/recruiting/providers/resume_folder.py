from __future__ import annotations

from pathlib import Path

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class ResumeFolderProvider(RecruitingProvider):
    """Reads plain-text resumes from a local folder — one .txt file per
    candidate. Simple local/offline alternative to the API-based providers
    (Greenhouse, Lever, etc.) for testing or small-scale use."""

    name = "resume_folder"

    def __init__(
        self,
        folder: str,
    ):

        self.folder = Path(folder)

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        candidates = []

        if not self.folder.exists():
            return candidates

        for file in sorted(self.folder.glob("*.txt")):

            text = file.read_text(encoding="utf-8")

            candidate = Candidate(
                id=file.stem,
                first_name=file.stem,
                last_name="",
                email="",
                location=location or "",
                title="",
                summary=text[:500],
                source=self.name,
            )

            if role and role.lower() not in text.lower():
                continue

            if skills and not any(
                skill.lower() in text.lower() for skill in skills
            ):
                continue

            candidates.append(candidate)

            if len(candidates) >= limit:
                break

        return candidates
