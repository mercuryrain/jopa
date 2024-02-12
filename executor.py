from builtins import print

from config import JopaConfig
from jira_connector import JIRAConnector
from git_connector import GitConnector
from branch import generate_branch_name
from issue_data import IssueData
from gitlab_connector import GitlabConnector
from merge_reqiest import generate_merge_request_title, generate_merge_request_description


class Executor(object):
    def __init__(self, config: JopaConfig):
        self._config = config
        self._jira_connector = JIRAConnector(
            server=self._config.jira_url,
            basic_auth=(self._config.jira_email, self._config.jira_token)
        )
        self._git = GitConnector()
        self._gitlab = GitlabConnector(
            self._config.gitlab_url,
            self._config.gitlab_token,
            self._config.gitlab_project_id
        )
        self._issues = {}

    def execute(
            self,
            issue_id: str,
            max_branch_name_length: int = 50,
            main_branch: str | None = None
    ):
        issue = self._get_issue(issue_id)
        print(f'Loaded issue {issue_id}: {issue.summary}')
        branch_name = generate_branch_name(issue, max_branch_name_length)
        print(f'Branch name: {branch_name}')

        master = main_branch or self._config.main_branch

        print(f'Switching to {master} branch...')
        self._git.checkout(main_branch or self._config.main_branch)
        print(f'Pulling {master} branch...')
        self._git.pull(main_branch or self._config.main_branch)
        print(f'Creating branch {branch_name}...')
        self._git.checkout(branch_name, True)
        print(f'Pushing branch {branch_name}...')
        self._git.push(branch_name)

        print(f'Branch {branch_name} created and pushed')
        print(f'Creating merge request...')

        self._gitlab.create_merge_request(
            branch_name=branch_name,
            main_branch=master,
            title=generate_merge_request_title(issue),
            description=generate_merge_request_description(issue)
        )

    def _get_issue(self, issue_id: str) -> IssueData:
        if issue_id not in self._issues:
            self._load_issue(issue_id)
        return self._issues[issue_id]

    def _load_issue(self, issue_id: str):
        self._issues[issue_id] = self._jira_connector.get_issue(issue_id)
