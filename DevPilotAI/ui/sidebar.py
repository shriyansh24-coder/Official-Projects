from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy
)

from PyQt5.QtCore import Qt


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(225)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(5)

        # Logo
        logo = QLabel("◈  DEVPILOT")
        logo.setObjectName("logo")

        layout.addWidget(logo)

        # Workspace
        workspace = QLabel("WORKSPACE")
        workspace.setObjectName("workspace_label")

        layout.addWidget(workspace)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("separator")

        layout.addWidget(line)

        # Navigation
        self.dashboard_btn = self.create_button("▣   Command Center")
        self.review_btn = self.create_button("◇   Code Review")
        self.debugger_btn = self.create_button("◉   Debugger")
        self.analysis_btn = self.create_button("⌘   Project Analysis")
        self.tests_btn = self.create_button("▤   Test Generator")
        self.security_btn = self.create_button("◆   Security")
        self.git_btn = self.create_button("⑂   Git")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.review_btn)
        layout.addWidget(self.debugger_btn)
        layout.addWidget(self.analysis_btn)
        layout.addWidget(self.tests_btn)
        layout.addWidget(self.security_btn)
        layout.addWidget(self.git_btn)

        # Settings at bottom
        spacer = QSpacerItem(
            20,
            20,
            QSizePolicy.Minimum,
            QSizePolicy.Expanding
        )

        layout.addItem(spacer)

        self.settings_btn = self.create_button("⚙   Settings")

        layout.addWidget(self.settings_btn)

        self.setLayout(layout)

        # Dashboard selected by default
        self.dashboard_btn.setObjectName("active_button")

    def create_button(self, text):

        button = QPushButton(text)

        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(42)

        return button