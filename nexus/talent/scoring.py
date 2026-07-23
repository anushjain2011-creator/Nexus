from __future__ import annotations

from nexus.talent.candidate import Candidate

from nexus.tools.embeddings.manager import embedding_manager


class CandidateScorer:

    def score(
        self,
        candidates: list[Candidate],
        role: str,
    ) -> list[Candidate]:

        role_vector = embedding_manager.embed(
            role
        )

        for candidate in candidates:

            candidate.score = self.score_candidate(
                candidate,
                role_vector,
            )

        return candidates

    def score_candidate(
        self,
        candidate: Candidate,
        role_vector,
    ) -> float:

        profile = self.build_profile(
            candidate
        )

        profile_vector = embedding_manager.embed(
            profile
        )

        similarity = embedding_manager.similarity(
            role_vector,
            profile_vector,
        )

        bonus = self.skill_bonus(
            candidate
        )

        experience = min(
            candidate.years_experience * 1.5,
            15,
        )

        score = (
            similarity * 75
            + bonus
            + experience
        )

        return round(
            min(score, 100),
            2,
        )

    def build_profile(
        self,
        candidate: Candidate,
    ) -> str:

        parts = [
            candidate.title or "",
            candidate.summary,
            " ".join(candidate.skills),
            " ".join(candidate.education),
            " ".join(candidate.certifications),
        ]

        return "\n".join(parts)

    def skill_bonus(
        self,
        candidate: Candidate,
    ) -> float:

        bonus = len(
            candidate.skills
        ) * 0.8

        bonus += len(
            candidate.certifications
        ) * 2

        return min(
            bonus,
            10,
        )

    def compare(
        self,
        candidate: Candidate,
        job_description: str,
    ) -> float:

        job_vector = embedding_manager.embed(
            job_description
        )

        candidate_vector = embedding_manager.embed(
            self.build_profile(candidate)
        )

        similarity = embedding_manager.similarity(
            job_vector,
            candidate_vector,
        )

        return round(
            similarity * 100,
            2,
        )

    def rank(
        self,
        candidates: list[Candidate],
    ) -> list[Candidate]:

        return sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

    def best(
        self,
        candidates: list[Candidate],
    ) -> Candidate | None:

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda candidate: candidate.score,
        )
