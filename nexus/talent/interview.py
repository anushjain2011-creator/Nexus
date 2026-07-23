from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Interview:

    id: str

    application_id: str

    candidate_id: str

    interviewer: str

    interview_type: str = "Technical"

    scheduled_for: datetime | None = None

    duration_minutes: int = 60

    location: str | None = None

    meeting_link: str | None = None

    status: str = "Scheduled"

    score: float | None = None

    recommendation: str | None = None

    strengths: list[str] = field(default_factory=list)

    concerns: list[str] = field(default_factory=list)

    feedback: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)

    completed_at: datetime | None = None

    metadata: dict = field(default_factory=dict)

    def reschedule(
        self,
        when: datetime,
    ):

        self.scheduled_for = when
        self.status = "Rescheduled"

    def cancel(self):

        self.status = "Cancelled"

    def complete(
        self,
        score: float,
        recommendation: str,
        feedback: str,
    ):

        self.score = score
        self.recommendation = recommendation
        self.feedback = feedback
        self.status = "Completed"
        self.completed_at = datetime.utcnow()

    def add_strength(
        self,
        strength: str,
    ):

        self.strengths.append(strength)

    def add_concern(
        self,
        concern: str,
    ):

        self.concerns.append(concern)

    def to_dict(self):

        return {
            "id": self.id,
            "application_id": self.application_id,
            "candidate_id": self.candidate_id,
            "interviewer": self.interviewer,
            "interview_type": self.interview_type,
            "scheduled_for": self.scheduled_for.isoformat() if self.scheduled_for else None,
            "duration_minutes": self.duration_minutes,
            "location": self.location,
            "meeting_link": self.meeting_link,
            "status": self.status,
            "score": self.score,
            "recommendation": self.recommendation,
            "strengths": self.strengths,
            "concerns": self.concerns,
            "feedback": self.feedback,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        return cls(**data)
