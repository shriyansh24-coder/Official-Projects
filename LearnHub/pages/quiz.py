import sqlite3
import random

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QFrame,
    QButtonGroup,
    QMessageBox
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class QuizPage(QWidget):

    def __init__(self, username):
        super().__init__()

        self.username = username

        # Original question bank
        self.question_bank = [

            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["function", "def", "define", "fun"],
                "answer": "def"
            },

            {
                "question": "Which symbol is used for comments in Python?",
                "options": ["//", "#", "/*", "--"],
                "answer": "#"
            },

            {
                "question": "Which data type stores True or False?",
                "options": ["String", "Integer", "Boolean", "Float"],
                "answer": "Boolean"
            },

            {
                "question": "Which function is used to display output in Python?",
                "options": ["display()", "show()", "print()", "output()"],
                "answer": "print()"
            },

            {
                "question": "Which operator is used for exponentiation in Python?",
                "options": ["^", "**", "//", "%%"],
                "answer": "**"
            },

            {
                "question": "Which collection is ordered and changeable?",
                "options": ["Tuple", "Set", "List", "Dictionary"],
                "answer": "List"
            },

            {
                "question": "Which keyword is used to create a loop over a sequence?",
                "options": ["repeat", "for", "loop", "iterate"],
                "answer": "for"
            },

            {
                "question": "Which method adds an item to the end of a list?",
                "options": ["add()", "insert()", "append()", "push()"],
                "answer": "append()"
            },

            {
                "question": "What is the correct file extension for Python files?",
                "options": [".python", ".pt", ".py", ".pyt"],
                "answer": ".py"
            },

            {
                "question": "Which keyword is used to create a class in Python?",
                "options": ["object", "class", "define", "struct"],
                "answer": "class"
            }
        ]

        self.current_question = 0
        self.score = 0

        # Stores user's selected answer for every question
        self.user_answers = {}

        # Stores questions marked for later
        self.marked_questions = set()

        self.initUI()

        self.start_quiz()

    # =========================================================
    # UI
    # =========================================================

    def initUI(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            25, 10, 15, 10
        )

        main_layout.setSpacing(12)

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QHBoxLayout()
        header.setContentsMargins(0 , 0 , 0 , 0)

        self.title = QLabel("🧠 Python Quiz")

        self.title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        self.title.setContentsMargins(
            2, 2, 2, 2
        )

        self.score_label = QLabel(
            "Score: 0"
        )

        self.score_label.setFont(
            QFont(
                "Segoe UI",
                14,
                QFont.Bold
            )
        )

        self.score_label.setContentsMargins(
            2, 2, 2, 2
        )

        header.addWidget(
            self.title
        )

        header.addStretch()

        header.addWidget(
            self.score_label
        )

        header_widget = QWidget()
        header_widget.setLayout(header)
        header_widget.setFixedHeight(45)

        main_layout.addWidget(
            header_widget
        )

        # -----------------------------------------------------
        # Question Counter
        # -----------------------------------------------------

        self.question_label = QLabel()
        self.question_label.setFixedHeight(28)

        self.question_label.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Bold
            )
        )

        self.question_label.setContentsMargins(
            2, 2, 2, 2
        )

        main_layout.addWidget(
            self.question_label
        )

        # -----------------------------------------------------
        # Progress Bar
        # -----------------------------------------------------

        self.progress_bar = QProgressBar()

        self.progress_bar.setTextVisible(
            False
        )

        self.progress_bar.setFixedHeight(
            8
        )

        main_layout.addWidget(
            self.progress_bar
        )

        # -----------------------------------------------------
        # Question Card
        # -----------------------------------------------------

        question_card = QFrame()

        question_card.setObjectName(
            "questionCard"
        )

        question_layout = QVBoxLayout()

        question_layout.setContentsMargins(
            20, 20, 20, 20
        )

        self.question_text = QLabel()

        self.question_text.setWordWrap(
            True
        )

        self.question_text.setAlignment(
            Qt.AlignCenter
        )

        self.question_text.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Bold
            )
        )

        question_layout.addWidget(
            self.question_text
        )

        question_card.setLayout(
            question_layout
        )

        main_layout.addWidget(
            question_card
        )

        # -----------------------------------------------------
        # Answer Buttons
        # -----------------------------------------------------

        self.answer_group = QButtonGroup(
            self
        )

        self.answer_buttons = []

        answers_layout = QVBoxLayout()

        answers_layout.setSpacing(
            10
        )

        for i in range(4):

            button = QPushButton()

            button.setMinimumHeight(
                50
            )

            button.setFont(
                QFont(
                    "Segoe UI",
                    15
                )
            )

            button.setCheckable(
                True
            )

            self.answer_group.addButton(
                button,
                i
            )

            self.answer_buttons.append(
                button
            )

            answers_layout.addWidget(
                button
            )

        main_layout.addLayout(
            answers_layout
        )

        # -----------------------------------------------------
        # Navigation
        # -----------------------------------------------------

        navigation = QHBoxLayout()

        self.previous_button = QPushButton(
            "← Previous"
        )

        self.mark_button = QPushButton(
            "🔖 Mark for Later"
        )

        self.next_button = QPushButton(
            "Next →"
        )

        self.previous_button.setMinimumHeight(42)
        self.mark_button.setMinimumHeight(42)
        self.next_button.setMinimumHeight(42)

        self.previous_button.setMinimumWidth(160)
        self.mark_button.setMinimumWidth(160)
        self.next_button.setMinimumWidth(160)

        self.previous_button.setFont(QFont("Segoe UI" , 13 , QFont.Bold))
        self.mark_button.setFont(QFont("Segoe UI" , 13 , QFont.Bold))
        self.next_button.setFont(QFont("Segoe UI" , 13 , QFont.Bold))

        self.previous_button.clicked.connect(
            self.previous_question
        )

        self.mark_button.clicked.connect(
            self.mark_for_later
        )

        self.next_button.clicked.connect(
            self.next_question
        )

        navigation.addWidget(
            self.previous_button
        )

        navigation.addStretch()

        navigation.addWidget(
            self.mark_button
        )

        navigation.addStretch()

        navigation.addWidget(
            self.next_button
        )

        main_layout.addLayout(
            navigation
        )

        self.setLayout(
            main_layout
        )

        # -----------------------------------------------------
        # Styling
        # -----------------------------------------------------

        self.setStyleSheet("""

            QWidget {
                background: #111827;
                color: white;
            }

            QLabel {
                color: white;
            }

            QFrame#questionCard {
                background: #1F2937;
                border: 1px solid #374151;
                border-radius: 14px;
            }

            QProgressBar {
                background: #374151;
                border: none;
                border-radius: 4px;
            }

            QProgressBar::chunk {
                background: #2563EB;
                border-radius: 4px;
            }

            QPushButton {
                background: #1F2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 9px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                background: #263449;
                border: 2px solid #3B82F6;
            }

            QPushButton:checked {
                background: #2563EB;
                border: 2px solid #3B82F6;
            }

            QPushButton#correct {
                background: #059669;
                border: 2px solid #10B981;
            }

            QPushButton#wrong {
                background: #DC2626;
                border: 2px solid #EF4444;
            }

            QPushButton#marked {
                background: #92400E;
                border: 2px solid #F59E0B;
            }

            QPushButton#nextButton {
                background: #2563EB;
                border: none;
            }

            QPushButton#nextButton:hover {
                background: #3B82F6;
            }

        """)

        self.next_button.setObjectName(
            "nextButton"
        )

    # =========================================================
    # Start / Randomize Quiz
    # =========================================================

    def start_quiz(self):

        # Make a fresh copy
        self.questions = [
            {
                "question": q["question"],
                "options": q["options"][:],
                "answer": q["answer"]
            }
            for q in self.question_bank
        ]

        # Randomize question order
        random.shuffle(
            self.questions
        )

        # Randomize options
        for question in self.questions:

            random.shuffle(
                question["options"]
            )

        self.current_question = 0

        self.score = 0

        self.user_answers = {}

        self.marked_questions = set()

        self.score_label.setText(
            "Score: 0"
        )

        self.show_question()

    # =========================================================
    # Show Question
    # =========================================================

    def show_question(self):

        question = self.questions[
            self.current_question
        ]

        total = len(
            self.questions
        )

        number = (
            self.current_question + 1
        )

        self.question_label.setText(
            f"Question {number} / {total}"
        )

        self.progress_bar.setValue(
            int(number / total * 100)
        )

        self.question_text.setText(
            question["question"]
        )

        # Reset buttons
        for i, button in enumerate(
            self.answer_buttons
        ):

            button.setEnabled(
                True
            )

            button.setObjectName(
                ""
            )

            button.setChecked(
                False
            )

            button.setText(
                f"{chr(65 + i)}. "
                f"{question['options'][i]}"
            )

        # Restore previous answer
        if self.current_question in self.user_answers:

            saved_answer = self.user_answers[
                self.current_question
            ]

            for i, option in enumerate(
                question["options"]
            ):

                if option == saved_answer:

                    self.answer_buttons[
                        i
                    ].setChecked(
                        True
                    )

        # Mark button
        if (
            self.current_question
            in self.marked_questions
        ):

            self.mark_button.setText(
                "🔖 Marked"
            )

            self.mark_button.setObjectName(
                "marked"
            )

        else:

            self.mark_button.setText(
                "🔖 Mark for Later"
            )

            self.mark_button.setObjectName(
                ""
            )

        # Previous button
        self.previous_button.setEnabled(
            self.current_question > 0
        )

        # Last question
        if (
            self.current_question
            == total - 1
        ):

            self.next_button.setText(
                "Finish Quiz ✓"
            )

        else:

            self.next_button.setText(
                "Next →"
            )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

    # =========================================================
    # Save Current Answer
    # =========================================================

    def save_current_answer(self):

        selected = (
            self.answer_group.checkedId()
        )

        if selected == -1:
            return

        question = self.questions[
            self.current_question
        ]

        selected_answer = (
            question["options"][selected]
        )

        self.user_answers[
            self.current_question
        ] = selected_answer

    # =========================================================
    # Previous
    # =========================================================

    def previous_question(self):

        self.save_current_answer()

        if self.current_question > 0:

            self.current_question -= 1

            self.show_question()

    # =========================================================
    # Next
    # =========================================================

    def next_question(self):

        self.save_current_answer()

        if (
            self.current_question
            < len(self.questions) - 1
        ):

            self.current_question += 1

            self.show_question()

        else:

            self.finish_quiz()

    # =========================================================
    # Mark for Later
    # =========================================================

    def mark_for_later(self):

        self.save_current_answer()

        if self.current_question in self.marked_questions:

            self.marked_questions.remove(
                self.current_question
            )

            self.mark_button.setText(
                "🔖 Mark for Later"
            )

            self.mark_button.setObjectName("")

        else:

            self.marked_questions.add(
                self.current_question
            )

            self.mark_button.setText(
                "🔖 Marked"
            )

            self.mark_button.setObjectName(
                "marked"
            )

        self.mark_button.style().unpolish(
            self.mark_button
        )

        self.mark_button.style().polish(
            self.mark_button
        )

    # =========================================================
    # Finish Quiz
    # =========================================================

    def finish_quiz(self):

        # Make sure the user has answered everything
        unanswered = []

        for i in range(
            len(self.questions)
        ):

            if i not in self.user_answers:

                unanswered.append(
                    i + 1
                )

        if unanswered:

            QMessageBox.warning(
                self,
                "Incomplete Quiz",
                "Please answer all questions "
                "before finishing the quiz."
            )

            self.current_question = (
                unanswered[0] - 1
            )

            self.show_question()

            return

        # Calculate score
        self.score = 0

        for i, question in enumerate(
            self.questions
        ):

            if (
                self.user_answers.get(i)
                == question["answer"]
            ):

                self.score += 1

        percentage = int(
            self.score
            / len(self.questions)
            * 100
        )

        self.save_score(
            self.score
        )

        self.show_result(
            percentage
        )

    # =========================================================
    # Result Screen
    # =========================================================

    def show_result(self, percentage):

        # Remove current quiz widgets
        layout = self.layout()

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.hide()
                widget.deleteLater()

        # -------------------------------------------------
        # Result Layout Settings
        # -------------------------------------------------

        layout.setContentsMargins(
            100, 40, 100, 40
        )

        layout.setSpacing(
            18
        )

        layout.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Trophy
        # -------------------------------------------------

        trophy = QLabel(
            "🏆"
        )

        trophy.setFont(
            QFont(
                "Segoe UI",
                55
            )
        )

        trophy.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title = QLabel(
            "Quiz Completed!"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                28,
                QFont.Bold
            )
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Score
        # -------------------------------------------------

        score = QLabel(
            f"{self.score} / {len(self.questions)}"
        )

        score.setFont(
            QFont(
                "Segoe UI",
                42,
                QFont.Bold
            )
        )

        score.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Percentage
        # -------------------------------------------------

        percentage_label = QLabel(
            f"{percentage}%"
        )

        percentage_label.setFont(
            QFont(
                "Segoe UI",
                24,
                QFont.Bold
            )
        )

        percentage_label.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Message
        # -------------------------------------------------

        if percentage >= 80:

            message = "Excellent Work! 🔥"

        elif percentage >= 60:

            message = "Good Job! Keep Learning! 💪"

        else:

            message = "Keep Practicing! 📚"

        message_label = QLabel(
            message
        )

        message_label.setFont(
            QFont(
                "Segoe UI",
                16
            )
        )

        message_label.setAlignment(
            Qt.AlignCenter
        )

        # -------------------------------------------------
        # Retake Button
        # -------------------------------------------------

        retake_button = QPushButton(
            "🔄 Retake Quiz"
        )

        retake_button.setFont(
            QFont(
                "Segoe UI",
                13
            )
        )

        retake_button.setMinimumHeight(
            45
        )

        retake_button.clicked.connect(
            self.restart_after_result
        )

        # -------------------------------------------------
        # Back Button
        # -------------------------------------------------

        back_button = QPushButton(
            "← Back"
        )

        back_button.setFont(
            QFont(
                "Segoe UI",
                13
            )
        )

        back_button.setMinimumHeight(
            45
        )

        back_button.clicked.connect(
            self.back_from_result
        )

        # -------------------------------------------------
        # Button Styles
        # -------------------------------------------------

        retake_button.setStyleSheet("""
            QPushButton {
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton:hover {
                background: #3B82F6;
            }
        """)

        back_button.setStyleSheet("""
            QPushButton {
                background: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton:hover {
                background: #4B5563;
            }
        """)

        # -------------------------------------------------
        # Add Result Widgets to Existing Layout
        # -------------------------------------------------

        layout.addWidget(
            trophy
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            score
        )

        layout.addWidget(
            percentage_label
        )

        layout.addWidget(
            message_label
        )

        layout.addSpacing(
            15
        )

        layout.addWidget(
            retake_button
        )

        layout.addWidget(
            back_button
        )


    # =========================================================
    # Retake
    # =========================================================

    def restart_after_result(self):

        self.initUI()

        self.start_quiz()

    # =========================================================
    # Back
    # =========================================================

    def back_from_result(self):

        # Close quiz window if it was opened separately
        self.close()

    # =========================================================
    # Save Score
    # =========================================================

    def save_score(self, score):

        conn = sqlite3.connect("learnhub.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO quiz_scores
            (username, course_id, score)
            VALUES (?, ?, ?)
        """, (
            self.username,
            1,
            score
        ))

        conn.commit()
        conn.close()