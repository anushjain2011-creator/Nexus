import os

from nexus.tools.github.client import GitHubClient


def execute(method: str, **kwargs):
    client = GitHubClient(token=os.environ.get("GITHUB_TOKEN"))
    return getattr(client, method)(**kwargs)
