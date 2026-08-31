import sqlite3
from turtle import title

from PyQt5.QtWidgets import(
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QProgressBar,
    QLineEdit
)
from PyQt5.QtGui import QFont

from pages.course_details import CourseDetails

class CoursesPage(QWidget):

    def __init__(self , username):
        super().__init__()

        self.username = username
        self.initUI()

    def create_course(self, course_name, description, progress):

        card = QFrame()

        layout = QVBoxLayout()

        icons = {
            "Python": "🐍",
            "Java": "☕",
            "C++": "💻"
        }

        icon = icons.get(course_name, "📚")

        title_label = QLabel(
            f"{icon} {course_name}"
        )

        title_label.setFont(
            QFont("Segoe UI", 16, QFont.Bold)
        )

        desc = QLabel(description)

        desc.setFont(
            QFont("Segoe UI", 15)
        )

        bar = QProgressBar()
        bar.setValue(progress)

        button = QPushButton("Open Course")

        button.setFont(
            QFont("Segoe UI", 12)
        )

        # IMPORTANT
        button.clicked.connect(
            lambda: self.open_course(course_name)
        )

        layout.addWidget(title_label)
        layout.addWidget(desc)
        layout.addWidget(bar)
        layout.addWidget(button)

        card.setLayout(layout)

        return card

    def initUI(self):

        layout = QVBoxLayout()

        heading = QLabel("📚 Courses")
        heading.setFont(QFont("Segoe UI" , 26 , QFont.Bold))

        search = QLineEdit()
        search.setPlaceholderText("Search Courses...")
        search.setFont(QFont("Segoe UI" , 14))

        layout.addWidget(heading)
        layout.addWidget(search)

        layout.addSpacing(20)

        icons = {
            "Python": "🐍",
            "Java": "☕",
            "C++": "💻"
        }

        for course_name, description in self.load_courses():

            progress = self.get_course_progress(course_name)

            layout.addWidget(
                self.create_course(
                    course_name,
                    description,
                    progress
                )
            )

        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget{
                background:#111827;
                color:white;
            }

            QFrame{
                background:#1F2937;
                border-radius:12px;
                padding:15px;
            }

            QLabel{
                color:white;
            }

            QLineEdit{
                background:#374151;
                border:2px solid #3B82F6;
                border-radius:10px;
                padding:8px;
                color:white;
            }

            QPushButton{
                background:#2563EB;
                color:white;
                border:none;
                border-radius:8px;
                padding:10px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#3B82F6;
            }

            QProgressBar{
                height:20px;
                border-radius:8px;
                font-weight:bold;
                font-size:12px;
                text-align:center;
            }

            QProgressBar::chunk{
                background:#3B82F6;
            }

        """)
    def load_courses(self):

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT course_name, description
            FROM courses
        """)

        courses = cursor.fetchall()

        conn.close()

        return courses

    def get_course_progress(self, course_name):

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        # Get course ID
        cursor.execute("""
            SELECT id
            FROM courses
            WHERE course_name = ?
        """, (course_name,))

        course = cursor.fetchone()

        if course is None:
            conn.close()
            return 0

        course_id = course[0]

        # Get user's saved progress
        cursor.execute("""
            SELECT progress
            FROM user_progress
            WHERE username = ? AND course_id = ?
        """, (self.username, course_id))

        result = cursor.fetchone()

        conn.close()

        if result is None:
            return 0

        return result[0]

    def open_course(self, course_name):

        self.course_window = CourseDetails(course_name, self.username)

        self.course_window.show()