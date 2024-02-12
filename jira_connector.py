from jira import JIRA
from issue_data import IssueData


class JIRAConnector(object):
    def __init__(self, server: str, basic_auth: tuple[str, str]):
        self._server = server
        self._basic_auth = basic_auth
        self._jira = JIRA(server=self._server, basic_auth=self._basic_auth)

    def get_issue(self, key: str) -> IssueData:
        issue = self._jira.issue(key)
        return IssueData(
            key=key,
            summary=issue.fields.summary,
            description=issue.fields.description
        )
