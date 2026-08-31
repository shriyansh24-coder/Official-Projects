import sqlite3

DB_NAME = "learnhub.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():

    conn = connect()
    cursor = conn.cursor()

    # -------------------------
    # Users Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # -------------------------
    # Courses Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # -------------------------
    # User Progress Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            progress INTEGER DEFAULT 0,
            UNIQUE(username, course_id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    # -------------------------
    # Notes Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT,
            content TEXT
        )
    """)

    # -------------------------
    # Quiz Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            course_id INTEGER,
            score INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    conn.commit()
    conn.close()
    
def add_user(username, email , password):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email , password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()

def save_progress(username, course_id, progress):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM user_progress
        WHERE username = ? AND course_id = ?
    """, (username, course_id))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE user_progress
            SET progress = ?
            WHERE username = ? AND course_id = ?
        """, (progress, username, course_id))

    else:

        cursor.execute("""
            INSERT INTO user_progress
            (username, course_id, progress)
            VALUES (?, ?, ?)
        """, (username, course_id, progress))

    conn.commit()
    conn.close()

def get_progress(username, course_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT progress
        FROM user_progress
        WHERE username = ? AND course_id = ?
    """, (username, course_id))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0

def add_default_courses():

    conn = connect()
    cursor = conn.cursor()

    courses = [("Python" , "Beginner to Advanced") ,
               ("Java" , "Object Oriented Programming") ,
               ("C++" , "STL & Competitive Programming")
            ]
    cursor.executemany("INSERT OR IGNORE INTO courses (course_name, description) VALUES (?, ?)", courses)
    conn.commit()
    conn.close()

create_table()
add_default_courses()

print("Database Initialized Successfully !")