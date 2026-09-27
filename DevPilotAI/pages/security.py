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


class SecurityWorker(QObject):
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


class SecurityPage(QWidget):

    def __init__(self):
        super().__init__()

        self.project_path = None
        self.thread = None
        self.worker = None

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30, 25, 30, 25
        )

        layout.setSpacing(15)

        # ---------------- HEADER ----------------

        title = QLabel("Security Scanner")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Scan your project for potential security risks and unsafe code patterns."
        )
        subtitle.setObjectName("page_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------- PROJECT ----------------

        self.project_label = QLabel(
            "PROJECT: NO PROJECT OPEN"
        )

        self.project_label.setObjectName(
            "project_label"
        )

        layout.addWidget(
            self.project_label
        )

        # ---------------- BUTTON ----------------

        self.scan_button = QPushButton(
            "◇ SCAN PROJECT"
        )

        self.scan_button.setObjectName(
            "primary_button"
        )

        self.scan_button.clicked.connect(
            self.run_scan
        )

        layout.addWidget(
            self.scan_button
        )

        # ---------------- OUTPUT ----------------

        result_label = QLabel(
            "SECURITY REPORT"
        )

        result_label.setObjectName(
            "section_label"
        )

        layout.addWidget(
            result_label
        )

        self.security_output = QTextEdit()

        self.security_output.setReadOnly(
            True
        )

        self.security_output.setMinimumHeight(
            450
        )

        self.security_output.setPlaceholderText(
            "Security findings will appear here..."
        )

        layout.addWidget(
            self.security_output
        )

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
    # SECURITY SCAN
    # -------------------------------------------------

    def run_scan(self):

        if not self.project_path:

            self.security_output.setPlainText(
                "Please open a project first."
            )

            return

        self.scan_button.setEnabled(
            False
        )

        self.scan_button.setText(
            "◇ SCANNING PROJECT..."
        )

        self.security_output.setPlainText(
            "DevPilot is scanning your project...\n\n"
            "Please wait."
        )

        project_context = build_project_context(
            self.project_path
        )

        prompt = f"""
You are a careful software security reviewer.

Analyze the following project for potential security
vulnerabilities and unsafe coding practices.

PROJECT DATA:
==================================================

{project_context}

==================================================

Return a concise professional security report.

Use exactly these sections:

1. CRITICAL / HIGH RISK
List only serious potential security issues.

2. MEDIUM RISK
List moderate security concerns.

3. LOW RISK
List lower-impact concerns.

4. FINDINGS
For each important finding include:

- File
- Issue
- Why it matters
- Recommended fix

5. POSITIVE SECURITY PRACTICES
Mention security practices that are already present.

6. SUMMARY
Give a short summary of the project's security posture.

Important rules:

- Base findings only on the provided project data.
- Do not invent files, vulnerabilities, or functionality.
- Distinguish confirmed insecure patterns from potential concerns.
- Do not claim that a vulnerability is exploitable unless the provided code supports that conclusion.
- Look for issues such as:
  * Hardcoded API keys or secrets
  * Exposed credentials
  * Unsafe file handling
  * Command injection risks
  * SQL injection risks
  * Unsafe subprocess usage
  * Path traversal
  * Insecure deserialization
  * Weak authentication or authorization
  * Sensitive information exposed in logs
  * Unsafe network requests
  * Dangerous dynamic code execution
  * Missing input validation
  * Insecure configuration
- Do not report harmless code as a vulnerability just to create findings.
- Keep the report concise and practical.
"""

        # ---------------- THREAD ----------------

        self.thread = QThread()

        self.worker = SecurityWorker(
            prompt
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.scan_finished
        )

        self.worker.error.connect(
            self.scan_error
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

    def scan_finished(self, result):

        self.security_output.setPlainText(
            result
        )

        self.scan_button.setEnabled(
            True
        )

        self.scan_button.setText(
            "◇ SCAN PROJECT"
        )

    # -------------------------------------------------
    # ERROR
    # -------------------------------------------------

    def scan_error(self, error):

        self.security_output.setPlainText(
            "DevPilot encountered an error:\n\n"
            + str(error)
        )

        self.scan_button.setEnabled(
            True
        )

        self.scan_button.setText(
            "◇ SCAN PROJECT"
        )