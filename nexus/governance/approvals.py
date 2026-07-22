from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Approval:

    id: str = field(default_factory=lambda: str(uuid4()))

    action: str = ""

    requester: str = ""

    approved: bool = False

    created_at: datetime = field(default_factory=datetime.utcnow)


class ApprovalManager:

    def __init__(self):

        self._approvals = {}

    def request(
        self,
        action: str,
        requester: str,
    ):

        approval = Approval(
            action=action,
            requester=requester,
        )

        self._approvals[
            approval.id
        ] = approval

        return approval

    def approve(
        self,
        approval_id: str,
    ):

        approval = self._approvals.get(
            approval_id
        )

        if approval:

            approval.approved = True

        return approval

    def pending(self):

        return [
            approval
            for approval in self._approvals.values()
            if not approval.approved
        ]
