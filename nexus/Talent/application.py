from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Application:

    id: str

    candidate_id: str

    job_id: str

    status: str = "Applied"

    source: str = ""

    applied_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    recruiter: str | None = None

    interview_ids: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)

    rating: float = 0.0

    offer_sent: bool = False

    hired: bool = False

    rejected: bool = False

    metadata: dict = field(default_factory=dict)

    def set_status(
        self,
        status: str,
    ):

        self.status = status
        self.updated_at = datetime.utcnow()

    def add_note(
        self,
        note: str,
    ):

        self.notes.append(note)
        self.updated_at = datetime.utcnow()

    def add_interview(
        self,
        interview_id: str,
    ):

        if interview_id not in self.interview_ids:
            self.interview_ids.append(interview_id)

        self.updated_at = datetime.utcnow()

    def set_rating(
        self,
        rating: float,
    ):

        self.rating = rating
        self.updated_at = datetime.utcnow()

    def send_offer(self):

        self.offer_sent = True
        self.status = "Offer"
        self.updated_at = datetime.utcnow()

    def mark_hired(self):

        self.hired = True
        self.rejected = False
        self.status = "Hired"
        self.updated_at = datetime.utcnow()

    def mark_rejected(self):

        self.rejected = True
        self.hired = False
        self.status = "Rejected"
        self.updated_at = datetime.utcnow()

    def is_active(self):

        return self.status not in {
            "Rejected",
            "Hired",
        }

    def to_dict(self):

        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "status": self.status,
            "source": self.source,
            "applied_at": self.applied_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "recruiter": self.recruiter,
            "interview_ids": self.interview_ids,
            "notes": self.notes,
            "rating": self.rating,
            "offer_sent": self.offer_sent,
            "hired": self.hired,
            "rejected": self.rejected,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(**data)
