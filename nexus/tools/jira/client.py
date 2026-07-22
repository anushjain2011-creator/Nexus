from jira import JIRA


class JiraClient:

    def __init__(
        self,
        url: str,
        username: str,
        token: str,
    ):

        self.client = JIRA(
            server=url,
            basic_auth=(username, token),
        )

    def issue(self, key: str):
        return self.client.issue(key)

    def search(self, jql: str):
        return self.client.search_issues(jql)
