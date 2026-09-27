from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from ui.sidebar import Sidebar
from ui.theme import APP_STYLE
from pages.project_explorer import ProjectExplorer
from pages.dashboard import Dashboard
from pages.code_review import CodeReviewPage
from pages.debugger import DebuggerPage
from pages.project_analysis import ProjectAnalysisPage
from pages.test_generator import TestGeneratorPage
from pages.security import SecurityPage
from pages.git_page import GitPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "DevPilot AI"
        )

        self.resize(
            1250,
            750
        )

        self.setStyleSheet(
            APP_STYLE
        )

        self.setup_ui()

    # ==================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        # ================= SIDEBAR =================

        self.sidebar = Sidebar()

        main_layout.addWidget(
            self.sidebar
        )

        # ================= STACK =================

        self.stack = QStackedWidget()

        # Dashboard
        self.dashboard = Dashboard()

        # Project Explorer
        self.project_explorer = ProjectExplorer()

        # Code Review
        self.code_review = CodeReviewPage()

        # Debugger
        self.debugger = DebuggerPage()

        # Project Analysis
        self.project_analysis = ProjectAnalysisPage()

        # Test Generator
        self.test_generator = TestGeneratorPage()

        # Security
        self.security = SecurityPage()

        #Git Page
        self.git_page = GitPage()

        # Add pages
        self.stack.addWidget(self.dashboard)

        self.stack.addWidget(self.project_explorer)

        self.stack.addWidget(self.code_review)

        self.stack.addWidget(self.debugger)

        self.stack.addWidget(self.project_analysis)

        self.stack.addWidget(self.test_generator)

        self.stack.addWidget(self.security)

        self.stack.addWidget(self.git_page)

        main_layout.addWidget(self.stack)

        central_widget.setLayout(main_layout)

        # ================= SIDEBAR CONNECTIONS =================

        self.sidebar.dashboard_btn.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.dashboard
            )
        )

        #self.sidebar.project_explorer_btn.clicked.connect(
        #    self.open_project_explorer
        #)

        self.sidebar.review_btn.clicked.connect(
            self.open_code_review
        )

        self.sidebar.debugger_btn.clicked.connect(
            self.open_debugger
        )

        self.sidebar.analysis_btn.clicked.connect(
            self.open_project_analysis
        )

        self.sidebar.tests_btn.clicked.connect(
            self.open_test_generator
        )

        self.sidebar.security_btn.clicked.connect(
            self.open_security
        )

        self.sidebar.git_btn.clicked.connect(
            self.open_git
        )

    # ==================================================

    def open_project_explorer(self):

        # Switch to explorer
        self.stack.setCurrentWidget(
            self.project_explorer
        )

        # Open folder dialog
        self.project_explorer.open_project()

        # Get opened project path
        project_path = self.project_explorer.project_path

        if project_path:

            import os

            project_name = os.path.basename(
                os.path.normpath(project_path)
            )

            self.dashboard.set_project(
                project_name,
                project_path
            )

    def open_code_review(self):

        self.stack.setCurrentWidget(
            self.code_review
        )

        project_path = (
            self.project_explorer.project_path
        )

        self.code_review.set_project(
            project_path
        )

    def open_debugger(self):

        self.stack.setCurrentWidget(self.debugger)

        project_path = self.project_explorer.project_path

        self.debugger.set_project(project_path)

    def open_project_analysis(self):

        self.stack.setCurrentWidget(
            self.project_analysis
        )

        project_path = (
            self.project_explorer.project_path
        )

        self.project_analysis.set_project(
            project_path
        )    

    def open_test_generator(self):

        self.stack.setCurrentWidget(
            self.test_generator
        )

        project_path = (
            self.project_explorer.project_path
        )

        self.test_generator.set_project(
            project_path
        )

    def open_security(self):

        self.stack.setCurrentWidget(
            self.security
        )

        project_path = (
            self.project_explorer.project_path
        )

        self.security.set_project(
            project_path
        )

    def open_git(self):

        self.stack.setCurrentWidget(
            self.git_page
        )

        project_path = (
            self.project_explorer.project_path
        )

        self.git_page.set_project(
            project_path
        )