from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)

from ai.client import ask_ai
from services.project_context import build_project_context


class AnalysisWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            result = ask_ai(self.prompt)
            self.finished.emit(result)
        except Exception as error:
            self.error.emit(str(error))


class ProjectAnalysisPage(QWidget):

    def __init__(self):
        super().__init__()

        self.project_path = None
        self.thread = None
        self.worker = None

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        # ---------------- HEADER ----------------

        title = QLabel("Project Analysis")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Analyze the structure, quality, risks, and architecture of your project."
        )
        subtitle.setObjectName("page_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------- PROJECT ----------------

        self.project_label = QLabel(
            "PROJECT: NO PROJECT OPEN"
        )

        self.project_label.setObjectName("project_label")

        layout.addWidget(self.project_label)

        # ---------------- BUTTON ----------------

        self.analyze_button = QPushButton(
            "◇ RUN PROJECT ANALYSIS"
        )

        self.analyze_button.setObjectName("primary_button")

        self.analyze_button.clicked.connect(
            self.run_analysis
        )

        layout.addWidget(self.analyze_button)

        # ---------------- OUTPUT ----------------

        result_label = QLabel(
            "AI PROJECT REPORT"
        )

        result_label.setObjectName("section_label")

        layout.addWidget(result_label)

        self.analysis_output = QTextEdit()

        self.analysis_output.setReadOnly(True)

        self.analysis_output.setMinimumHeight(450)

        self.analysis_output.setPlaceholderText(
            "Your project analysis will appear here..."
        )

        layout.addWidget(self.analysis_output)

    # -------------------------------------------------
    # PROJECT
    # -------------------------------------------------

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

        else:

            self.project_label.setText(
                "PROJECT: NO PROJECT OPEN"
            )

    # -------------------------------------------------
    # ANALYSIS
    # -------------------------------------------------

    def run_analysis(self):

        if not self.project_path:

            self.analysis_output.setPlainText(
                "Please open a project first."
            )

            return

        self.analyze_button.setEnabled(False)

        self.analyze_button.setText(
            "◇ ANALYZING PROJECT..."
        )

        self.analysis_output.setPlainText(
            "DevPilot is analyzing your project...\n\n"
            "This may take some time depending on the "
            "size of the project."
        )

        # Build project context

        project_context = build_project_context(
            self.project_path
        )

        prompt = f"""
You are an expert software architect and code reviewer.

Analyze the following software project.

PROJECT DATA:
==================================================

{project_context}

==================================================

Create a professional project analysis report.

Use exactly these sections:

1. PROJECT OVERVIEW
Explain what the project appears to do.

2. PROJECT STRUCTURE
Explain the important folders and files and how they appear to be organized.

3. ARCHITECTURE
Explain how the major components interact.

4. CODE QUALITY
Identify strengths and areas that could be improved.

5. POTENTIAL BUGS
Identify suspicious patterns, possible bugs, or fragile areas.

6. PERFORMANCE
Identify possible performance issues or inefficient approaches.

7. SECURITY
Identify potential security risks or unsafe practices.

8. MAINTAINABILITY
Explain how easy the project should be to maintain and extend.

9. RECOMMENDATIONS
Provide practical improvements in priority order.

10. FINAL SUMMARY
Give a concise summary of the current state of the project.

Important rules:

- Base your analysis only on the provided project data.
- Do not invent files or functionality.
- Clearly distinguish confirmed issues from potential concerns.
- Keep explanations practical and understandable.
- Do not rewrite the entire project.
"""

        # ---------------- THREAD ----------------

        self.thread = QThread()

        self.worker = AnalysisWorker(prompt)

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.analysis_finished
        )

        self.worker.error.connect(
            self.analysis_error
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------

    def analysis_finished(self, result):

        self.analysis_output.setPlainText(
            result
        )

        self.analyze_button.setEnabled(
            True
        )

        self.analyze_button.setText(
            "◇ RUN PROJECT ANALYSIS"
        )

    # -------------------------------------------------
    # ERROR
    # -------------------------------------------------

    def analysis_error(self, error):

        self.analysis_output.setPlainText(
            "DevPilot encountered an error:\n\n"
            + str(error)
        )

        self.analyze_button.setEnabled(
            True
        )

        self.analyze_button.setText(
            "◇ RUN PROJECT ANALYSIS"
        )