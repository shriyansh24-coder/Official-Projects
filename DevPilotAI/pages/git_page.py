from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QSplitter,
)

from PyQt5.QtCore import Qt

from services.git_service import (
    is_git_repository,
    get_branch,
    get_status,
    get_recent_commits,
    get_diff,
    get_changed_files,
)


class GitPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_path = None
        self.changed_files = []

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel("Git Integration")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Inspect repository status, branches, changes, and recent commits."
        )
        subtitle.setObjectName("page_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.project_label = QLabel(
            "PROJECT: NO PROJECT OPEN"
        )
        self.project_label.setObjectName("project_label")

        layout.addWidget(self.project_label)

        controls = QHBoxLayout()

        self.branch_label = QLabel(
            "BRANCH: --"
        )
        self.branch_label.setObjectName("section_label")

        self.refresh_button = QPushButton(
            "↻ REFRESH GIT"
        )
        self.refresh_button.setObjectName("primary_button")
        self.refresh_button.clicked.connect(
            self.refresh_git
        )

        controls.addWidget(self.branch_label)
        controls.addStretch()
        controls.addWidget(self.refresh_button)

        layout.addLayout(controls)

        # ==================================================
        # CHANGED FILES + DIFF VIEWER
        # ==================================================

        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("git_splitter")

        # ------------------------------
        # LEFT: CHANGED FILES
        # ------------------------------

        left_panel = QWidget()

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(8)

        changed_label = QLabel("CHANGED FILES")
        changed_label.setObjectName("section_label")

        self.changed_files_list = QListWidget()

        self.changed_files_list.setStyleSheet("""
            QListWidget {
                background-color: #111821;
                color: #E6EDF3;
                border: 1px solid #1C2935;
                border-radius: 8px;
                padding: 6px;
            }

            QListWidget::item {
                color: #E6EDF3;
                background-color: transparent;
                padding: 10px;
                border-radius: 5px;
            }

            QListWidget::item:hover {
                background-color: #18232D;
            }

            QListWidget::item:selected {
                background-color: #16313A;
                color: #E6EDF3;
            }
        """)

        self.changed_files_list.itemClicked.connect(
            self.show_file_diff
        )

        left_layout.addWidget(changed_label)
        left_layout.addWidget(self.changed_files_list)

        # ------------------------------
        # RIGHT: DIFF VIEWER
        # ------------------------------

        right_panel = QWidget()

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(8)

        diff_label = QLabel("DIFF VIEWER")
        diff_label.setObjectName("section_label")

        self.diff_output = QTextEdit()
        self.diff_output.setReadOnly(True)

        self.diff_output.setStyleSheet("""
            QTextEdit {
                background-color: #0D1117;
                color: #E6EDF3;
                border: 1px solid #1C2935;
                border-radius: 8px;
                padding: 10px;
                selection-background-color: #164E63;
                selection-color: #E6EDF3;
            }
        """)

        self.diff_output.setPlainText(
            "Select a changed file to view its diff."
        )

        right_layout.addWidget(diff_label)
        right_layout.addWidget(self.diff_output)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([320, 680])

        layout.addWidget(splitter, 1)

        # ==================================================
        # WORKING TREE
        # ==================================================

        status_label = QLabel("WORKING TREE")
        status_label.setObjectName("section_label")

        layout.addWidget(status_label)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setMaximumHeight(130)
        self.status_output.setPlaceholderText(
            "Git status will appear here..."
        )

        layout.addWidget(self.status_output)

        # ==================================================
        # RECENT COMMITS
        # ==================================================

        commits_label = QLabel("RECENT COMMITS")
        commits_label.setObjectName("section_label")

        layout.addWidget(commits_label)

        self.commits_output = QTextEdit()
        self.commits_output.setReadOnly(True)
        self.commits_output.setMaximumHeight(130)
        self.commits_output.setPlaceholderText(
            "Recent commits will appear here..."
        )

        layout.addWidget(self.commits_output)

    def set_project(self, project_path):

        self.project_path = project_path

        if project_path:
            import os

            project_name = os.path.basename(
                os.path.normpath(project_path)
            )

            self.project_label.setText(
                f"PROJECT: {project_name.upper()}"
            )

            self.refresh_git()

        else:
            self.project_label.setText(
                "PROJECT: NO PROJECT OPEN"
            )

            self.branch_label.setText(
                "BRANCH: --"
            )

            self.changed_files_list.clear()
            self.diff_output.clear()
            self.status_output.clear()
            self.commits_output.clear()

    def refresh_git(self):

        if not self.project_path:
            self.branch_label.setText(
                "BRANCH: --"
            )

            self.changed_files_list.clear()

            self.diff_output.setPlainText(
                "Please open a project first."
            )

            self.status_output.setPlainText(
                "Please open a project first."
            )

            self.commits_output.clear()

            return

        if not is_git_repository(
            self.project_path
        ):
            self.branch_label.setText(
                "BRANCH: NOT A GIT REPOSITORY"
            )

            self.changed_files_list.clear()

            self.diff_output.setPlainText(
                "The selected project is not inside a Git repository."
            )

            self.status_output.setPlainText(
                "The selected project is not inside a Git repository."
            )

            self.commits_output.clear()

            return

        branch = get_branch(
            self.project_path
        )

        status = get_status(
            self.project_path
        )

        commits = get_recent_commits(
            self.project_path
        )

        self.branch_label.setText(
            f"BRANCH: {branch or '(no branch)'}"
        )

        self.status_output.setPlainText(
            status or "Working tree clean."
        )

        self.commits_output.setPlainText(
            commits or "No commits found."
        )

        self.load_changed_files()

    def load_changed_files(self):

        self.changed_files_list.clear()

        self.diff_output.setPlainText(
            "Select a changed file to view its diff."
        )

        self.changed_files = get_changed_files(
            self.project_path
        )

        if not self.changed_files:

            item = QListWidgetItem(
                "✓  No changed files"
            )

            item.setFlags(Qt.NoItemFlags)

            self.changed_files_list.addItem(
                item
            )

            return

        for file_info in self.changed_files:

            status = file_info["status"]
            path = file_info["path"]

            if "??" in status:
                icon = "○"

            elif "M" in status:
                icon = "●"

            elif "A" in status:
                icon = "+"

            elif "D" in status:
                icon = "×"

            else:
                icon = "•"

            item = QListWidgetItem(
                f"{icon}  {path}"
            )

            item.setData(
                Qt.UserRole,
                path
            )

            self.changed_files_list.addItem(
                item
            )

    def show_file_diff(self, item):

        if not self.project_path:
            return

        file_path = item.data(
            Qt.UserRole
        )

        if not file_path:
            return

        status = None

        for file_info in self.changed_files:

            if file_info["path"] == file_path:

                status = file_info["status"]
                break

        # ----------------------------------------------
        # UNTRACKED FILE
        # ----------------------------------------------

        if status and "??" in status:

            self.show_untracked_file(
                file_path
            )

            return

        # ----------------------------------------------
        # TRACKED / MODIFIED FILE
        # ----------------------------------------------

        diff = get_diff(
            self.project_path,
            file_path
        )

        if diff:

            self.diff_output.setPlainText(
                diff
            )

        else:

            self.diff_output.setPlainText(
                "No diff available for this file."
            )

    def show_untracked_file(self, file_path):

        import os

        from services.file_service import read_file

        full_path = os.path.abspath(
            os.path.join(
                self.project_path,
                file_path
            )
        )

        # A Git status entry can represent a folder.
        if not os.path.isfile(full_path):

            self.diff_output.setPlainText(
                "This Git entry is a folder or cannot be displayed as a file."
            )

            return

        content = read_file(
            full_path
        )

        if content.startswith(
            "Unable to read"
        ):

            self.diff_output.setPlainText(
                content
            )

            return

        preview = (
            "NEW FILE\n"
            + "=" * 70
            + "\n"
            + file_path
            + "\n\n"
            + content
        )

        self.diff_output.setPlainText(
            preview
        )
