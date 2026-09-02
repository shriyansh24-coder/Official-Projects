# 🎵 MusicHub — Music Playlist Manager

A desktop Music Playlist Manager built with **Python, PyQt5 and pygame-ce**.

MusicHub provides a simple and modern **Radiant Purple-Black** interface for managing and playing personal music playlists.

---

## ✨ Features

- 🎵 Add songs to your playlist
- 🗑️ Delete songs
- 🧹 Clear entire playlist
- 🔎 Search songs
- ▶️ Play music
- ⏸️ Pause music
- ▶️ Resume paused music
- ⏹️ Stop playback
- ⏮️ Previous song
- ⏭️ Next song
- 🔀 Shuffle playlist
- 🔊 Volume control
- 🔁 Repeat current song
- ⏭️ Automatically play the next song
- 💾 Automatically save playlist changes
- 📂 Restore playlist after restarting the application
- 🛡️ Duplicate-song protection
- ⚠️ Detect missing audio files
- 🌌 Radiant Purple-Black dark UI

---

## 🛠️ Technologies Used

- **Python**
- **PyQt5** — graphical user interface
- **pygame-ce** — audio playback
- **JSON** — playlist persistence

---

## 📁 Project Structure

```text
MusicPlaylistManager/
│
├── assets/
│
├── data/
│
├── modules/
│   ├── playlist.py
│   ├── player.py
│   └── storage.py
│
├── ui/
│   ├── main_window.py
│   └── styles.py
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore