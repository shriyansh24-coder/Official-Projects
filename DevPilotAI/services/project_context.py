import os

from services.file_service import scan_project, read_file


# Files DevPilot should analyze
SUPPORTED_EXTENSIONS = {
    ".py",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".sql",
    ".json",
    ".xml",
    ".md",
}


# Prevent extremely large files from consuming API tokens
MAX_FILE_SIZE = 50000


def build_project_context(project_path):
    """
    Scan the project and build a text representation
    that can be sent to the AI.
    """

    if not project_path or not os.path.isdir(project_path):
        return "No project is currently open."

    files = scan_project(project_path)

    context_parts = []

    for relative_path in files:

        extension = os.path.splitext(relative_path)[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        full_path = os.path.join(
            project_path,
            relative_path
        )

        try:

            if os.path.getsize(full_path) > MAX_FILE_SIZE:
                context_parts.append(
                    f"\n--- FILE: {relative_path} ---\n"
                    "[File skipped because it is too large.]"
                )
                continue

            content = read_file(full_path)

            context_parts.append(
                f"\n--- FILE: {relative_path} ---\n"
                f"{content}"
            )

        except Exception as error:

            context_parts.append(
                f"\n--- FILE: {relative_path} ---\n"
                f"[Unable to read file: {error}]"
            )

    if not context_parts:
        return "The project contains no supported source files."

    return "\n".join(context_parts)