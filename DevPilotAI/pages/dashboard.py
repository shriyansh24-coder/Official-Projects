from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QLineEdit,
    QTextEdit
)

from PyQt5.QtCore import QThread , QObject , pyqtSignal

from ai.rag import ProjectAI

class DashboardAIWorker(QObject):

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, project_ai, question):
        super().__init__()
        self.project_ai = project_ai
        self.question = question

    def run(self):
        try:
            result = self.project_ai.ask(
                self.question
            )
            self.finished.emit(result)

        except Exception as error:
            self.error.emit(str(error))

class Dashboard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.project_ai = ProjectAI()
        self.project_path = None

        self.setup_ui()

    # ==================================================

    def setup_ui(self):

        content_layout = QVBoxLayout()

        content_layout.setContentsMargins(
            38, 30, 38, 30
        )

        content_layout.setSpacing(12)

        # ================= HEADER =================

        header = QHBoxLayout()

        title = QLabel("Command Center")
        title.setObjectName("page_title")

        status = QLabel("●  SYSTEM ONLINE")
        status.setObjectName("system_status")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(status)

        content_layout.addLayout(header)

        # ================= WELCOME =================

        welcome = QLabel(
            "Good evening, developer."
        )

        welcome.setObjectName("welcome")

        subtitle = QLabel(
            "Your AI development command center."
        )

        subtitle.setObjectName("subtitle")

        content_layout.addSpacing(8)

        content_layout.addWidget(welcome)
        content_layout.addWidget(subtitle)

        content_layout.addSpacing(10)

        # ================= STATISTICS =================

        stats = QHBoxLayout()
        stats.setSpacing(12)

        stats.addWidget(
            self.create_stat_card("PROJECTS", "00")
        )

        stats.addWidget(
            self.create_stat_card("AI REVIEWS", "00")
        )

        stats.addWidget(
            self.create_stat_card("ISSUES FOUND", "00")
        )

        stats.addWidget(
            self.create_stat_card("CODE QUALITY", "--")
        )

        content_layout.addLayout(stats)

        content_layout.addSpacing(10)

        # ================= AI CORE =================

        section = QLabel("AI CORE")
        section.setObjectName("section_title")

        content_layout.addWidget(section)

        ai_frame = QFrame()
        ai_frame.setObjectName("ai_frame")

        ai_layout = QVBoxLayout()

        ai_layout.setContentsMargins(
            22, 20, 22, 20
        )

        ai_layout.setSpacing(12)

        ai_header_layout = QHBoxLayout()

        ai_header = QLabel(
            "◈  DEVPILOT INTELLIGENCE"
        )

        ai_header.setObjectName(
            "ai_header"
        )

        self.project_label = QLabel(
            "PROJECT: NO PROJECT OPEN"
        )

        self.project_label.setObjectName(
            "project_label"
        )

        ai_header_layout.addWidget(ai_header)

        ai_header_layout.addStretch()

        ai_header_layout.addWidget(
            self.project_label
        )

        ai_layout.addLayout(
            ai_header_layout
        )

        ai_header.setObjectName("ai_header")

        description = QLabel(
            "Ask DevPilot to analyze your code, "
            "find bugs, explain architecture or "
            "review security."
        )

        description.setObjectName("ai_description")

        # AI input
        self.ai_input = QLineEdit()

        self.ai_input.setObjectName("ai_input")

        self.ai_input.setPlaceholderText(
            "e.g. Explain Python functions..."
        )

        # AI button
        self.ai_button = QPushButton(
            "EXECUTE ANALYSIS  →"
        )

        self.ai_button.setObjectName(
            "ai_button"
        )

        self.ai_button.clicked.connect(
            self.run_ai
        )

        # AI response
        self.ai_output = QTextEdit()
        self.ai_output.setMinimumHeight(500)
        #self.ai_output.setFont(QFont("Consolas", 20))

        self.ai_output.setReadOnly(True)

        self.ai_output.setPlaceholderText(
            "DevPilot AI response will appear here..."
        )

        self.ai_output.setStyleSheet("""
            QTextEdit {
                background-color: #080D12;
                color: #B8C7D3;
                border: 1px solid #20323D;
                border-radius: 5px;
                padding: 12px;
                font-family: Consolas;
                font-size: 13px;
            }
        """)

        ai_layout.addWidget(ai_header)
        ai_layout.addWidget(description)
        ai_layout.addWidget(self.ai_input)
        ai_layout.addWidget(self.ai_button)
        ai_layout.addWidget(self.ai_output)

        ai_frame.setLayout(ai_layout)

        content_layout.addWidget(ai_frame)

        content_layout.addSpacing(8)

        # ================= ACTIONS =================

        actions = QHBoxLayout()

        actions.setSpacing(10)

        open_project = QPushButton(
            "▣  Open Project"
        )

        open_project.setObjectName(
            "primary_button"
        )

        open_project.clicked.connect(
            self.open_project
        )

        start_review = QPushButton(
            "◇  Run Code Review"
        )

        start_review.setObjectName(
            "secondary_button"
        )

        actions.addWidget(open_project)
        actions.addWidget(start_review)
        actions.addStretch()

        content_layout.addLayout(actions)

        content_layout.addStretch()

        self.setLayout(content_layout)

    # ==================================================
    # AI
    # ==================================================

    def run_ai(self):

        question = self.ai_input.text().strip()

        if not question:
            self.ai_output.setPlainText(
                "Please enter a question."
            )
            return

        if not self.project_path:
            self.ai_output.setPlainText(
                "Please open a project first."
            )
            return

        self.ai_button.setEnabled(False)
        self.ai_button.setText("ANALYZING...")

        self.ai_output.setPlainText(
            "◈ DevPilot is analyzing your project...\n\n"
            "Searching project memory..."
        )

        self.thread = QThread()
        self.worker = DashboardAIWorker(
            self.project_ai,
            question
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.ai_finished
        )

        self.worker.error.connect(
            self.ai_error
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

    def ai_finished(self, result):

        self.ai_output.setPlainText(
            result
        )

        self.ai_button.setEnabled(True)
        self.ai_button.setText(
            "EXECUTE ANALYSIS  →"
        )

    def ai_error(self, error):

        self.ai_output.setPlainText(
            f"AI Error:\n\n{error}"
        )

        self.ai_button.setEnabled(True)
        self.ai_button.setText(
            "EXECUTE ANALYSIS  →"
        )

    # ==================================================

    def open_project(self):

        main_window = self.window()

        if hasattr(
            main_window,
            "open_project_explorer"
        ):
            main_window.open_project_explorer()

    # ==================================================

    def create_stat_card(
        self,
        title,
        value
    ):

        card = QFrame()

        card.setObjectName(
            "stat_card"
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            18, 15, 18, 15
        )

        title_label = QLabel(title)

        title_label.setObjectName(
            "stat_title"
        )

        value_label = QLabel(value)

        value_label.setObjectName(
            "stat_value"
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.setLayout(layout)

        return card

    def set_project(self, project_name, project_path=None):

        if project_name:
            self.project_label.setText(
                f"PROJECT: {project_name.upper()}"
            )
        else:
            self.project_label.setText(
                "PROJECT: NO PROJECT OPEN"
            )

        self.project_path = project_path

        if project_path:
            self.project_ai.load_project(project_path)