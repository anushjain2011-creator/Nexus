import os

from nexus.tools.notion.client import NotionClient


def execute(method: str, **kwargs):
    client = NotionClient(token=os.environ.get("NOTION_TOKEN"))
    return getattr(client, method)(**kwargs)
