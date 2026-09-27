import os


IGNORED_FOLDERS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules"
}


def scan_project(project_path):
    """
    Scan a project directory and return its files/folders.
    """

    project_data = []

    for root, dirs, files in os.walk(project_path):

        # Prevent scanning unwanted folders
        dirs[:] = [
            folder for folder in dirs
            if folder not in IGNORED_FOLDERS
        ]

        relative_root = os.path.relpath(
            root,
            project_path
        )

        if relative_root == ".":
            relative_root = ""

        for file in files:

            file_path = os.path.join(
                relative_root,
                file
            )

            project_data.append(file_path)

    return sorted(project_data)


def read_file(file_path):
    """
    Read a source file safely.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return file.read()

    except UnicodeDecodeError:
        return "This file cannot be displayed as text."

    except Exception as error:
        return f"Unable to read file: {error}"