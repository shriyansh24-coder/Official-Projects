import sqlite3
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from register import RegisterWindow

from dashboard import Dashboard


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.setWindowTitle("LearnHub Login")
        self.setFixedSize(500, 600)

        # Build UI
        self.initUI()

    def initUI(self):

        # =========================
        # Title
        # =========================
        title = QLabel("📚 LearnHub")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        subtitle = QLabel("Learn • Practice • Grow")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))

        # =========================
        # Username
        # =========================
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")

        # =========================
        # Password
        # =========================
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)

        # =========================
        # Buttons
        # =========================
        login_button = QPushButton("Login")
        register_button = QPushButton("Create Account")

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)

        # =========================
        # Layout
        # =========================
        layout = QVBoxLayout()

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        layout.addSpacing(20)

        layout.addWidget(login_button)
        layout.addWidget(register_button)

        layout.addStretch()

        self.setLayout(layout)

        # =========================
        # Styles
        # =========================
        self.setStyleSheet("""
            QWidget{
                background-color:#111827;
                color:white;
                font-family:Segoe UI;
            }

            QLabel{
                color:white;
            }

            QLineEdit{
                background:#1F2937;
                border:2px solid #3B82F6;
                border-radius:12px;
                padding:10px;
                color:white;
                font-size:15px;
            }

            QLineEdit:focus{
                border:2px solid #10B981;
            }

            QPushButton{
                background:#2563EB;
                color:white;
                border:none;
                border-radius:12px;
                padding:12px;
                font-size:16px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#3B82F6;
            }

            QPushButton:pressed{
                background:#1D4ED8;
            }
        """)

    # =========================
    # Login Function
    # =========================
    def login(self):
        username = self.username.text().strip()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
            return

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            self.dashboard = Dashboard(username)
            self.dashboard.show()
            self.close()

        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

    # =========================
    # Register Function
    # =========================
    def register(self):
        print("Register Button Clicked!")

        self.register_window = RegisterWindow()
        self.register_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())