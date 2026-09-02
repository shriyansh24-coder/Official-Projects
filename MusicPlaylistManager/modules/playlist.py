from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox
)


class AddSongDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Song")
        self.setFixedSize(450, 230)

        self.song_name = ""
        self.file_path = ""

        self.create_ui()

    def create_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Song title
        title_label = QLabel("Song Title")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter song title")

        layout.addWidget(title_label)
        layout.addWidget(self.title_input)

        # Audio file
        file_label = QLabel("Audio File")

        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select an existing audio file")
        self.file_input.setReadOnly(True)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)

        layout.addWidget(file_label)
        layout.addLayout(file_layout)

        # Buttons
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        add_button = QPushButton("Add Song")

        cancel_button.clicked.connect(self.reject)
        add_button.clicked.connect(self.add_song)

        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(add_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.ogg)"
        )

        if file_path:
            self.file_path = file_path
            self.file_input.setText(file_path)

    def add_song(self):

        song_name = self.title_input.text().strip()

        if not song_name:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter a song title."
            )
            return

        if not self.file_path:
            QMessageBox.warning(
                self,
                "No Audio File",
                "Please select an audio file."
            )
            return

        self.song_name = song_name

        self.accept()