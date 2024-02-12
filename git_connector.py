import subprocess


class GitConnector:
    @staticmethod
    def checkout(branch: str, create: bool = False):
        subprocess.run(
            ['git', 'checkout', '-b', branch] if create else ['git', 'checkout', branch]
        )

    @staticmethod
    def pull(branch: str, origin: str = 'origin'):
        subprocess.run(['git', 'pull', origin, branch])

    @staticmethod
    def push(branch_name: str, origin: str = 'origin'):
        subprocess.run(['git', 'push', '-u', origin, branch_name])
