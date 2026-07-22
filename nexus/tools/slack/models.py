from dataclasses import dataclass


@dataclass(slots=True)
class SlackMessage:

    channel: str

    text: str
