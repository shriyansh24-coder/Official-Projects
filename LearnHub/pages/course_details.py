import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QProgressBar
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CourseDetails(QWidget):

    def load_progress(self):

        course_id = self.get_course_id()

        if course_id is None:
            return

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT progress
            FROM user_progress
            WHERE username = ? AND course_id = ?
        """, (self.username, course_id))

        result = cursor.fetchone()

        conn.close()

        if result:

            progress = result[0]

            self.progress_bar.setValue(progress)

            self.progress_label.setText(
                f"Progress: {progress}%"
            )

            # Restore completed lessons
            completed_count = round(
                progress / 100 * len(self.lessons)
            )

            for i in range(completed_count):

                self.completed_lessons.add(i)

                item = self.lesson_list.item(i)

                item.setText(
                    "✅ " + self.lessons[i]
                )

    def get_course_id(self):
        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        course_name = self.course_name

        cursor.execute("""
            SELECT id
            FROM courses
            WHERE course_name = ?
        """, (course_name,))

        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]

        return None

    def save_progress(self , progress):

        course_id = self.get_course_id()

        if course_id is None:
            return

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute("""
                SELECT id
                FROM user_progress
                WHERE username = ? AND course_id = ?
            """, (self.username, course_id))

        existing = cursor.fetchone()

        if existing:

            cursor.execute("""
                UPDATE user_progress
                SET progress = ?
                WHERE username = ? AND course_id = ?
            """, (progress, self.username, course_id))

        else:

            cursor.execute("""
                INSERT INTO user_progress
                (username, course_id, progress)
                VALUES (?, ?, ?)
            """, (self.username, course_id, progress))

        conn.commit()
        conn.close()

    def __init__(self, course_name , username):
        super().__init__()

        self.course_name = course_name
        self.username = username

        self.current_lesson = 0
        self.completed_lessons = set()

        self.lessons = [
            "Introduction",
            "Variables",
            "Data Types",
            "Operators",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Object Oriented Programming",
            "Mini Project"
        ]

        self.initUI()

        self.load_progress()

    def initUI(self):

        self.setWindowTitle(f"{self.course_name} - LearnHub")
        self.setFixedSize(700, 600)

        layout = QVBoxLayout()

        # Course Title
        title = QLabel(f"📚 {self.course_name}")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Progress Text
        self.progress_label = QLabel("Progress: 0%")
        self.progress_label.setFont(
            QFont("Segoe UI", 14, QFont.Bold)
        )
        self.progress_label.setAlignment(Qt.AlignCenter)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Lesson List
        self.lesson_list = QListWidget()

        for lesson in self.lessons:
            self.lesson_list.addItem("⬜ " + lesson)

        self.lesson_list.itemClicked.connect(
            self.select_lesson
        )

        # Current Lesson
        self.lesson_title = QLabel(
            "Select a lesson to begin"
        )

        self.lesson_title.setFont(
            QFont("Segoe UI", 18, QFont.Bold)
        )

        self.lesson_title.setAlignment(Qt.AlignCenter)

        # Lesson Content
        self.lesson_content = QLabel(
            "Choose a lesson from the list."
        )

        self.lesson_content.setWordWrap(True)
        self.lesson_content.setAlignment(Qt.AlignCenter)
        self.lesson_content.setFont(
            QFont("Segoe UI", 13)
        )

        # Buttons
        previous_button = QPushButton("◀ Previous")

        start_button = QPushButton("▶ Start Lesson")

        next_button = QPushButton("Next ▶")

        complete_button = QPushButton(
            "✅ Mark as Completed"
        )

        previous_button.clicked.connect(
            self.previous_lesson
        )

        start_button.clicked.connect(
            self.start_lesson
        )

        next_button.clicked.connect(
            self.next_lesson
        )

        complete_button.clicked.connect(
            self.complete_lesson
        )

        # Navigation Layout
        navigation = QHBoxLayout()

        navigation.addWidget(previous_button)
        navigation.addWidget(start_button)
        navigation.addWidget(next_button)

        # Main Layout
        layout.addWidget(title)

        layout.addWidget(
            self.progress_label
        )

        layout.addWidget(
            self.progress_bar
        )

        layout.addWidget(
            self.lesson_list
        )

        layout.addWidget(
            self.lesson_title
        )

        layout.addWidget(
            self.lesson_content
        )

        layout.addLayout(
            navigation
        )

        layout.addWidget(
            complete_button
        )

        self.setLayout(layout)

        # Styling
        self.setStyleSheet("""

            QWidget {
                background: #111827;
                color: white;
            }

            QLabel {
                color: white;
            }

            QListWidget {
                background: #1F2937;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }

            QListWidget::item {
                padding: 10px;
            }

            QListWidget::item:selected {
                background: #2563EB;
                border-radius: 6px;
            }

            QProgressBar {
                height: 22px;
                border-radius: 10px;
                background: #374151;
                color: white;
                font-size: 13px;
                font-weight: bold;
                text-align: center;
            }

            QProgressBar::chunk {
                background: #3B82F6;
                border-radius: 10px;
            }

            QPushButton {
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #3B82F6;
            }

        """)

    # -------------------------
    # Select Lesson
    # -------------------------

    def select_lesson(self, item):

        self.current_lesson = (
            self.lesson_list.row(item)
        )

        self.start_lesson()

    # -------------------------
    # Start Lesson
    # -------------------------

    def start_lesson(self):

        lesson = self.lessons[
            self.current_lesson
        ]

        self.lesson_title.setText(
            lesson
        )

        self.lesson_content.setText(
            f"You are currently learning: {lesson}\n\n"
            f"This is the {self.course_name} course.\n\n"
            "Study this topic and then click "
            "'Mark as Completed' when you finish."
        )

    # -------------------------
    # Next Lesson
    # -------------------------

    def next_lesson(self):

        if self.current_lesson < len(self.lessons) - 1:

            self.current_lesson += 1

            self.lesson_list.setCurrentRow(
                self.current_lesson
            )

            self.start_lesson()

    # -------------------------
    # Previous Lesson
    # -------------------------

    def previous_lesson(self):

        if self.current_lesson > 0:

            self.current_lesson -= 1

            self.lesson_list.setCurrentRow(
                self.current_lesson
            )

            self.start_lesson()

    # -------------------------
    # Complete Lesson
    # -------------------------

    def complete_lesson(self):

        self.completed_lessons.add(
            self.current_lesson
        )

        item = self.lesson_list.item(
            self.current_lesson
        )

        item.setText(
            "✅ " +
            self.lessons[self.current_lesson]
        )

        progress = int(
            len(self.completed_lessons)
            / len(self.lessons)
            * 100
        )

        self.progress_bar.setValue(
            progress
        )

        self.progress_label.setText(
            f"Progress: {progress}%"
        )

        self.save_progress(progress)