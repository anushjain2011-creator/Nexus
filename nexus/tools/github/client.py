from github import Github


class GitHubClient:

    def __init__(self, token: str):
        self.client = Github(token)

    def repository(self, name: str):
        return self.client.get_repo(name)

    def issues(self, repo: str):
        return self.repository(repo).get_issues()

    def create_issue(
        self,
        repo: str,
        title: str,
        body: str = "",
    ):
        return self.repository(repo).create_issue(
            title=title,
            body=body,
        )
