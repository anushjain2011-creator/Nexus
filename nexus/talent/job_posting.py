from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JobPosting:

    id: str

    title: str

    department: str

    description: str

    location: str = "Remote"

    employment_type: str = "Full-Time"

    experience_level: str = "Mid"

    salary_min: float | None = None

    salary_max: float | None = None

    currency: str = "USD"

    skills: list[str] = field(default_factory=list)

    responsibilities: list[str] = field(default_factory=list)

    qualifications: list[str] = field(default_factory=list)

    benefits: list[str] = field(default_factory=list)

    status: str = "draft"

    created_at: datetime = field(default_factory=datetime.utcnow)

    published_at: datetime | None = None

    expires_at: datetime | None = None

    applicants: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def publish(self):

        self.status = "published"
        self.published_at = datetime.utcnow()

    def close(self):

        self.status = "closed"

    def add_skill(
        self,
        skill: str,
    ):

        if skill not in self.skills:
            self.skills.append(skill)

    def add_responsibility(
        self,
        responsibility: str,
    ):

        self.responsibilities.append(
            responsibility
        )

    def add_qualification(
        self,
        qualification: str,
    ):

        self.qualifications.append(
            qualification
        )

    def add_benefit(
        self,
        benefit: str,
    ):

        self.benefits.append(
            benefit
        )

    def add_applicant(
        self,
        candidate_id: str,
    ):

        if candidate_id not in self.applicants:
            self.applicants.append(
                candidate_id
            )

    def salary_range(self):

        if (
            self.salary_min is None
            or self.salary_max is None
        ):
            return None

        return (
            self.salary_min,
            self.salary_max,
        )

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "department": self.department,
            "description": self.description,
            "location": self.location,
            "employment_type": self.employment_type,
            "experience_level": self.experience_level,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "currency": self.currency,
            "skills": self.skills,
            "responsibilities": self.responsibilities,
            "qualifications": self.qualifications,
            "benefits": self.benefits,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "applicants": self.applicants,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(**data)
