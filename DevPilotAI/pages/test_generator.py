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


class TestWorker(QObject):
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


class TestGeneratorPage(QWidget):

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

        title = QLabel("Test Generator")
        title.setObjectName("page_title")

        subtitle = QLabel(
            "Generate test cases and test code using AI."
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

        language_layout.addWidget(
            language_label
        )

        language_layout.addWidget(
            self.language_box
        )

        layout.addLayout(
            language_layout
        )

        # ---------------- SOURCE CODE ----------------

        code_label = QLabel(
            "SOURCE CODE"
        )

        code_label.setObjectName(
            "section_label"
        )

        layout.addWidget(
            code_label
        )

        self.code_input = QTextEdit()

        self.code_input.setPlaceholderText(
            "Paste the code you want to generate tests for..."
        )

        self.code_input.setMinimumHeight(
            220
        )

        layout.addWidget(
            self.code_input
        )

        # ---------------- BUTTON ----------------

        self.generate_button = QPushButton(
            "◇ GENERATE TESTS"
        )

        self.generate_button.setObjectName(
            "primary_button"
        )

        self.generate_button.clicked.connect(
            self.generate_tests
        )

        layout.addWidget(
            self.generate_button
        )

        # ---------------- OUTPUT ----------------

        result_label = QLabel(
            "AI GENERATED TESTS"
        )

        result_label.setObjectName(
            "section_label"
        )

        layout.addWidget(
            result_label
        )

        self.test_output = QTextEdit()

        self.test_output.setReadOnly(
            True
        )

        self.test_output.setMinimumHeight(
            300
        )

        self.test_output.setPlaceholderText(
            "Generated tests will appear here..."
        )

        layout.addWidget(
            self.test_output
        )

    # -------------------------------------------------
    # PROJECT
    # -------------------------------------------------

    def set_project(self, project_path):

        self.project_path = project_path

    # -------------------------------------------------
    # GENERATE TESTS
    # -------------------------------------------------

    def generate_tests(self):

        code = self.code_input.toPlainText().strip()

        language = (
            self.language_box.currentText()
        )

        if not code:

            self.test_output.setPlainText(
                "Please enter source code first."
            )

            return

        prompt = f"""
You are an expert software testing engineer.

Generate high-quality tests for the following
{language} source code.

SOURCE CODE:
==================================================

{code}

==================================================

Create a professional test generation report.

Use exactly these sections:

1. CODE UNDER TEST
Briefly explain what functionality is being tested.

2. TEST STRATEGY
Explain the testing approach.

3. TEST CASES
List important test cases and what each one verifies.

4. EDGE CASES
Identify unusual or boundary conditions that should be tested.

5. EXPECTED RESULTS
Explain what the expected behavior should be.

6. GENERATED TEST CODE
Provide complete runnable test code whenever possible.

7. ADDITIONAL TESTS
Suggest further tests that could improve coverage.

Important rules:

- Base the tests only on the provided source code.
- Do not invent functions that do not exist.
- Cover normal cases and edge cases.
- Keep the generated code practical.
- Clearly identify assumptions.
- Prefer readable test code.
"""

        self.generate_button.setEnabled(
            False
        )

        self.generate_button.setText(
            "◇ GENERATING TESTS..."
        )

        self.test_output.setPlainText(
            "DevPilot is generating tests...\n\n"
            "Please wait."
        )

        # ---------------- THREAD ----------------

        self.thread = QThread()

        self.worker = TestWorker(
            prompt
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.tests_finished
        )

        self.worker.error.connect(
            self.tests_error
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

    def tests_finished(self, result):

        self.test_output.setPlainText(
            result
        )

        self.generate_button.setEnabled(
            True
        )

        self.generate_button.setText(
            "◇ GENERATE TESTS"
        )

    # -------------------------------------------------
    # ERROR
    # -------------------------------------------------

    def tests_error(self, error):

        self.test_output.setPlainText(
            "DevPilot encountered an error:\n\n"
            + str(error)
        )

        self.generate_button.setEnabled(
            True
        )

        self.generate_button.setText(
            "◇ GENERATE TESTS"
        )