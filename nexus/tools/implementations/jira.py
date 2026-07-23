import os

from nexus.tools.jira.client import JiraClient


def execute(method: str, **kwargs):
    client = JiraClient(
        url=os.environ.get("JIRA_URL"),
        username=os.environ.get("JIRA_USERNAME"),
        token=os.environ.get("JIRA_TOKEN"),
    )
    return getattr(client, method)(**kwargs)
