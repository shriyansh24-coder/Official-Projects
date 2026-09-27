import os
import subprocess


def _run_git_at(path, *args):
    if not path:
        return ""

    try:
        result = subprocess.run(
            ["git", *args],
            cwd=path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.returncode != 0:
            return result.stderr.strip()

        return result.stdout.strip()

    except Exception as error:
        return f"Git error: {error}"


def get_repo_root(project_path):
    """Return the Git repository root containing project_path."""
    if not project_path:
        return ""

    result = _run_git_at(
        project_path,
        "rev-parse",
        "--show-toplevel",
    )

    if result.startswith("Git error:") or not result:
        return ""

    return os.path.normpath(result)


def run_git(project_path, *args):
    """Run a Git command from the repository root."""
    repo_root = get_repo_root(project_path)

    if not repo_root:
        return "No Git repository found."

    return _run_git_at(repo_root, *args)


def is_git_repository(project_path):
    return bool(get_repo_root(project_path))


def get_branch(project_path):
    return run_git(
        project_path,
        "branch",
        "--show-current",
    )


def _project_prefix(project_path, repo_root):
    """Return the selected project's path relative to repo_root."""
    project_path = os.path.abspath(project_path)
    repo_root = os.path.abspath(repo_root)

    try:
        relative = os.path.relpath(project_path, repo_root)
    except ValueError:
        return ""

    if relative == ".":
        return ""

    return relative.replace("\\", "/")


def _clean_git_path(path):
    return path.replace("\\", "/").strip()


def _is_inside_project(repo_relative_path, project_prefix):
    path = _clean_git_path(repo_relative_path)
    prefix = project_prefix.strip("/")

    if not prefix:
        return True

    return path == prefix or path.startswith(prefix + "/")


def _to_project_relative(repo_relative_path, project_prefix):
    path = _clean_git_path(repo_relative_path)
    prefix = project_prefix.replace("\\", "/").strip("/")

    if not prefix:
        return path

    if path == prefix:
        return "."

    prefix_with_slash = prefix + "/"

    if path.startswith(prefix_with_slash):
        return path[len(prefix_with_slash):]

    return path


def _to_repo_relative(project_path, file_path):
    """Convert a project-relative path into a repo-relative Git path."""
    repo_root = get_repo_root(project_path)

    if not repo_root:
        return _clean_git_path(file_path)

    project_prefix = _project_prefix(project_path, repo_root)
    clean_file = _clean_git_path(file_path).lstrip("/")

    if project_prefix:
        return project_prefix.rstrip("/") + "/" + clean_file

    return clean_file


def _parse_status_line(line):
    """Parse one line of git status --short output."""
    status = line[:2]
    path = line[3:].strip()

    # Rename/copy status can be represented as old -> new.
    if " -> " in path:
        path = path.split(" -> ")[-1]

    return status, path


def get_status(project_path):
    """Return Git status for the selected project only."""
    repo_root = get_repo_root(project_path)

    if not repo_root:
        return "No Git repository found."

    project_prefix = _project_prefix(project_path, repo_root)

    raw = _run_git_at(
        repo_root,
        "status",
        "--short",
        "--untracked-files=all",
    )

    if not raw or raw.startswith("Git error:"):
        return raw

    lines = []

    for line in raw.splitlines():
        if not line.strip():
            continue

        status, path = _parse_status_line(line)

        if not _is_inside_project(path, project_prefix):
            continue

        project_relative = _to_project_relative(
            path,
            project_prefix,
        )

        lines.append(f"{status} {project_relative}")

    return "\n".join(lines)


def get_changed_files(project_path):
    """Return changed files belonging only to the selected project."""
    repo_root = get_repo_root(project_path)

    if not repo_root:
        return []

    project_prefix = _project_prefix(project_path, repo_root)

    raw = _run_git_at(
        repo_root,
        "status",
        "--short",
        "--untracked-files=all",
    )

    if not raw or raw.startswith("Git error:"):
        return []

    changed_files = []

    for line in raw.splitlines():
        if not line.strip():
            continue

        status, path = _parse_status_line(line)

        if not _is_inside_project(path, project_prefix):
            continue

        project_relative = _to_project_relative(
            path,
            project_prefix,
        )

        full_path = os.path.join(
            project_path,
            project_relative,
        )

        # Ignore directory entries. --untracked-files=all should normally
        # give us individual files, but this keeps the UI safe.
        if os.path.isdir(full_path):
            continue

        changed_files.append({
            "status": status,
            "path": project_relative,
        })

    return changed_files


def get_diff(project_path, file_path):
    """Return staged + unstaged diff for a tracked project file."""
    repo_root = get_repo_root(project_path)

    if not repo_root:
        return "No Git repository found."

    repo_relative = _to_repo_relative(
        project_path,
        file_path,
    )

    return _run_git_at(
        repo_root,
        "diff",
        "HEAD",
        "--",
        repo_relative,
    )


def get_recent_commits(project_path, limit=5):
    return run_git(
        project_path,
        "log",
        f"-{limit}",
        "--oneline",
    )


def get_repo_summary(project_path):
    repo_root = get_repo_root(project_path)

    return {
        "root": repo_root,
        "project": os.path.abspath(project_path) if project_path else "",
    }