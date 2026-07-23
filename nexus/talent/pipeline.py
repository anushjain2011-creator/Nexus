from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from nexus.talent.application import Application
from nexus.talent.interview import Interview


class HiringPipeline:

    def __init__(self):

        self.applications: dict[str, Application] = {}

        self.interviews: dict[str, Interview] = {}

    def create_application(
        self,
        candidate_id: str,
        job_id: str,
        source: str = "",
    ) -> Application:

        application = Application(
            id=str(uuid4()),
            candidate_id=candidate_id,
            job_id=job_id,
            source=source,
        )

        self.applications[
            application.id
        ] = application

        return application

    def move_candidate(
        self,
        candidate,
        stage: str,
    ):

        application = self._find_application(
            candidate.id
        )

        if application is None:
            return None

        application.set_status(
            stage
        )

        return application

    def status(
        self,
        candidate,
    ):

        application = self._find_application(
            candidate.id
        )

        if application is None:
            return None

        return application.status

    def schedule_interview(
        self,
        candidate,
        interviewer=None,
        when=None,
    ) -> Interview:

        application = self._find_application(
            candidate.id
        )

        if application is None:
            raise ValueError(
                "Candidate has not applied."
            )

        interview = Interview(
            id=str(uuid4()),
            application_id=application.id,
            candidate_id=candidate.id,
            interviewer=interviewer or "Unassigned",
            scheduled_for=when or datetime.utcnow(),
        )

        self.interviews[
            interview.id
        ] = interview

        application.add_interview(
            interview.id
        )

        application.set_status(
            "Interview"
        )

        return interview

    def complete_interview(
        self,
        interview_id: str,
        score: float,
        recommendation: str,
        feedback: str,
    ):

        interview = self.interviews[
            interview_id
        ]

        interview.complete(
            score,
            recommendation,
            feedback,
        )

        return interview

    def create_offer(
        self,
        candidate,
        salary: float,
    ):

        application = self._find_application(
            candidate.id
        )

        if application is None:
            return None

        application.send_offer()

        return {
            "candidate": candidate.full_name,
            "salary": salary,
            "status": application.status,
        }

    def onboard(
        self,
        candidate,
    ):

        application = self._find_application(
            candidate.id
        )

        if application is None:
            return None

        application.mark_hired()

        return {
            "candidate": candidate.full_name,
            "status": application.status,
        }

    def reject(
        self,
        candidate,
    ):

        application = self._find_application(
            candidate.id
        )

        if application is None:
            return None

        application.mark_rejected()

        return application

    def applications_for_job(
        self,
        job_id: str,
    ):

        return [
            application
            for application in self.applications.values()
            if application.job_id == job_id
        ]

    def active_candidates(self):

        return [
            application
            for application in self.applications.values()
            if application.is_active()
        ]

    def _find_application(
        self,
        candidate_id: str,
    ):

        for application in self.applications.values():

            if application.candidate_id == candidate_id:
                return application

        return None
