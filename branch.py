import re
from issue_data import IssueData


def generate_branch_name(issue: IssueData, limit: int = 50) -> str:
    branch_name = issue.key + '-' + re.sub(r'[^a-zA-Z0-9]', '_', issue.summary).lower()
    return branch_name[:limit]