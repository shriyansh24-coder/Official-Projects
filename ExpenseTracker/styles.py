APP_STYLE = """

QMainWindow {
    background-color: #f5f6fa;
}

/* ================= SIDEBAR ================= */

QFrame#sidebar {
    background-color: #1e1e2f;
    border: none;
}

QLabel#logo {
    color: white;
    font-size: 20px;
    font-weight: bold;
}

QPushButton#menuButton {
    background-color: transparent;
    color: #c7c7d9;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding-left: 15px;
    font-size: 14px;
}

QPushButton#menuButton:hover {
    background-color: #2d2d44;
    color: white;
}

QPushButton#menuButton:pressed {
    background-color: #363653;
}

/* ================= DASHBOARD ================= */

QLabel#pageTitle {
    color: #20202d;
    font-size: 28px;
    font-weight: bold;
}

QLabel#subtitle {
    color: #777788;
    font-size: 14px;
}

/* ================= CARDS ================= */

QFrame#card {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #e7e7ee;
}

QLabel#cardTitle {
    color: #777788;
    font-size: 13px;
}

QLabel#cardValue {
    color: #20202d;
    font-size: 26px;
    font-weight: bold;
}

/* ================= RECENT EXPENSES ================= */

QLabel#sectionTitle {
    color: #20202d;
    font-size: 20px;
    font-weight: bold;
}

QLabel#emptyLabel {
    color: #9999aa;
    font-size: 14px;
}

"""