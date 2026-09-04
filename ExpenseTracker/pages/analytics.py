from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QProgressBar
)

from database import (
    get_total_expenses,
    get_category_summary
)


class AnalyticsPage(QWidget):

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

        title = QLabel("Analytics")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Understand where your money is going"
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(25)

        # ================= TOTAL CARD =================

        total_card = QFrame()
        total_card.setObjectName("card")
        total_card.setFixedHeight(130)

        total_layout = QVBoxLayout(
            total_card
        )

        total_label = QLabel(
            "Total Spending"
        )
        total_label.setObjectName(
            "cardTitle"
        )

        self.total_amount = QLabel(
            "₹ 0.00"
        )
        self.total_amount.setObjectName(
            "cardValue"
        )

        total_layout.addWidget(
            total_label
        )

        total_layout.addWidget(
            self.total_amount
        )

        layout.addWidget(total_card)

        layout.addSpacing(25)

        # ================= CATEGORY =================

        category_title = QLabel(
            "Spending by Category"
        )
        category_title.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(
            category_title
        )

        self.category_layout = QVBoxLayout()

        self.category_layout.setSpacing(12)

        layout.addLayout(
            self.category_layout
        )

        layout.addStretch()

        self.load_analytics()

    # ================= LOAD =================

    def load_analytics(self):

        total = get_total_expenses()

        self.total_amount.setText(
            f"₹ {total:,.2f}"
        )

        # Remove previous widgets
        while self.category_layout.count():

            item = self.category_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        summary = get_category_summary()

        if not summary:

            empty = QLabel(
                "No expenses available yet."
            )

            empty.setObjectName(
                "emptyLabel"
            )

            self.category_layout.addWidget(
                empty
            )

            return

        for category, amount in summary:

            row = QFrame()
            row.setObjectName("card")

            row_layout = QVBoxLayout(row)

            # Top row
            top_layout = QHBoxLayout()

            category_label = QLabel(
                category
            )

            category_label.setStyleSheet("""
                font-size: 15px;
                font-weight: bold;
            """)

            percentage = (
                amount / total * 100
                if total > 0 else 0
            )

            percentage_label = QLabel(
                f"₹ {amount:,.2f}   "
                f"({percentage:.1f}%)"
            )

            percentage_label.setStyleSheet("""
                font-size: 14px;
                color: #777788;
            """)

            top_layout.addWidget(
                category_label
            )

            top_layout.addStretch()

            top_layout.addWidget(
                percentage_label
            )

            row_layout.addLayout(
                top_layout
            )

            # Progress bar
            progress = QProgressBar()

            progress.setRange(
                0, 100
            )

            progress.setValue(
                int(percentage)
            )

            progress.setTextVisible(False)

            progress.setFixedHeight(8)

            row_layout.addWidget(
                progress
            )

            self.category_layout.addWidget(
                row
            )