import smtplib
from email.message import EmailMessage


class EmailClient:

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
    ):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send(
        self,
        to: str,
        subject: str,
        body: str,
    ):

        message = EmailMessage()

        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP_SSL(
            self.host,
            self.port,
        ) as smtp:

            smtp.login(
                self.username,
                self.password,
            )

            smtp.send_message(message)
