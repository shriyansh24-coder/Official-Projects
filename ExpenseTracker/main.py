import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget
)

from PyQt5.QtCore import Qt

from styles import APP_STYLE
from database import (
    create_table,
    get_total_expenses,
    get_monthly_expenses,
    get_transaction_count,
    get_expenses
)

from pages.add_expense import AddExpensePage

from pages.expenses import ExpensesPage

from pages.analytics import AnalyticsPage

from pages.settings import SettingsPage


class ExpenseTracker(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 1200, 700)

        # ================= MAIN WIDGET =================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)
        sidebar_layout.setSpacing(10)

        # Logo
        logo = QLabel("💰 Expense Tracker")
        logo.setObjectName("logo")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(30)

        # Dashboard Button
        dashboard_btn = QPushButton("🏠  Dashboard")
        dashboard_btn.setObjectName("menuButton")
        dashboard_btn.setFixedHeight(45)
        dashboard_btn.clicked.connect(self.show_dashboard)

        # Add Expense Button
        add_expense_btn = QPushButton("➕  Add Expense")
        add_expense_btn.setObjectName("menuButton")
        add_expense_btn.setFixedHeight(45)
        add_expense_btn.clicked.connect(self.show_add_expense)

        # Expenses Button
        expenses_btn = QPushButton("🧾  Expenses")
        expenses_btn.setObjectName("menuButton")
        expenses_btn.setFixedHeight(45)
        expenses_btn.clicked.connect(self.show_expenses)

        # Analytics Button
        analytics_btn = QPushButton("📊  Analytics")
        analytics_btn.setObjectName("menuButton")
        analytics_btn.setFixedHeight(45)
        analytics_btn.clicked.connect(self.show_analytics)

        # Settings Button
        settings_btn = QPushButton("⚙️  Settings")
        settings_btn.setObjectName("menuButton")
        settings_btn.setFixedHeight(45)
        settings_btn.clicked.connect(self.show_settings)

        sidebar_layout.addWidget(dashboard_btn)
        sidebar_layout.addWidget(add_expense_btn)
        sidebar_layout.addWidget(expenses_btn)
        sidebar_layout.addWidget(analytics_btn)
        sidebar_layout.addWidget(settings_btn)

        sidebar_layout.addStretch()

        # Logout
        logout_btn = QPushButton("🚪  Logout")
        logout_btn.setObjectName("menuButton")
        logout_btn.setFixedHeight(45)

        sidebar_layout.addWidget(logout_btn)

        # ================= PAGE CONTAINER =================

        self.pages = QStackedWidget()

        # ================= DASHBOARD =================

        dashboard = QWidget()

        dashboard_layout = QVBoxLayout(dashboard)

        dashboard_layout.setContentsMargins(
            35, 30, 35, 30
        )

        # Title
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Track and manage your expenses"
        )
        subtitle.setObjectName("subtitle")

        dashboard_layout.addWidget(title)
        dashboard_layout.addWidget(subtitle)

        dashboard_layout.addSpacing(30)

        # ================= SUMMARY CARDS =================

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # ---------- Total Expenses ----------

        total_card = QFrame()
        total_card.setObjectName("card")
        total_card.setFixedHeight(130)

        total_layout = QVBoxLayout(total_card)

        total_label = QLabel("Total Expenses")
        total_label.setObjectName("cardTitle")

        self.total_amount = QLabel("₹ 0")
        self.total_amount.setObjectName("cardValue")

        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_amount)

        # ---------- This Month ----------

        month_card = QFrame()
        month_card.setObjectName("card")
        month_card.setFixedHeight(130)

        month_layout = QVBoxLayout(month_card)

        month_label = QLabel("This Month")
        month_label.setObjectName("cardTitle")

        self.month_amount = QLabel("₹ 0")
        self.month_amount.setObjectName("cardValue")

        month_layout.addWidget(month_label)
        month_layout.addWidget(self.month_amount)

        # ---------- Transactions ----------

        records_card = QFrame()
        records_card.setObjectName("card")
        records_card.setFixedHeight(130)

        records_layout = QVBoxLayout(records_card)

        records_label = QLabel("Transactions")
        records_label.setObjectName("cardTitle")

        self.records_count = QLabel("0")
        self.records_count.setObjectName("cardValue")

        records_layout.addWidget(records_label)
        records_layout.addWidget(self.records_count)

        # Add cards
        cards_layout.addWidget(total_card)
        cards_layout.addWidget(month_card)
        cards_layout.addWidget(records_card)

        dashboard_layout.addLayout(cards_layout)

        dashboard_layout.addSpacing(30)

        # ================= RECENT EXPENSES =================

        recent_title = QLabel("Recent Expenses")
        recent_title.setObjectName("sectionTitle")

        dashboard_layout.addWidget(recent_title)

        self.recent_text = QLabel()

        self.recent_text.setObjectName("emptyLabel")

        self.recent_text.setAlignment(
            Qt.AlignCenter
        )

        self.recent_text.setMinimumHeight(200)

        dashboard_layout.addWidget(
            self.recent_text
        )

        dashboard_layout.addStretch()

        # ================= ADD EXPENSE PAGE =================

        self.add_expense_page = AddExpensePage()
        self.expenses_page = ExpensesPage()

        self.analytics_page = AnalyticsPage()
        self.settings_page = SettingsPage()

        self.add_expense_page.back_requested.connect(
            self.show_dashboard
        )

        # IMPORTANT:
        # Refresh dashboard after saving an expense
        self.add_expense_page.back_requested.connect(
            self.refresh_dashboard
        )

        # ================= ADD PAGES =================

        self.pages.addWidget(dashboard)
        self.pages.addWidget(
            self.add_expense_page
        )
        self.pages.addWidget(
            self.expenses_page
        )
        self.pages.addWidget(
            self.analytics_page
        )
        self.pages.addWidget(
            self.settings_page
        )

        # ================= MAIN LAYOUT =================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        # Load dashboard data
        self.refresh_dashboard()

    # ================= NAVIGATION =================

    def show_dashboard(self):

        self.pages.setCurrentIndex(0)

        self.refresh_dashboard()

    def show_add_expense(self):

        self.pages.setCurrentIndex(1)

    def show_expenses(self):

        self.pages.setCurrentIndex(2)
        self.expenses_page.load_expenses()

    def show_analytics(self):

        self.pages.setCurrentIndex(3)

        self.analytics_page.load_analytics()


    def show_settings(self):

        self.pages.setCurrentIndex(4)

    # ================= REFRESH DASHBOARD =================

    def refresh_dashboard(self):

        # Total expenses
        total = get_total_expenses()

        self.total_amount.setText(
            f"₹ {total:,.2f}"
        )

        # This month
        monthly = get_monthly_expenses()

        self.month_amount.setText(
            f"₹ {monthly:,.2f}"
        )

        # Transaction count
        count = get_transaction_count()

        self.records_count.setText(
            str(count)
        )

        # Recent expenses
        expenses = get_expenses()

        if not expenses:

            self.recent_text.setText(
                "No expenses added yet.\n"
                "Your recent transactions will appear here."
            )

        else:

            recent = expenses[:5]

            text = ""

            for expense in recent:

                expense_id = expense[0]
                amount = expense[1]
                category = expense[2]
                description = expense[3]
                expense_date = expense[4]

                text += (
                    f"₹ {amount:,.2f}   |   "
                    f"{category}   |   "
                    f"{description or 'No description'}   |   "
                    f"{expense_date}\n\n"
                )

            self.recent_text.setText(text)


# ================= APPLICATION =================

if __name__ == "__main__":

    create_table()

    app = QApplication(sys.argv)

    app.setStyleSheet(APP_STYLE)

    window = ExpenseTracker()

    window.show()

    sys.exit(app.exec_())