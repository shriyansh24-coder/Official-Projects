import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PyQt5.QtGui import QFont


class ProfilePage(QWidget):

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
            "👤 Profile"
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
        # Get Email
        # -----------------------------------------

        email = ""

        conn = sqlite3.connect(
            "learnhub.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT email
            FROM users
            WHERE username = ?
            """,
            (self.username,)
        )

        result = cursor.fetchone()

        if result:
            email = result[0]

        conn.close()

        # -----------------------------------------
        # Profile Card
        # -----------------------------------------

        card = QFrame()

        card.setStyleSheet("""
            QFrame {
                background: #1F2937;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        card_layout = QVBoxLayout()

        name_label = QLabel(
            f"👤 Username: {self.username}"
        )

        name_label.setFont(
            QFont(
                "Segoe UI",
                16,
                QFont.Bold
            )
        )

        email_label = QLabel(
            f"📧 Email: {email}"
        )

        email_label.setFont(
            QFont(
                "Segoe UI",
                15
            )
        )

        account_label = QLabel(
            "🔐 Account: Active"
        )

        account_label.setFont(
            QFont(
                "Segoe UI",
                15
            )
        )

        card_layout.addWidget(
            name_label
        )

        card_layout.addWidget(
            email_label
        )

        card_layout.addWidget(
            account_label
        )

        card.setLayout(
            card_layout
        )

        layout.addWidget(
            card
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

        # -----------------------------------------
        # Page Style
        # -----------------------------------------

        self.setStyleSheet("""
            QWidget {
                background: #111827;
                color: white;
            }

            QLabel {
                color: white;
            }
        """)