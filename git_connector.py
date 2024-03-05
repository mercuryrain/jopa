import subprocess


class GitConnector:

    @staticmethod
    def add_all() -> None:
        subprocess.run(['git', 'add', '-A'])

    @staticmethod
    def checkout(branch: str, create: bool = False) -> None:
        subprocess.run(
            ['git', 'checkout', '-b', branch] if create else ['git', 'checkout', branch]
        )

    @staticmethod
    def pull(branch: str, origin: str = 'origin') -> None:
        subprocess.run(['git', 'pull', origin, branch])

    @staticmethod
    def push(branch_name: str, origin: str = 'origin') -> None:
        subprocess.run(['git', 'push', '-u', origin, branch_name])

    @staticmethod
    def commit(message: str, no_verify: bool = False) -> None:
        subprocess.run(['git', 'commit', '-m', message] + (['--no-verify'] if no_verify else []))

    @staticmethod
    def get_current_git_branch() -> str:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        current_branch = result.stdout.strip()
        return current_branch

    @staticmethod
    def fetch_all() -> None:
        subprocess.run(['git', 'fetch', '--all'])

    @staticmethod
    def reset(branch: str, hard: bool = False) -> None:
        subprocess.run(['git', 'reset', '--' + ('hard' if hard else 'soft'), branch])

    @staticmethod
    def merge(branch: str, no_edit: bool = True):
        subprocess.run(['git', 'merge', branch] + (['--no-edit'] if no_edit else []))

    @staticmethod
    def has_changes() -> bool:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return bool(result.stdout.strip())

    @staticmethod
    def stash() -> None:
        subprocess.run(['git', 'stash'])

    @staticmethod
    def stash_pop() -> None:
        subprocess.run(['git', 'stash', 'pop'])
