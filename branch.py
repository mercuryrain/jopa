import re
from issue_data import IssueData


def generate_branch_name(issue: IssueData, limit: int = 50) -> str:
    # Replace all non-alphanumeric characters with underscores
    branch_name = (issue.key
                   + '-'
                   + re.sub(r'[^a-zA-Z0-9]', '_', issue.summary).lower())

    # Remove multiple underscores
    branch_name = re.sub(r'_+', '_', branch_name)

    # Remove trailing underscores and limit the length
    return branch_name[:limit].strip('_')
