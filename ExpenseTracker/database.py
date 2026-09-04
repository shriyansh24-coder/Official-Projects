import sqlite3
from datetime import date


DB_NAME = "expense_tracker.db"


def connect():
    return sqlite3.connect(DB_NAME)


# ================= CREATE TABLE =================

def create_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ================= ADD EXPENSE =================

def add_expense(amount, category, description, expense_date):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        expense_date
    ))

    conn.commit()
    conn.close()


# ================= GET ALL EXPENSES =================

def get_expenses():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses


# ================= TOTAL EXPENSES =================

def get_total_expenses():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================= THIS MONTH =================

def get_monthly_expenses():

    conn = connect()
    cursor = conn.cursor()

    current_month = date.today().strftime("%Y-%m")

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE date LIKE ?
    """, (current_month + "%",))

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ================= TRANSACTION COUNT =================

def get_transaction_count():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count

# ================= UPDATE EXPENSE =================

def update_expense(expense_id, amount, category, description, expense_date):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (
        amount,
        category,
        description,
        expense_date,
        expense_id
    ))

    conn.commit()
    conn.close()


# ================= DELETE EXPENSE =================

def delete_expense(expense_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    conn.commit()
    conn.close()

# ================= CATEGORY SUMMARY =================

def get_category_summary():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    summary = cursor.fetchall()

    conn.close()

    return summary