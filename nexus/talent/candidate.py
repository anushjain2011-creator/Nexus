from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Candidate:

    id: str

    first_name: str
    last_name: str

    email: str | None = None
    phone: str | None = None
    location: str | None = None

    title: str | None = None

    years_experience: float = 0.0

    skills: list[str] = field(default_factory=list)

    education: list[str] = field(default_factory=list)

    certifications: list[str] = field(default_factory=list)

    experience: list[dict[str, Any]] = field(default_factory=list)

    links: dict[str, str] = field(default_factory=dict)

    resume_path: str | None = None

    summary: str = ""

    source: str = ""

    status: str = "new"

    score: float = 0.0

    applied_at: datetime | None = None

    notes: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:

        return f"{self.first_name} {self.last_name}"

    def add_skill(
        self,
        skill: str,
    ):

        if skill not in self.skills:
            self.skills.append(skill)

    def add_note(
        self,
        note: str,
    ):

        self.notes.append(note)

    def add_tag(
        self,
        tag: str,
    ):

        if tag not in self.tags:
            self.tags.append(tag)

    def set_score(
        self,
        score: float,
    ):

        self.score = round(score, 2)

    def update_status(
        self,
        status: str,
    ):

        self.status = status

    def has_skill(
        self,
        skill: str,
    ) -> bool:

        return any(
            value.lower() == skill.lower()
            for value in self.skills
        )

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "title": self.title,
            "years_experience": self.years_experience,
            "skills": self.skills,
            "education": self.education,
            "certifications": self.certifications,
            "experience": self.experience,
            "links": self.links,
            "resume_path": self.resume_path,
            "summary": self.summary,
            "source": self.source,
            "status": self.status,
            "score": self.score,
            "notes": self.notes,
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(**data)
