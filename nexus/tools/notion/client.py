from notion_client import Client


class NotionClient:

    def __init__(self, token: str):
        self.client = Client(auth=token)

    def page(self, page_id: str):
        return self.client.pages.retrieve(page_id)

    def database(self, database_id: str):
        return self.client.databases.retrieve(database_id)
