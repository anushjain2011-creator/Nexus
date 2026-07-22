from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class CommunicationEventType(str, Enum):
    MESSAGE_SENT = "communication.message_sent"
    MESSAGE_RECEIVED = "communication.message_received"

    EMAIL_SENT = "communication.email_sent"
    SLACK_SENT = "communication.slack_sent"
    NOTIFICATION_SENT = "communication.notification_sent"

    REMINDER_SENT = "communication.reminder_sent"

    MEETING_SCHEDULED = "communication.meeting_scheduled"
    MEETING_CANCELLED = "communication.meeting_cancelled"

    APPROVAL_REQUESTED = "communication.approval_requested"
    APPROVAL_RECEIVED = "communication.approval_received"
    APPROVAL_REJECTED = "communication.approval_rejected"

    STATUS_UPDATE = "communication.status_update"

    ESCALATED = "communication.escalated"


@dataclass(slots=True)
class CommunicationEvent:
    event_type: CommunicationEventType

    communication_id: str

    project_id: str | None = None

    source: str = "system"

    data: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)

    id: str = field(default_factory=lambda: str(uuid4()))

    actor: str | None = None

    correlation_id: str | None = None

    version: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.event_type.value,
            "communication_id": self.communication_id,
            "project_id": self.project_id,
            "source": self.source,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "version": self.version,
            "data": self.data,
        }

    @classmethod
    def email_sent(
        cls,
        communication_id: str,
        source: str,
        recipient: str,
        subject: str,
    ):
        return cls(
            event_type=CommunicationEventType.EMAIL_SENT,
            communication_id=communication_id,
            source=source,
            data={
                "recipient": recipient,
                "subject": subject,
            },
        )

    @classmethod
    def slack_sent(
        cls,
        communication_id: str,
        source: str,
        channel: str,
    ):
        return cls(
            event_type=CommunicationEventType.SLACK_SENT,
            communication_id=communication_id,
            source=source,
            data={
                "channel": channel,
            },
        )

    @classmethod
    def reminder_sent(
        cls,
        communication_id: str,
        source: str,
        recipient: str,
    ):
        return cls(
            event_type=CommunicationEventType.REMINDER_SENT,
            communication_id=communication_id,
            source=source,
            data={
                "recipient": recipient,
            },
        )

    @classmethod
    def meeting_scheduled(
        cls,
        communication_id: str,
        source: str,
        meeting_id: str,
        attendees: list[str],
    ):
        return cls(
            event_type=CommunicationEventType.MEETING_SCHEDULED,
            communication_id=communication_id,
            source=source,
            data={
                "meeting_id": meeting_id,
                "attendees": attendees,
            },
        )

    @classmethod
    def approval_requested(
        cls,
        communication_id: str,
        source: str,
        approver: str,
        item: str,
    ):
        return cls(
            event_type=CommunicationEventType.APPROVAL_REQUESTED,
            communication_id=communication_id,
            source=source,
            data={
                "approver": approver,
                "item": item,
            },
        )

    @classmethod
    def approval_received(
        cls,
        communication_id: str,
        source: str,
        approver: str,
    ):
        return cls(
            event_type=CommunicationEventType.APPROVAL_RECEIVED,
            communication_id=communication_id,
            source=source,
            data={
                "approver": approver,
            },
        )

    @classmethod
    def status_update(
        cls,
        communication_id: str,
        source: str,
        message: str,
    ):
        return cls(
            event_type=CommunicationEventType.STATUS_UPDATE,
            communication_id=communication_id,
            source=source,
            data={
                "message": message,
            },
        )

    @classmethod
    def escalated(
        cls,
        communication_id: str,
        source: str,
        reason: str,
    ):
        return cls(
            event_type=CommunicationEventType.ESCALATED,
            communication_id=communication_id,
            source=source,
            data={
                "reason": reason,
            },
        )
