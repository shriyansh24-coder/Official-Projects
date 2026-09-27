from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
)

from ai.client import ask_ai


class DebugWorker(QObject):
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


class DebuggerPage(QWidget):

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

        title = QLabel("AI Debugger")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Analyze errors, identify root causes, and generate fixes."
        )
        subtitle.setObjectName("page_subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------------- LANGUAGE ----------------

        language_layout = QHBoxLayout()

        language_label = QLabel("LANGUAGE")

        self.language_box = QComboBox()
        self.language_box.addItems([
            "Python",
            "C",
            "C++",
            "Java",
            "JavaScript",
            "TypeScript",
            "Other"
        ])

        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_box)

        layout.addLayout(language_layout)

        # ---------------- CODE ----------------

        code_label = QLabel("SOURCE CODE")
        code_label.setObjectName("section_label")

        layout.addWidget(code_label)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText(
            "Paste the code that is causing the problem here..."
        )

        self.code_input.setMinimumHeight(200)

        layout.addWidget(self.code_input)

        # ---------------- ERROR ----------------

        error_label = QLabel("ERROR / EXCEPTION")
        error_label.setObjectName("section_label")

        layout.addWidget(error_label)

        self.error_input = QTextEdit()
        self.error_input.setPlaceholderText(
            "Paste the error message, traceback, or describe the problem..."
        )

        self.error_input.setMinimumHeight(120)

        layout.addWidget(self.error_input)

        # ---------------- BUTTON ----------------

        self.debug_button = QPushButton("◇ DEBUG CODE")
        self.debug_button.setObjectName("primary_button")
        self.debug_button.clicked.connect(self.run_debug)

        layout.addWidget(self.debug_button)

        # ---------------- RESULT ----------------

        result_label = QLabel("AI DEBUG ANALYSIS")
        result_label.setObjectName("section_label")

        layout.addWidget(result_label)

        self.debug_output = QTextEdit()
        self.debug_output.setReadOnly(True)
        self.debug_output.setMinimumHeight(250)

        self.debug_output.setPlaceholderText(
            "AI debugging results will appear here..."
        )

        layout.addWidget(self.debug_output)

    # -------------------------------------------------
    # PROJECT
    # -------------------------------------------------

    def set_project(self, project_path):

        self.project_path = project_path

    # -------------------------------------------------
    # DEBUG
    # -------------------------------------------------

    def run_debug(self):

        code = self.code_input.toPlainText().strip()
        error = self.error_input.toPlainText().strip()
        language = self.language_box.currentText()

        if not code:
            self.debug_output.setPlainText(
                "Please enter the source code first."
            )
            return

        if not error:
            self.debug_output.setPlainText(
                "Please enter the error message or describe the problem."
            )
            return

        prompt = f"""
You are an expert software debugging assistant.

Analyze the following {language} code and error.

SOURCE CODE:
----------------
{code}
----------------

ERROR / EXCEPTION:
----------------
{error}
----------------

Provide the response using exactly these sections:

1. ERROR EXPLANATION
Explain what the error means in simple terms.

2. ROOT CAUSE
Identify the exact reason the problem is happening.

3. PROBLEMATIC CODE
Show the part of the code responsible for the problem.

4. FIX
Explain what needs to be changed.

5. CORRECTED CODE
Provide the corrected version of the relevant code.

6. PREVENTION
Explain how the developer can avoid this problem in the future.

Keep the explanation practical and easy to understand.
Do not unnecessarily rewrite unrelated parts of the program.
"""

        self.debug_button.setEnabled(False)
        self.debug_button.setText("◇ ANALYZING...")
        self.debug_output.setPlainText(
            "DevPilot is analyzing the error...\n\n"
            "Please wait."
        )

        # ---------------- THREAD ----------------

        self.thread = QThread()
        self.worker = DebugWorker(prompt)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.debug_finished)
        self.worker.error.connect(self.debug_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------

    def debug_finished(self, result):

        self.debug_output.setPlainText(result)

        self.debug_button.setEnabled(True)
        self.debug_button.setText("◇ DEBUG CODE")

    # -------------------------------------------------
    # ERROR
    # -------------------------------------------------

    def debug_error(self, error):

        self.debug_output.setPlainText(
            "DevPilot encountered an error:\n\n"
            + str(error)
        )

        self.debug_button.setEnabled(True)
        self.debug_button.setText("◇ DEBUG CODE")