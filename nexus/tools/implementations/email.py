import os

from nexus.tools.email.client import EmailClient


def execute(method: str, **kwargs):
    client = EmailClient(
        host=os.environ.get("EMAIL_HOST"),
        port=int(os.environ.get("EMAIL_PORT", "465")),
        username=os.environ.get("EMAIL_USERNAME"),
        password=os.environ.get("EMAIL_PASSWORD"),
    )
    return getattr(client, method)(**kwargs)
