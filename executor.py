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

    def easy_push(self, issue_id: str, no_verify: bool = False, origin: str = 'origin'):
        issue = self._get_issue(issue_id)
        print(f'Loaded issue {issue_id}: {issue.summary}')

        branch_name = self._git.get_current_git_branch()
        print(f'Current branch: {branch_name}')

        print('Adding all files...')
        self._git.add_all()

        print('Committing...')
        self._git.commit(f'{issue.key}: {issue.summary}', no_verify=no_verify)
        print('Pushing...')
        self._git.push(branch_name=branch_name, origin=origin)

    def merge_to_remote(self, branch_name: str, origin: str = 'origin'):
        has_changes = self._git.has_changes()

        if has_changes:
            print('You have uncommitted changes. Please commit or stash them before merging')
            return

        current_branch_name = self._git.get_current_git_branch()
        print(f'Current branch: {current_branch_name}')

        print('Fetching...')
        self._git.fetch_all()

        print('Checking out...')
        self._git.checkout(branch_name)

        print('Resetting...')

        self._git.reset(f"{origin}/{branch_name}", hard=True)

        print('Merging...')
        self._git.merge(current_branch_name, no_edit=True)

        print('Pushing...')
        self._git.push(branch_name=branch_name, origin=origin)

        self._git.checkout(current_branch_name)


    def execute(
            self,
            issue_id: str,
            max_branch_name_length: int = 100,
            main_branch: str | None = None,
            remove_source_branch: bool = True,
            squash: bool = True
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
        print('Creating merge request...')

        self._gitlab.create_merge_request(
            branch_name=branch_name,
            main_branch=master,
            title=generate_merge_request_title(issue),
            description=generate_merge_request_description(issue),
            remove_source_branch=remove_source_branch,
            squash=squash
        )

    def _get_issue(self, issue_id: str) -> IssueData:
        if issue_id not in self._issues:
            self._load_issue(issue_id)
        return self._issues[issue_id]

    def _load_issue(self, issue_id: str):
        self._issues[issue_id] = self._jira_connector.get_issue(issue_id)
