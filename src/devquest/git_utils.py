import subprocess


def _run_git(args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def is_git_repo(cwd: str | None = None) -> bool:
    result = _run_git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    return result.returncode == 0 and result.stdout.strip() == "true"


def has_changes(cwd: str | None = None) -> bool:
    result = _run_git(["status", "--porcelain"], cwd=cwd)
    return result.returncode == 0 and bool(result.stdout.strip())


def has_remote(name: str = "origin", cwd: str | None = None) -> bool:
    result = _run_git(["remote"], cwd=cwd)
    if result.returncode != 0:
        return False
    remotes = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return name in remotes


def current_branch(cwd: str | None = None) -> str | None:
    result = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def format_push_error(stderr: str) -> str:
    lower = stderr.lower()

    if "could not resolve hostname" in lower or "could not resolve host" in lower:
        return "Remote repository not found or unreachable."

    if "permission denied" in lower or "publickey" in lower:
        return "SSH authentication failed. Check your SSH key and remote access."

    if "authentication failed" in lower or "invalid username or password" in lower:
        return "Authentication failed. Check your credentials for the remote."

    if "no configured push destination" in lower:
        return "No remote origin found."

    if "failed to push some refs" in lower:
        return "Push rejected. Pull remote changes or check branch permissions."

    stripped = stderr.strip()
    if stripped:
        return stripped

    return "Push failed. Check your git remote and network connection."
