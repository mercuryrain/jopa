from issue_data import IssueData


def generate_merge_request_title(issue: IssueData) -> str:
    return f'Draft: {issue.key}: {issue.summary}'


def generate_merge_request_description(issue: IssueData, limit: int = 2000) -> str:
    return f'Issue: \n\n{issue.description[:limit]}'
