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


def list_remotes(cwd: str | None = None) -> list[tuple[str, str, str]]:
    result = _run_git(["remote", "-v"], cwd=cwd)
    if result.returncode != 0:
        return []

    remotes = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            remotes.append((parts[0], parts[1], parts[2].strip("()")))
    return remotes


def list_branches(cwd: str | None = None) -> list[dict]:
    result = _run_git(["branch", "-a", "--format=%(refname)|%(HEAD)"], cwd=cwd)
    if result.returncode != 0:
        return []

    branches = []
    for line in result.stdout.splitlines():
        if "|" not in line:
            continue

        ref, head = line.split("|", 1)
        ref = ref.strip()

        if not ref or ref.endswith("/HEAD"):
            continue

        if ref.startswith("refs/heads/"):
            name = ref.removeprefix("refs/heads/")
            remote = False
        elif ref.startswith("refs/remotes/"):
            name = ref.removeprefix("refs/remotes/")
            remote = True
        else:
            continue

        branches.append(
            {
                "name": name,
                "current": head.strip() == "*",
                "remote": remote,
            }
        )

    return branches


def branch_exists(name: str, cwd: str | None = None) -> bool:
    result = _run_git(["show-ref", "--verify", "--quiet", f"refs/heads/{name}"], cwd=cwd)
    return result.returncode == 0


def ref_exists(name: str, cwd: str | None = None) -> bool:
    result = _run_git(["rev-parse", "--verify", "--quiet", name], cwd=cwd)
    return result.returncode == 0


def checkout_branch(name: str, cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    return _run_git(["checkout", name], cwd=cwd)


def create_branch(name: str, cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    return _run_git(["checkout", "-b", name], cwd=cwd)


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
