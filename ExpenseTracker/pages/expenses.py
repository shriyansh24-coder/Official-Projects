from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog,
    QLineEdit,
    QComboBox,
    QDateEdit
)

from PyQt5.QtCore import Qt, QDate

from database import (
    get_expenses,
    update_expense,
    delete_expense
)


class ExpensesPage(QWidget):

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

        header_layout = QHBoxLayout()

        title = QLabel("Expenses")
        title.setObjectName("pageTitle")

        header_layout.addWidget(title)
        header_layout.addStretch()

        refresh_button = QPushButton("🔄 Refresh")
        refresh_button.setFixedWidth(100)

        refresh_button.clicked.connect(
            self.load_expenses
        )

        header_layout.addWidget(
            refresh_button
        )

        layout.addLayout(header_layout)

        subtitle = QLabel(
            "View and manage all your expenses"
        )

        subtitle.setObjectName("subtitle")

        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # ================= TABLE =================

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Category",
            "Description",
            "Amount",
            "Edit",
            "Delete"
        ])

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2, QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4, QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            5, QHeaderView.ResizeToContents
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # ================= BOTTOM =================

        bottom_layout = QHBoxLayout()

        self.count_label = QLabel(
            "0 expenses"
        )

        self.count_label.setObjectName(
            "subtitle"
        )

        bottom_layout.addWidget(
            self.count_label
        )

        bottom_layout.addStretch()

        layout.addLayout(bottom_layout)

        # Load data
        self.load_expenses()

    # ================= LOAD =================

    def load_expenses(self):

        expenses = get_expenses()

        self.table.setRowCount(
            len(expenses)
        )

        for row, expense in enumerate(expenses):

            expense_id = expense[0]
            amount = expense[1]
            category = expense[2]
            description = expense[3]
            expense_date = expense[4]

            # Date
            date_item = QTableWidgetItem(
                expense_date
            )

            # Category
            category_item = QTableWidgetItem(
                category
            )

            # Description
            description_item = QTableWidgetItem(
                description or "-"
            )

            # Amount
            amount_item = QTableWidgetItem(
                f"₹ {amount:,.2f}"
            )

            date_item.setTextAlignment(
                Qt.AlignCenter
            )

            category_item.setTextAlignment(
                Qt.AlignCenter
            )

            amount_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row, 0, date_item
            )

            self.table.setItem(
                row, 1, category_item
            )

            self.table.setItem(
                row, 2, description_item
            )

            self.table.setItem(
                row, 3, amount_item
            )

            # ================= EDIT =================

            edit_button = QPushButton("✏️")

            edit_button.setFixedSize(
                45, 32
            )

            edit_button.clicked.connect(
                lambda checked,
                expense_id=expense_id:
                self.edit_expense(expense_id)
            )

            self.table.setCellWidget(
                row, 4, edit_button
            )

            # ================= DELETE =================

            delete_button = QPushButton("🗑️")

            delete_button.setFixedSize(
                45, 32
            )

            delete_button.clicked.connect(
                lambda checked,
                expense_id=expense_id:
                self.confirm_delete(expense_id)
            )

            self.table.setCellWidget(
                row, 5, delete_button
            )

        # Count
        count = len(expenses)

        self.count_label.setText(
            f"{count} expense"
            + ("s" if count != 1 else "")
        )

    # ================= EDIT =================

    def edit_expense(self, expense_id):

        expenses = get_expenses()

        selected_expense = None

        for expense in expenses:

            if expense[0] == expense_id:

                selected_expense = expense
                break

        if selected_expense is None:
            return

        _, amount, category, description, expense_date = selected_expense

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "Edit Expense"
        )

        dialog.setFixedWidth(400)

        layout = QVBoxLayout(dialog)

        # Amount
        amount_label = QLabel("Amount")

        amount_input = QLineEdit(
            str(amount)
        )

        layout.addWidget(amount_label)
        layout.addWidget(amount_input)

        # Category
        category_label = QLabel("Category")

        category_input = QComboBox()

        category_input.addItems([
            "Food",
            "Transport",
            "Shopping",
            "Entertainment",
            "Bills",
            "Education",
            "Health",
            "Other"
        ])

        category_input.setCurrentText(
            category
        )

        layout.addWidget(category_label)
        layout.addWidget(category_input)

        # Description
        description_label = QLabel(
            "Description"
        )

        description_input = QLineEdit(
            description or ""
        )

        layout.addWidget(
            description_label
        )

        layout.addWidget(
            description_input
        )

        # Date
        date_label = QLabel("Date")

        date_input = QDateEdit()

        date_input.setCalendarPopup(True)

        date_input.setDate(
            QDate.fromString(
                expense_date,
                "yyyy-MM-dd"
            )
        )

        layout.addWidget(date_label)
        layout.addWidget(date_input)

        # ================= BUTTONS =================

        buttons_layout = QHBoxLayout()

        save_button = QPushButton(
            "💾 Save Changes"
        )

        cancel_button = QPushButton(
            "Cancel"
        )

        buttons_layout.addWidget(
            save_button
        )

        buttons_layout.addWidget(
            cancel_button
        )

        layout.addLayout(
            buttons_layout
        )

        # ================= SAVE =================

        def save_changes():

            try:

                new_amount = float(
                    amount_input.text().strip()
                )

                if new_amount <= 0:
                    raise ValueError

            except ValueError:

                QMessageBox.warning(
                    dialog,
                    "Invalid Amount",
                    "Please enter a valid amount."
                )

                return

            new_category = (
                category_input.currentText()
            )

            new_description = (
                description_input.text().strip()
            )

            new_date = (
                date_input.date().toString(
                    "yyyy-MM-dd"
                )
            )

            update_expense(
                expense_id,
                new_amount,
                new_category,
                new_description,
                new_date
            )

            QMessageBox.information(
                dialog,
                "Success",
                "Expense updated successfully!"
            )

            dialog.accept()

            self.load_expenses()

        save_button.clicked.connect(
            save_changes
        )

        cancel_button.clicked.connect(
            dialog.reject
        )

        dialog.exec_()

    # ================= DELETE =================

    def confirm_delete(self, expense_id):

        reply = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            delete_expense(
                expense_id
            )

            self.load_expenses()

            QMessageBox.information(
                self,
                "Deleted",
                "Expense deleted successfully!"
            )