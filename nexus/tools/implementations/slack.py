import os

from nexus.tools.slack.client import SlackClient


def execute(method: str, **kwargs):
    client = SlackClient(token=os.environ.get("SLACK_TOKEN"))
    return getattr(client, method)(**kwargs)
