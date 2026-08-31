import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QMessageBox,
    QLineEdit
)

from PyQt5.QtGui import QFont


class SettingsPage(QWidget):

    def __init__(self, username):

        super().__init__()

        self.username = username

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            30, 25, 30, 25
        )

        layout.setSpacing(15)

        # -----------------------------------------
        # Heading
        # -----------------------------------------

        heading = QLabel(
            "⚙ Settings"
        )

        heading.setFont(
            QFont(
                "Segoe UI",
                26,
                QFont.Bold
            )
        )

        layout.addWidget(
            heading
        )

        # -----------------------------------------
        # Account Information
        # -----------------------------------------

        account_card = QFrame()

        account_layout = QVBoxLayout()

        account_title = QLabel(
            "👤 Account Information"
        )

        account_title.setFont(
            QFont(
                "Segoe UI",
                17,
                QFont.Bold
            )
        )

        username_label = QLabel(
            f"Username: {self.username}"
        )

        username_label.setFont(
            QFont(
                "Segoe UI",
                14
            )
        )

        account_layout.addWidget(
            account_title
        )

        account_layout.addWidget(
            username_label
        )

        account_card.setLayout(
            account_layout
        )

        layout.addWidget(
            account_card
        )

        # -----------------------------------------
        # Change Password
        # -----------------------------------------

        password_card = QFrame()

        password_layout = QVBoxLayout()

        password_title = QLabel(
            "🔑 Change Password"
        )

        password_title.setFont(
            QFont(
                "Segoe UI",
                17,
                QFont.Bold
            )
        )

        new_password = QLineEdit()

        new_password.setPlaceholderText(
            "Enter new password"
        )

        new_password.setEchoMode(
            QLineEdit.Password
        )

        change_button = QPushButton(
            "Change Password"
        )

        change_button.setFont(
            QFont(
                "Segoe UI",
                13
            )
        )

        change_button.setMinimumHeight(
            42
        )

        change_button.clicked.connect(
            lambda: self.change_password(
                new_password
            )
        )

        password_layout.addWidget(
            password_title
        )

        password_layout.addWidget(
            new_password
        )

        password_layout.addWidget(
            change_button
        )

        password_card.setLayout(
            password_layout
        )

        layout.addWidget(
            password_card
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

        # -----------------------------------------
        # Style
        # -----------------------------------------

        self.setStyleSheet("""
            QWidget {
                background: #111827;
                color: white;
            }

            QLabel {
                color: white;
            }

            QFrame {
                background: #1F2937;
                border-radius: 12px;
                padding: 15px;
            }

            QLineEdit {
                background: #374151;
                color: white;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton {
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #3B82F6;
            }
        """)

    # ---------------------------------------------
    # Change Password
    # ---------------------------------------------

    def change_password(self, password_box):

        new_password = password_box.text().strip()

        if not new_password:

            QMessageBox.warning(
                self,
                "Error",
                "Please enter a new password."
            )

            return

        conn = sqlite3.connect(
            "learnhub.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE username = ?
            """,
            (
                new_password,
                self.username
            )
        )

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Success",
            "Password changed successfully!"
        )

        password_box.clear()