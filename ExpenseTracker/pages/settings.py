from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton
)


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ================= UI =================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40, 35, 40, 35
        )

        layout.setSpacing(15)

        # ================= HEADER =================

        title = QLabel("Settings")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Manage your Expense Tracker"
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(25)

        # ================= GENERAL =================

        general_title = QLabel(
            "General"
        )

        general_title.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(
            general_title
        )

        general_card = QFrame()

        general_card.setObjectName(
            "card"
        )

        general_layout = QVBoxLayout(
            general_card
        )

        # Currency
        currency_row = QHBoxLayout()

        currency_label = QLabel(
            "Currency"
        )

        currency_value = QLabel(
            "₹  Indian Rupee"
        )

        currency_value.setStyleSheet("""
            color: #777788;
            font-size: 14px;
        """)

        currency_row.addWidget(
            currency_label
        )

        currency_row.addStretch()

        currency_row.addWidget(
            currency_value
        )

        general_layout.addLayout(
            currency_row
        )

        # Application
        app_row = QHBoxLayout()

        app_label = QLabel(
            "Application"
        )

        app_value = QLabel(
            "Expense Tracker"
        )

        app_value.setStyleSheet("""
            color: #777788;
            font-size: 14px;
        """)

        app_row.addWidget(
            app_label
        )

        app_row.addStretch()

        app_row.addWidget(
            app_value
        )

        general_layout.addLayout(
            app_row
        )

        # Version
        version_row = QHBoxLayout()

        version_label = QLabel(
            "Version"
        )

        version_value = QLabel(
            "1.0.0"
        )

        version_value.setStyleSheet("""
            color: #777788;
            font-size: 14px;
        """)

        version_row.addWidget(
            version_label
        )

        version_row.addStretch()

        version_row.addWidget(
            version_value
        )

        general_layout.addLayout(
            version_row
        )

        layout.addWidget(
            general_card
        )

        layout.addSpacing(25)

        # ================= ABOUT =================

        about_title = QLabel(
            "About"
        )

        about_title.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(
            about_title
        )

        about_card = QFrame()

        about_card.setObjectName(
            "card"
        )

        about_layout = QVBoxLayout(
            about_card
        )

        app_name = QLabel(
            "💰 Expense Tracker"
        )

        app_name.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        description = QLabel(
            "A simple and professional expense "
            "management application built with "
            "Python, PyQt5 and SQLite."
        )

        description.setWordWrap(True)

        description.setStyleSheet("""
            color: #777788;
            font-size: 14px;
        """)

        about_layout.addWidget(
            app_name
        )

        about_layout.addWidget(
            description
        )

        layout.addWidget(
            about_card
        )

        layout.addStretch()