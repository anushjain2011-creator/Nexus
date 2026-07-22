from __future__ import annotations

import email
import imaplib
from email.header import decode_header

from nexus.talent.candidate import Candidate
from nexus.tools.recruiting.base import RecruitingProvider


class EmailProvider(RecruitingProvider):

    name = "email"

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        mailbox: str = "INBOX",
    ):

        self.host = host
        self.username = username
        self.password = password
        self.mailbox = mailbox

    def search_candidates(
        self,
        role: str,
        location: str | None = None,
        skills: list[str] | None = None,
        limit: int = 25,
    ) -> list[Candidate]:

        candidates = []

        mail = imaplib.IMAP4_SSL(
            self.host
        )

        mail.login(
            self.username,
            self.password,
        )

        mail.select(
            self.mailbox
        )

        _, messages = mail.search(
            None,
            "ALL",
        )

        ids = messages[0].split()

        for message_id in reversed(ids):

            _, data = mail.fetch(
                message_id,
                "(RFC822)",
            )

            message = email.message_from_bytes(
                data[0][1]
            )

            sender = message.get(
                "From",
                ""
            )

            subject = self.decode(
                message.get(
                    "Subject",
                    ""
                )
            )

            for part in message.walk():

                filename = part.get_filename()

                if not filename:
                    continue

                lower = filename.lower()

                if not lower.endswith(
                    (
                        ".pdf",
                        ".doc",
                        ".docx",
                        ".txt",
                    )
                ):
                    continue

                name = sender.split("<")[0].strip()

                pieces = name.split(
                    maxsplit=1
                )

                first = pieces[0]

                last = (
                    pieces[1]
                    if len(pieces) > 1
                    else ""
                )

                candidates.append(
                    Candidate(
                        id=str(message_id.decode()),
                        first_name=first,
                        last_name=last,
                        email=self.extract_email(
                            sender
                        ),
                        summary=subject,
                        source=self.name,
                    )
                )

                if len(candidates) >= limit:

                    mail.logout()

                    return candidates

        mail.logout()

        return candidates

    def extract_email(
        self,
        sender: str,
    ) -> str:

        if "<" in sender:

            return sender.split("<")[1].replace(
                ">",
                "",
            )

        return sender

    def decode(
        self,
        value: str,
    ) -> str:

        decoded = decode_header(
            value
        )[0]

        text, encoding = decoded

        if isinstance(
            text,
            bytes,
        ):

            return text.decode(
                encoding or "utf-8",
                errors="ignore",
            )

        return text

    def publish_job(
        self,
        job,
    ):

        return None

    def update_job(
        self,
        job,
    ):

        return None

    def close_job(
        self,
        job_id: str,
    ):

        return None
