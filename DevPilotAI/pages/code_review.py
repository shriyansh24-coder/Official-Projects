import os

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
    QSplitter
)

from PyQt5.QtCore import (
    Qt,
    QThread,
    QObject,
    pyqtSignal
)

from ai.client import ask_ai
from services.file_service import scan_project, read_file


# ==========================================================
# AI REVIEW WORKER
# ==========================================================

class ReviewWorker(QObject):

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):

        try:

            result = ask_ai(
                self.prompt
            )

            self.finished.emit(
                result
            )

        except Exception as error:

            self.error.emit(
                str(error)
            )


# ==========================================================
# CODE REVIEW PAGE
# ==========================================================

class CodeReviewPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.project_path = None

        self.thread = None
        self.worker = None

        self.setup_ui()

    # ======================================================
    # UI
    # ======================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            38,
            30,
            38,
            30
        )

        main_layout.setSpacing(14)

        # ==================================================
        # HEADER
        # ==================================================

        header = QHBoxLayout()

        title = QLabel(
            "AI Code Review"
        )

        title.setObjectName(
            "page_title"
        )

        self.project_label = QLabel(
            "PROJECT: NO PROJECT OPEN"
        )

        self.project_label.setObjectName(
            "project_label"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            self.project_label
        )

        main_layout.addLayout(
            header
        )

        # ==================================================
        # DESCRIPTION
        # ==================================================

        description = QLabel(
            "Analyze your source code for bugs, "
            "bad practices, performance issues "
            "and possible improvements."
        )

        description.setObjectName(
            "subtitle"
        )

        main_layout.addWidget(
            description
        )

        # ==================================================
        # FILE SELECTOR
        # ==================================================

        file_layout = QHBoxLayout()

        self.file_combo = QComboBox()

        self.file_combo.setMinimumHeight(
            40
        )

        self.file_combo.addItem(
            "Select a source file..."
        )

        self.review_button = QPushButton(
            "◇  REVIEW CODE"
        )

        self.review_button.setObjectName(
            "ai_button"
        )

        self.review_button.clicked.connect(
            self.run_review
        )

        file_layout.addWidget(
            self.file_combo
        )

        file_layout.addWidget(
            self.review_button
        )

        main_layout.addLayout(
            file_layout
        )

        # ==================================================
        # SPLITTER
        # ==================================================

        splitter = QSplitter(
            Qt.Horizontal
        )

        # ==================================================
        # SOURCE CODE
        # ==================================================

        code_frame = QWidget()

        code_layout = QVBoxLayout()

        code_layout.setContentsMargins(
            0,
            0,
            6,
            0
        )

        code_title = QLabel(
            "SOURCE CODE"
        )

        code_title.setObjectName(
            "section_title"
        )

        self.code_editor = QTextEdit()

        self.code_editor.setReadOnly(
            True
        )

        self.code_editor.setPlaceholderText(
            "Selected source code will appear here..."
        )

        code_layout.addWidget(
            code_title
        )

        code_layout.addWidget(
            self.code_editor
        )

        code_frame.setLayout(
            code_layout
        )

        # ==================================================
        # AI REVIEW
        # ==================================================

        review_frame = QWidget()

        review_layout = QVBoxLayout()

        review_layout.setContentsMargins(
            6,
            0,
            0,
            0
        )

        review_title = QLabel(
            "AI REVIEW"
        )

        review_title.setObjectName(
            "section_title"
        )

        self.review_output = QTextEdit()

        self.review_output.setReadOnly(
            True
        )

        self.review_output.setPlaceholderText(
            "AI code review will appear here..."
        )

        review_layout.addWidget(
            review_title
        )

        review_layout.addWidget(
            self.review_output
        )

        review_frame.setLayout(
            review_layout
        )

        # Add both sides
        splitter.addWidget(
            code_frame
        )

        splitter.addWidget(
            review_frame
        )

        splitter.setSizes([
            600,
            600
        ])

        main_layout.addWidget(
            splitter
        )

        self.setLayout(
            main_layout
        )

        # ==================================================
        # FILE SELECTION EVENT
        # ==================================================

        self.file_combo.currentIndexChanged.connect(
            self.load_selected_file
        )

    # ======================================================
    # SET PROJECT
    # ======================================================

    def set_project(self, project_path):

        self.project_path = project_path

        if not project_path:

            self.project_label.setText(
                "PROJECT: NO PROJECT OPEN"
            )

            self.file_combo.clear()

            self.file_combo.addItem(
                "Select a source file..."
            )

            return

        project_name = os.path.basename(
            os.path.normpath(
                project_path
            )
        )

        self.project_label.setText(
            f"PROJECT: {project_name.upper()}"
        )

        self.load_files()

    # ======================================================
    # LOAD FILES
    # ======================================================

    def load_files(self):

        self.file_combo.blockSignals(
            True
        )

        self.file_combo.clear()

        self.file_combo.addItem(
            "Select a source file..."
        )

        if not self.project_path:

            self.file_combo.blockSignals(
                False
            )

            return

        files = scan_project(
            self.project_path
        )

        supported_extensions = {
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
            ".sql"
        }

        for file in files:

            extension = os.path.splitext(
                file
            )[1].lower()

            if extension in supported_extensions:

                self.file_combo.addItem(
                    file
                )

        self.file_combo.blockSignals(
            False
        )

    # ======================================================
    # LOAD SELECTED FILE
    # ======================================================

    def load_selected_file(self):

        if not self.project_path:
            return

        relative_path = (
            self.file_combo.currentText()
        )

        if (
            not relative_path
            or relative_path == "Select a source file..."
        ):

            self.code_editor.clear()

            return

        full_path = os.path.join(
            self.project_path,
            relative_path
        )

        content = read_file(
            full_path
        )

        self.code_editor.setPlainText(
            content
        )

    # ======================================================
    # RUN REVIEW
    # ======================================================

    def run_review(self):

        if not self.project_path:

            self.review_output.setPlainText(
                "Please open a project first."
            )

            return

        relative_path = (
            self.file_combo.currentText()
        )

        if (
            not relative_path
            or relative_path == "Select a source file..."
        ):

            self.review_output.setPlainText(
                "Please select a source file."
            )

            return

        code = self.code_editor.toPlainText()

        if not code.strip():

            self.review_output.setPlainText(
                "The selected file is empty."
            )

            return

        # ==================================================
        # AI PROMPT
        # ==================================================

        prompt = f"""
You are DevPilot AI, an expert software
code reviewer.

Review this source code.

FILE:
{relative_path}

CODE:
{code}

Give the review using these sections:

1. OVERALL ASSESSMENT

2. BUGS

3. CODE QUALITY

4. PERFORMANCE

5. SECURITY

6. IMPROVEMENTS

7. IMPROVED CODE

Rules:

- Do not invent problems.
- Mention actual problems clearly.
- Keep the explanation practical.
- Mention relevant code sections whenever possible.
"""

        # ==================================================
        # UPDATE UI
        # ==================================================

        self.review_button.setEnabled(
            False
        )

        self.review_button.setText(
            "◈  ANALYZING..."
        )

        self.review_output.setPlainText(
            "◈ DevPilot is analyzing your code...\n\n"
            "Please wait..."
        )

        # ==================================================
        # CREATE WORKER
        # ==================================================

        self.thread = QThread()

        self.worker = ReviewWorker(
            prompt
        )

        self.worker.moveToThread(
            self.thread
        )

        # Start worker
        self.thread.started.connect(
            self.worker.run
        )

        # Worker result
        self.worker.finished.connect(
            self.review_finished
        )

        self.worker.error.connect(
            self.review_error
        )

        # Stop thread after worker finishes
        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        # Cleanup
        self.thread.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        # Start
        self.thread.start()

    # ======================================================
    # REVIEW FINISHED
    # ======================================================

    def review_finished(self, result):

        self.review_output.setPlainText(
            result
        )

        self.review_button.setEnabled(
            True
        )

        self.review_button.setText(
            "◇  REVIEW CODE"
        )

    # ======================================================
    # REVIEW ERROR
    # ======================================================

    def review_error(self, error):

        self.review_output.setPlainText(
            f"AI Error:\n\n{error}"
        )

        self.review_button.setEnabled(
            True
        )

        self.review_button.setText(
            "◇  REVIEW CODE"
        )