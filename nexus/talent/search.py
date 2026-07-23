from __future__ import annotations

from nexus.talent.candidate import Candidate

from nexus.tools.recruiting.manager import RecruitingManager


class TalentSearch:

    def __init__(
        self,
        providers: RecruitingManager,
    ):

        self.providers = providers

    def search(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        candidates: list[Candidate] = []

        for provider in self.providers.providers():

            try:

                results = provider.search_candidates(
                    role=role,
                    location=location,
                    skills=skills,
                    limit=limit,
                )

                candidates.extend(results)

            except Exception:
                continue

        return self.deduplicate(
            candidates
        )

    def search_provider(
        self,
        provider: str,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        service = self.providers.get(
            provider
        )

        if service is None:
            return []

        return service.search_candidates(
            role=role,
            location=location,
            skills=skills,
            limit=limit,
        )

    def deduplicate(
        self,
        candidates: list[Candidate],
    ) -> list[Candidate]:

        unique = {}

        for candidate in candidates:

            if candidate.email:

                key = candidate.email.lower()

            else:

                key = (
                    candidate.full_name.lower(),
                    candidate.location,
                )

            if key not in unique:

                unique[key] = candidate

        return list(
            unique.values()
        )

    def filter_skills(
        self,
        candidates: list[Candidate],
        skills: list[str],
    ) -> list[Candidate]:

        if not skills:
            return candidates

        required = {
            skill.lower()
            for skill in skills
        }

        matches = []

        for candidate in candidates:

            candidate_skills = {
                skill.lower()
                for skill in candidate.skills
            }

            if required.issubset(
                candidate_skills
            ):
                matches.append(
                    candidate
                )

        return matches

    def filter_location(
        self,
        candidates: list[Candidate],
        location: str,
    ) -> list[Candidate]:

        if not location:
            return candidates

        return [
            candidate
            for candidate in candidates
            if candidate.location
            and location.lower()
            in candidate.location.lower()
        ]

    def limit(
        self,
        candidates: list[Candidate],
        amount: int,
    ) -> list[Candidate]:

        return candidates[:amount]
