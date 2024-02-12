import gitlab


class GitlabConnector(object):
    def __init__(self, url: str, token: str, project_id: str | int):
        self._url = url
        self._token = token
        self._project_id = project_id
        self._instance = gitlab.Gitlab(url=self._url, private_token=self._token)
        self._project = self._instance.projects.get(self._project_id)

    def create_merge_request(self, branch_name: str, main_branch: str, title: str, description: str):
        self._project.mergerequests.create({
            'source_branch': branch_name,
            'target_branch': main_branch,
            'title': title,
            'description': description
        })
