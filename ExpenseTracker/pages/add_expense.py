from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDateEdit,
    QMessageBox
)

from PyQt5.QtCore import QDate, pyqtSignal

from database import add_expense


class AddExpensePage(QWidget):

    # Signal used to go back to Dashboard
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        # ================= MAIN LAYOUT =================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40, 35, 40, 35
        )

        layout.setSpacing(15)

        # ================= BACK BUTTON =================

        back_button = QPushButton("←  Back")

        back_button.setFixedWidth(100)

        back_button.clicked.connect(
            self.back_requested.emit
        )

        layout.addWidget(back_button)

        # ================= TITLE =================

        title = QLabel("Add Expense")

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        subtitle = QLabel(
            "Record a new expense"
        )

        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #777788;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # ================= AMOUNT =================

        amount_label = QLabel("Amount")

        self.amount_input = QLineEdit()

        self.amount_input.setPlaceholderText(
            "Enter amount"
        )

        layout.addWidget(amount_label)
        layout.addWidget(self.amount_input)

        # ================= CATEGORY =================

        category_label = QLabel("Category")

        self.category_input = QComboBox()

        self.category_input.addItems([
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Health",
            "Other"
        ])

        layout.addWidget(category_label)
        layout.addWidget(self.category_input)

        # ================= DESCRIPTION =================

        description_label = QLabel("Description")

        self.description_input = QLineEdit()

        self.description_input.setPlaceholderText(
            "What was this expense for?"
        )

        layout.addWidget(description_label)
        layout.addWidget(self.description_input)

        # ================= DATE =================

        date_label = QLabel("Date")

        self.date_input = QDateEdit()

        self.date_input.setCalendarPopup(True)

        self.date_input.setDate(
            QDate.currentDate()
        )

        layout.addWidget(date_label)
        layout.addWidget(self.date_input)

        layout.addSpacing(15)

        # ================= BUTTONS =================

        buttons_layout = QHBoxLayout()

        save_button = QPushButton(
            "💾  Save Expense"
        )

        clear_button = QPushButton(
            "Clear"
        )

        save_button.clicked.connect(
            self.save_expense
        )

        clear_button.clicked.connect(
            self.clear_form
        )

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(clear_button)

        layout.addLayout(buttons_layout)

        layout.addStretch()

    # ================= SAVE EXPENSE =================

    def save_expense(self):

        amount = self.amount_input.text().strip()

        category = self.category_input.currentText()

        description = (
            self.description_input.text().strip()
        )

        date = self.date_input.date().toString(
            "yyyy-MM-dd"
        )

        # Validate amount
        try:

            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Amount",
                "Please enter a valid amount."
            )

            return

        # Save to database
        add_expense(
            amount,
            category,
            description,
            date
        )

        QMessageBox.information(
            self,
            "Success",
            "Expense added successfully!"
        )

        self.clear_form()

    # ================= CLEAR FORM =================

    def clear_form(self):

        self.amount_input.clear()

        self.category_input.setCurrentIndex(0)

        self.description_input.clear()

        self.date_input.setDate(
            QDate.currentDate()
        )