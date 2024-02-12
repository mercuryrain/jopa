from os import getenv
from dotenv import load_dotenv


class JopaConfig(object):
    def __init__(self,
                 jira_url: str,
                 jira_email: str,
                 jira_token: str,
                 main_branch: str,
                 gitlab_url: str,
                 gitlab_token: str,
                 gitlab_project_id: str):
        self.jira_url = jira_url
        self.jira_email = jira_email
        self.jira_token = jira_token
        self.main_branch = main_branch
        self.gitlab_url = gitlab_url
        self.gitlab_token = gitlab_token
        self.gitlab_project_id = gitlab_project_id


def load_config() -> JopaConfig:
    load_dotenv()
    # config = JopaConfig()
    # config.server_url = getenv('JIRA_SERVER')
    # config.email = getenv('JIRA_EMAIL')
    # config.token = getenv('JIRA_TOKEN')
    # config.main_branch = getenv('MAIN_BRANCH', 'master')
    # config.gitlab_url = getenv('GITLAB_URL')
    # config.gitlab_token = getenv('GITLAB_TOKEN')
    # config.gitlab_project_id = getenv('GITLAB_PROJECT_ID')

    return JopaConfig(
        jira_url=getenv('JIRA_SERVER'),
        jira_email=getenv('JIRA_EMAIL'),
        jira_token=getenv('JIRA_TOKEN'),
        main_branch=getenv('MAIN_BRANCH', 'master'),
        gitlab_url=getenv('GITLAB_URL'),
        gitlab_token=getenv('GITLAB_TOKEN'),
        gitlab_project_id=getenv('GITLAB_PROJECT_ID')
    )


def validate_config(config: JopaConfig):
    if not config.jira_url:
        raise ValueError('JIRA_SERVER environment variable is not set')
    if not config.jira_email:
        raise ValueError('JIRA_EMAIL environment variable is not set')
    if not config.jira_token:
        raise ValueError('JIRA_TOKEN environment variable is not set')
    if not config.gitlab_url:
        raise ValueError('GITLAB_URL environment variable is not set')
    if not config.gitlab_token:
        raise ValueError('GITLAB_TOKEN environment variable is not set')
    if not config.gitlab_project_id:
        raise ValueError('GITLAB_PROJECT_ID environment variable is not set')
