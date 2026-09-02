import random
import os
import pygame

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QMessageBox,
    QLineEdit,
    QSlider,
    QCheckBox
)

from PyQt5.QtCore import Qt, QTimer

from modules.playlist import AddSongDialog
from modules.storage import save_playlist, load_playlist


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        pygame.mixer.init()

        self.is_paused = False
        self.current_file = None

        self.setWindowTitle("Music Playlist Manager")
        self.setGeometry(100, 100, 1200, 700)

        self.song_timer = QTimer()
        self.song_timer.timeout.connect(
            self.check_song_finished
        )
        self.song_timer.start(500)

        self.create_ui()

    # ==================================================
    # UI
    # ==================================================

    def create_ui(self):

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_widget.setLayout(main_layout)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QFrame()
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(
            20, 25, 20, 25
        )
        sidebar_layout.setSpacing(10)

        sidebar.setLayout(sidebar_layout)

        logo = QLabel("🎵 MusicHub")
        logo.setObjectName("logo")

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(25)

        self.home_button = QPushButton("🏠  Home")
        self.songs_button = QPushButton("🎵  My Songs")
        add_button = QPushButton("➕  Add Song")
        shuffle_button = QPushButton("🔀  Shuffle")
        delete_button = QPushButton("🗑️  Delete Song")
        clear_button = QPushButton("🧹  Clear Playlist")
        self.settings_button = QPushButton("⚙️  Settings")

        self.home_button.clicked.connect(
            self.show_home
        )

        self.songs_button.clicked.connect(
            self.show_all_songs
        )

        add_button.clicked.connect(
            self.add_song
        )

        shuffle_button.clicked.connect(
            self.shuffle_playlist
        )

        delete_button.clicked.connect(
            self.delete_song
        )

        clear_button.clicked.connect(
            self.clear_playlist
        )

        self.settings_button.clicked.connect(
            self.show_settings
        )

        sidebar_layout.addWidget(
            self.home_button
        )
        sidebar_layout.addWidget(
            self.songs_button
        )
        sidebar_layout.addWidget(
            add_button
        )
        sidebar_layout.addWidget(
            shuffle_button
        )
        sidebar_layout.addWidget(
            delete_button
        )
        sidebar_layout.addWidget(
            clear_button
        )

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(
            self.settings_button
        )

        # =========================
        # CONTENT
        # =========================

        self.content = QFrame()

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(
            35, 30, 35, 25
        )
        self.content_layout.setSpacing(12)

        self.content.setLayout(
            self.content_layout
        )

        # Title
        self.title = QLabel("My Playlist")
        self.title.setObjectName(
            "page_title"
        )

        self.subtitle = QLabel(
            "Manage and enjoy your favorite songs"
        )
        self.subtitle.setObjectName(
            "subtitle"
        )

        self.current_song_label = QLabel(
            "No song selected"
        )
        self.current_song_label.setObjectName(
            "current_song"
        )

        self.content_layout.addWidget(
            self.title
        )

        self.content_layout.addWidget(
            self.subtitle
        )

        self.content_layout.addWidget(
            self.current_song_label
        )

        # =========================
        # SEARCH
        # =========================

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "🔎 Search songs..."
        )

        self.search_box.textChanged.connect(
            self.search_songs
        )

        self.content_layout.addWidget(
            self.search_box
        )

        # =========================
        # PLAYLIST
        # =========================

        self.playlist = QListWidget()
        self.playlist.setObjectName(
            "playlist"
        )

        self.playlist.currentItemChanged.connect(
            self.song_selected
        )

        self.load_saved_playlist()

        self.content_layout.addWidget(
            self.playlist
        )

        # =========================
        # CONTROLS
        # =========================

        controls = QHBoxLayout()
        controls.setSpacing(10)

        self.previous_button = QPushButton("⏮")
        self.play_button = QPushButton("▶")
        self.pause_button = QPushButton("⏸")
        self.stop_button = QPushButton("⏹")
        self.next_button = QPushButton("⏭")

        self.previous_button.setObjectName(
            "control_button"
        )

        self.play_button.setObjectName(
            "play_button"
        )

        self.pause_button.setObjectName(
            "control_button"
        )

        self.stop_button.setObjectName(
            "control_button"
        )

        self.next_button.setObjectName(
            "control_button"
        )

        self.previous_button.clicked.connect(
            self.previous_song
        )

        self.play_button.clicked.connect(
            self.play_song
        )

        self.pause_button.clicked.connect(
            self.pause_song
        )

        self.stop_button.clicked.connect(
            self.stop_song
        )

        self.next_button.clicked.connect(
            self.next_song
        )

        controls.addStretch()

        controls.addWidget(
            self.previous_button
        )

        controls.addWidget(
            self.play_button
        )

        controls.addWidget(
            self.pause_button
        )

        controls.addWidget(
            self.stop_button
        )

        controls.addWidget(
            self.next_button
        )

        controls.addStretch()

        self.content_layout.addLayout(
            controls
        )

        # =========================
        # VOLUME
        # =========================

        volume_layout = QHBoxLayout()

        volume_label = QLabel(
            "🔊 Volume"
        )

        self.volume_slider = QSlider(
            Qt.Horizontal
        )

        self.volume_slider.setRange(
            0, 100
        )

        self.volume_slider.setValue(
            70
        )

        self.volume_slider.valueChanged.connect(
            self.change_volume
        )

        volume_layout.addWidget(
            volume_label
        )

        volume_layout.addWidget(
            self.volume_slider
        )

        self.content_layout.addLayout(
            volume_layout
        )

        # =========================
        # REPEAT
        # =========================

        self.repeat_checkbox = QCheckBox(
            "🔁 Repeat current song"
        )

        self.content_layout.addWidget(
            self.repeat_checkbox
        )

        # =========================
        # ADD EVERYTHING
        # =========================

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            self.content
        )

        pygame.mixer.music.set_volume(
            0.7
        )

    # ==================================================
    # HOME
    # ==================================================

    def show_home(self):

        self.title.setText(
            "🎵 MusicHub"
        )

        self.subtitle.setText(
            "Welcome to your personal music playlist manager"
        )

        self.current_song_label.setText(
            f"Songs in playlist: {self.playlist.count()}"
        )

        self.search_box.clear()

    # ==================================================
    # MY SONGS
    # ==================================================

    def show_all_songs(self):

        self.title.setText(
            "My Songs"
        )

        self.subtitle.setText(
            f"You have {self.playlist.count()} song(s) in your playlist"
        )

        self.current_song_label.setText(
            "Select a song to play"
        )

        self.search_box.clear()

    # ==================================================
    # SETTINGS
    # ==================================================

    def show_settings(self):

        QMessageBox.information(
            self,
            "Settings",
            "MusicHub Settings\n\n"
            "Playlist saving: Enabled\n"
            "Automatic Next: Enabled\n"
            "Audio Player: pygame\n"
            "Theme: Radiant Purple-Black"
        )

    # ==================================================
    # ADD SONG
    # ==================================================

    def add_song(self):

        dialog = AddSongDialog(self)

        if dialog.exec_():

            song_name = dialog.song_name.strip()
            file_path = dialog.file_path

            # Prevent duplicate file
            for i in range(
                self.playlist.count()
            ):

                existing = self.playlist.item(i)

                if existing.data(
                    Qt.UserRole
                ) == file_path:

                    QMessageBox.warning(
                        self,
                        "Duplicate Song",
                        "This song is already in your playlist."
                    )

                    return

            item = QListWidgetItem(
                f"🎵  {song_name}"
            )

            item.setData(
                Qt.UserRole,
                file_path
            )

            self.playlist.addItem(
                item
            )

            self.save_current_playlist()

            self.current_song_label.setText(
                f"Added: {song_name}"
            )

    # ==================================================
    # DELETE
    # ==================================================

    def delete_song(self):

        row = self.playlist.currentRow()

        if row == -1:

            QMessageBox.warning(
                self,
                "No Song Selected",
                "Please select a song to delete."
            )

            return

        item = self.playlist.item(row)

        file_path = item.data(
            Qt.UserRole
        )

        if file_path == self.current_file:

            pygame.mixer.music.stop()

            self.current_file = None
            self.is_paused = False

        self.playlist.takeItem(
            row
        )

        self.current_song_label.setText(
            "No song selected"
        )

        self.save_current_playlist()

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_playlist(self):

        if self.playlist.count() == 0:
            return

        answer = QMessageBox.question(
            self,
            "Clear Playlist",
            "Are you sure you want to remove all songs?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer == QMessageBox.Yes:

            pygame.mixer.music.stop()

            self.current_file = None
            self.is_paused = False

            self.playlist.clear()

            self.current_song_label.setText(
                "Playlist cleared"
            )

            self.save_current_playlist()

    # ==================================================
    # SELECTION
    # ==================================================

    def song_selected(
        self,
        current,
        previous
    ):

        if current:

            self.current_song_label.setText(
                f"Now Selected: {current.text()}"
            )

            self.is_paused = False

        else:

            self.current_song_label.setText(
                "No song selected"
            )

    # ==================================================
    # PLAY
    # ==================================================

    def play_song(self):

        current_item = (
            self.playlist.currentItem()
        )

        if current_item is None:

            QMessageBox.warning(
                self,
                "No Song Selected",
                "Please select a song first."
            )

            return

        file_path = current_item.data(
            Qt.UserRole
        )

        if not file_path:

            QMessageBox.warning(
                self,
                "Audio File Missing",
                "This song has no audio file."
            )

            return

        # File was moved/deleted
        if not os.path.exists(file_path):

            QMessageBox.warning(
                self,
                "File Not Found",
                "The audio file could not be found.\n\n"
                "It may have been moved or deleted."
            )

            return

        try:

            # Resume
            if (
                self.is_paused
                and file_path == self.current_file
            ):

                pygame.mixer.music.unpause()

                self.is_paused = False

                self.current_song_label.setText(
                    f"▶ Playing: {current_item.text()}"
                )

                return

            pygame.mixer.music.load(
                file_path
            )

            pygame.mixer.music.play()

            self.current_file = file_path
            self.is_paused = False

            self.current_song_label.setText(
                f"▶ Playing: {current_item.text()}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Playback Error",
                f"Could not play this file.\n\n{error}"
            )

    # ==================================================
    # PAUSE
    # ==================================================

    def pause_song(self):

        if pygame.mixer.music.get_busy():

            pygame.mixer.music.pause()

            self.is_paused = True

            self.current_song_label.setText(
                "⏸ Music Paused"
            )

    # ==================================================
    # STOP
    # ==================================================

    def stop_song(self):

        pygame.mixer.music.stop()

        self.is_paused = False
        self.current_file = None

        self.current_song_label.setText(
            "⏹ Music Stopped"
        )

    # ==================================================
    # PREVIOUS
    # ==================================================

    def previous_song(self):

        count = self.playlist.count()

        if count == 0:
            return

        current_index = (
            self.playlist.currentRow()
        )

        if current_index <= 0:
            new_index = count - 1
        else:
            new_index = current_index - 1

        self.playlist.setCurrentRow(
            new_index
        )

        self.play_song()

    # ==================================================
    # NEXT
    # ==================================================

    def next_song(self):

        count = self.playlist.count()

        if count == 0:
            return

        current_index = (
            self.playlist.currentRow()
        )

        if current_index == -1:
            new_index = 0

        elif current_index >= count - 1:
            new_index = 0

        else:
            new_index = current_index + 1

        self.playlist.setCurrentRow(
            new_index
        )

        self.play_song()

    # ==================================================
    # SHUFFLE
    # ==================================================

    def shuffle_playlist(self):

        if self.playlist.count() < 2:
            return

        songs = []

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(i)

            songs.append({
                "text": item.text(),
                "file": item.data(Qt.UserRole)
            })

        random.shuffle(songs)

        self.playlist.clear()

        for song in songs:

            item = QListWidgetItem(
                song["text"]
            )

            item.setData(
                Qt.UserRole,
                song["file"]
            )

            self.playlist.addItem(
                item
            )

        self.save_current_playlist()

        self.current_song_label.setText(
            "🔀 Playlist Shuffled"
        )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_songs(self, text):

        text = text.lower().strip()

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(i)

            matches = (
                text in item.text().lower()
            )

            item.setHidden(
                not matches
            )

    # ==================================================
    # VOLUME
    # ==================================================

    def change_volume(self, value):

        pygame.mixer.music.set_volume(
            value / 100
        )

    # ==================================================
    # AUTO NEXT
    # ==================================================

    def check_song_finished(self):

        if not self.current_file:
            return

        if self.is_paused:
            return

        if not pygame.mixer.music.get_busy():

            if (
                self.repeat_checkbox.isChecked()
            ):

                self.play_song()

            else:

                self.next_song()

    # ==================================================
    # SAVE
    # ==================================================

    def save_current_playlist(self):

        songs = []

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(i)

            song_name = item.text().replace(
                "🎵  ",
                "",
                1
            )

            file_path = item.data(
                Qt.UserRole
            )

            songs.append({
                "name": song_name,
                "file": file_path
            })

        save_playlist(
            songs
        )

    # ==================================================
    # LOAD
    # ==================================================

    def load_saved_playlist(self):

        songs = load_playlist()

        for song in songs:

            item = QListWidgetItem(
                f"🎵  {song['name']}"
            )

            item.setData(
                Qt.UserRole,
                song.get("file")
            )

            self.playlist.addItem(
                item
            )

    # ==================================================
    # CLOSE
    # ==================================================

    def closeEvent(self, event):

        self.save_current_playlist()

        self.song_timer.stop()

        pygame.mixer.music.stop()

        pygame.mixer.quit()

        event.accept()