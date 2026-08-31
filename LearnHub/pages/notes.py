import sqlite3

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QMessageBox
)

from PyQt5.QtGui import QFont


class NotesPage(QWidget):

    def __init__(self, username):
        super().__init__()

        self.username = username

        self.initUI()
        self.load_notes()

        self.notes_list.itemClicked.connect(self.open_note)

    def initUI(self):

        layout = QVBoxLayout()

        # Heading
        heading = QLabel("📋 My Notes")
        heading.setFont(
            QFont("Segoe UI", 26, QFont.Bold)
        )

        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Note Title"
        )
        self.title_input.setFont(
            QFont("Segoe UI", 14)
        )

        # Content
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText(
            "Write your notes here..."
        )
        self.content_input.setFont(
            QFont("Segoe UI", 13)
        )

        # Buttons
        save_button = QPushButton(
            "💾 Save Note"
        )

        clear_button = QPushButton(
            "🗑 Clear"
        )

        save_button.clicked.connect(
            self.save_note
        )

        clear_button.clicked.connect(
            self.clear_note
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)

        # Saved Notes
        notes_label = QLabel(
            "Saved Notes"
        )

        notes_label.setFont(
            QFont("Segoe UI", 18, QFont.Bold)
        )

        self.notes_list = QListWidget()

        # Layout
        layout.addWidget(heading)

        layout.addSpacing(15)

        layout.addWidget(
            self.title_input
        )

        layout.addWidget(
            self.content_input
        )

        layout.addLayout(
            button_layout
        )

        layout.addSpacing(20)

        layout.addWidget(
            notes_label
        )

        layout.addWidget(
            self.notes_list
        )

        self.setLayout(layout)

        # Style
        self.setStyleSheet("""

            QWidget {
                background: #111827;
                color: white;
            }

            QLabel {
                color: white;
            }

            QLineEdit,
            QTextEdit {
                background: #1F2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 10px;
                padding: 10px;
            }

            QLineEdit:focus,
            QTextEdit:focus {
                border: 2px solid #3B82F6;
            }

            QPushButton {
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #3B82F6;
            }

            QListWidget {
                background: #1F2937;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }

            QListWidget::item {
                padding: 10px;
            }

            QListWidget::item:selected {
                background: #2563EB;
                border-radius: 6px;
            }

        """)

    # -------------------------
    # Save Note
    # -------------------------

    def save_note(self):

        title = self.title_input.text().strip()

        content = self.content_input.toPlainText().strip()

        if not title or not content:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both a title and note content."
            )

            return

        conn = sqlite3.connect(
            "learnhub.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notes
            (username, title, content)
            VALUES (?, ?, ?)
        """, (
            self.username,
            title,
            content
        ))

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Success",
            "Note saved successfully!"
        )

        self.clear_note()

        self.load_notes()

    # -------------------------
    # Load Notes
    # -------------------------

    def load_notes(self):

        self.notes_list.clear()

        conn = sqlite3.connect(
            "learnhub.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title
            FROM notes
            WHERE username = ?
            ORDER BY id DESC
        """, (self.username,))

        notes = cursor.fetchall()

        conn.close()

        for note_id, title in notes:

            self.notes_list.addItem(
                f"📝 {title}"
            )

    def open_note(self, item):

        title = item.text().replace("📝 ", "")

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT content
            FROM notes
            WHERE username = ? AND title = ?
        """, (self.username, title))

        result = cursor.fetchone()

        conn.close()

        if result:

            self.title_input.setText(title)

            self.content_input.setPlainText(
                result[0]
            )

    # -------------------------
    # Clear
    # -------------------------

    def clear_note(self):

        self.title_input.clear()

        self.content_input.clear()