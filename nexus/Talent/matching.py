from __future__ import annotations

from difflib import SequenceMatcher

from nexus.talent.candidate import Candidate
from nexus.talent.resume import Resume


class CandidateMatcher:

    def resume_to_candidate(
        self,
        resume: Resume,
    ) -> Candidate:

        parser = resume.metadata.get("parser")

        if parser is None:
            raise ValueError(
                "Resume parser not provided."
            )

        return parser.parse(resume)

    def match(
        self,
        candidates: list[Candidate],
        role: str,
    ) -> list[Candidate]:

        ranked = []

        for candidate in candidates:

            candidate.score = self.role_score(
                candidate,
                role,
            )

            ranked.append(candidate)

        ranked.sort(
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return ranked

    def role_score(
        self,
        candidate: Candidate,
        role: str,
    ) -> float:

        score = SequenceMatcher(
            None,
            candidate.title.lower(),
            role.lower(),
        ).ratio()

        return round(
            score * 100,
            2,
        )

    def match_skills(
        self,
        candidate: Candidate,
        required_skills: list[str],
    ) -> float:

        if not required_skills:
            return 100.0

        candidate_skills = {
            skill.lower()
            for skill in candidate.skills
        }

        matched = 0

        for skill in required_skills:

            if skill.lower() in candidate_skills:
                matched += 1

        return round(
            (matched / len(required_skills)) * 100,
            2,
        )

    def experience_score(
        self,
        candidate: Candidate,
        minimum_years: float,
    ) -> float:

        if minimum_years <= 0:
            return 100.0

        value = (
            candidate.years_experience
            / minimum_years
        )

        return round(
            min(value, 1.0) * 100,
            2,
        )

    def overall_score(
        self,
        candidate: Candidate,
        role: str,
        skills: list[str],
        minimum_years: float,
    ) -> float:

        role_score = self.role_score(
            candidate,
            role,
        )

        skill_score = self.match_skills(
            candidate,
            skills,
        )

        experience_score = self.experience_score(
            candidate,
            minimum_years,
        )

        score = (
            role_score * 0.35
            + skill_score * 0.45
            + experience_score * 0.20
        )

        return round(
            score,
            2,
        )

    def best_match(
        self,
        candidates: list[Candidate],
        role: str,
        skills: list[str],
        minimum_years: float,
    ) -> Candidate | None:

        if not candidates:
            return None

        for candidate in candidates:

            candidate.score = self.overall_score(
                candidate,
                role,
                skills,
                minimum_years,
            )

        return max(
            candidates,
            key=lambda candidate: candidate.score,
        )
