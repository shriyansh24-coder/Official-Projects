import os
import wave
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# Load API Key
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# ==========================================
# Audio Constants
# ==========================================

SAMPLE_RATE = 24000
CHANNELS = 1
SAMPLE_WIDTH = 2
BYTES_PER_SECOND = SAMPLE_RATE * SAMPLE_WIDTH

PLAYBACK_CHUNK_SIZE = int(BYTES_PER_SECOND * 0.02)  # 20 ms


# ==========================================
# Streaming / Playback Control
# ==========================================

stop_event = threading.Event()

audio_stream = None

audio_buffer = bytearray()
audio_lock = threading.Lock()

playback_position = 0
generation_active = False
generation_finished = False
playback_paused = False

playback_thread = None
playback_stop_event = threading.Event()


# ==========================================
# Voice Presets
# ==========================================

VOICES = {
    "Puck — Upbeat": "Puck",
    "Kore — Firm": "Kore",
    "Fenrir — Excitable": "Fenrir",
    "Leda — Youthful": "Leda",
    "Aoede — Breezy": "Aoede",
    "Gacrux — Mature": "Gacrux",
    "Achird — Friendly": "Achird",
    "Algieba — Smooth": "Algieba",
    "Enceladus — Breathy": "Enceladus",
    "Sulafat — Warm": "Sulafat",
}


ACCENTS = {
    "American English": "American English",
    "British English": "British English",
    "Indian English": "Indian English",
    "Australian English": "Australian English",
}


STYLES = {
    "Natural": "natural and conversational",
    "Professional": "professional and polished",
    "Friendly": "friendly and warm",
    "Energetic": "energetic and enthusiastic",
    "Calm": "calm and relaxed",
    "Dramatic": "dramatic and expressive",
    "Confident": "confident and authoritative",
}


SPEEDS = {
    "Slow": "slow pace",
    "Normal": "natural pace",
    "Fast": "slightly fast pace",
}


# ==========================================
# Save WAV File
# ==========================================

def save_wav(filename, pcm_data):

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm_data)


# ==========================================
# Audio Helpers
# ==========================================

def get_duration():

    with audio_lock:
        total_bytes = len(audio_buffer)

    return total_bytes / BYTES_PER_SECOND


def get_position():

    with audio_lock:
        position = playback_position

    return position / BYTES_PER_SECOND


def format_time(seconds):

    seconds = max(0, int(seconds))

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"


def update_player_ui():

    try:

        duration = get_duration()
        position = get_position()

        duration_label.config(
            text=format_time(duration)
        )

        position_label.config(
            text=format_time(position)
        )

        progress_scale.config(
            to=max(duration, 0.1)
        )

        progress_var.set(
            min(position, max(duration, 0.1))
        )

    except Exception:
        pass

    root.after(100, update_player_ui)


# ==========================================
# Stop Playback Stream
# ==========================================

def close_audio_stream():

    global audio_stream

    if audio_stream is not None:

        try:
            audio_stream.abort()
        except Exception:
            pass

        try:
            audio_stream.close()
        except Exception:
            pass

        audio_stream = None


# ==========================================
# Playback Worker
# ==========================================

def playback_worker():

    global audio_stream
    global playback_position

    try:

        audio_stream = sd.RawOutputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )

        audio_stream.start()

        while not playback_stop_event.is_set():

            # ----------------------------------
            # Pause
            # ----------------------------------

            if playback_paused:

                try:
                    audio_stream.stop()
                except Exception:
                    pass

                while (
                    playback_paused
                    and not playback_stop_event.is_set()
                ):
                    threading.Event().wait(0.05)

                if playback_stop_event.is_set():
                    break

                try:
                    audio_stream.start()
                except Exception:
                    pass

                continue

            # ----------------------------------
            # Read available audio
            # ----------------------------------

            with audio_lock:

                available = (
                    len(audio_buffer)
                    - playback_position
                )

                if available > 0:

                    amount = min(
                        PLAYBACK_CHUNK_SIZE,
                        available
                    )

                    # Keep complete 16-bit samples
                    amount -= amount % SAMPLE_WIDTH

                    if amount > 0:

                        data = bytes(
                            audio_buffer[
                                playback_position:
                                playback_position + amount
                            ]
                        )

                    else:
                        data = None

                else:
                    data = None

            # ----------------------------------
            # Play audio
            # ----------------------------------

            if data:

                try:

                    audio_stream.write(data)

                    with audio_lock:
                        playback_position += len(data)

                except Exception:

                    if playback_stop_event.is_set():
                        break

                    raise

                continue

            # ----------------------------------
            # No audio available
            # ----------------------------------

            if generation_finished:

                # Gemini has finished AND
                # there is no audio left.
                with audio_lock:
                    at_end = (
                        playback_position
                        >= len(audio_buffer)
                    )

                if at_end:
                    root.after(
                        0,
                        playback_finished
                    )
                    break

            # Gemini is still generating.
            # Wait and check again.
            threading.Event().wait(0.02)

    except Exception as e:

        if not playback_stop_event.is_set():

            root.after(
                0,
                lambda error=str(e):
                status_var.set(
                    f"● Playback error: {error}"
                )
            )

    finally:

        close_audio_stream()


# ==========================================
# Start Playback
# ==========================================

def start_playback():

    global playback_thread
    global playback_paused
    global playback_position

    with audio_lock:

        if len(audio_buffer) == 0:
            return

        # If at the end, restart from beginning
        if playback_position >= len(audio_buffer):
            playback_position = 0

    playback_paused = False

    playback_stop_event.clear()

    if (
        playback_thread is None
        or not playback_thread.is_alive()
    ):

        playback_thread = threading.Thread(
            target=playback_worker,
            daemon=True
        )

        playback_thread.start()

    play_pause_button.config(
        text="⏸ Pause"
    )

    status_var.set(
        "● Playback playing"
    )

    status_label.config(
        fg="#4ade80"
    )


# ==========================================
# Pause Playback
# ==========================================

def pause_playback():

    global playback_paused

    playback_paused = True

    play_pause_button.config(
        text="▶ Play"
    )

    status_var.set(
        "● Playback paused"
    )

    status_label.config(
        fg="#f5b942"
    )

# ==========================================
# Toggle Play / Pause
# ==========================================

def toggle_play_pause():

    with audio_lock:

        has_audio = len(audio_buffer) > 0

    if not has_audio:
        return

    if playback_paused:

        start_playback()

    else:

        if (
            playback_thread is not None
            and playback_thread.is_alive()
        ):
            pause_playback()
        else:
            start_playback()


# ==========================================
# Seek Audio
# ==========================================

def seek_audio(value):

    global playback_position

    try:

        seconds = float(value)

        new_position = int(
            seconds * BYTES_PER_SECOND
        )

        # Align to complete 16-bit samples
        new_position -= (
            new_position % SAMPLE_WIDTH
        )

        with audio_lock:

            new_position = max(
                0,
                min(
                    new_position,
                    len(audio_buffer)
                )
            )

            playback_position = new_position

    except Exception:
        pass


# ==========================================
# Rewind 10 Seconds
# ==========================================

def rewind_10():

    global playback_position

    with audio_lock:

        playback_position = max(
            0,
            playback_position - (
                10 * BYTES_PER_SECOND
            )
        )


# ==========================================
# Forward 10 Seconds
# ==========================================

def forward_10():

    global playback_position

    with audio_lock:

        playback_position = min(
            len(audio_buffer),
            playback_position + (
                10 * BYTES_PER_SECOND
            )
        )


# ==========================================
# Playback Finished
# ==========================================

def playback_finished():

    global playback_paused

    playback_paused = True

    play_pause_button.config(
        text="▶ Play"
    )

    status_var.set(
        "● Playback complete"
    )

    status_label.config(
        fg="#888f9b"
    )


# ==========================================
# Stop Generation
# ==========================================

def stop_speech():

    global generation_active
    global playback_paused

    stop_event.set()

    generation_active = False

    playback_paused = True

    playback_stop_event.set()

    close_audio_stream()

    play_pause_button.config(
        text="▶ Play"
    )

    status_var.set(
        "● Stopping..."
    )

    status_label.config(
        fg="#f5b942"
    )


# ==========================================
# Reset Audio Buffer
# ==========================================

def reset_audio():

    global playback_position
    global generation_finished
    global generation_active
    global playback_paused

    playback_stop_event.set()

    close_audio_stream()

    with audio_lock:

        audio_buffer.clear()
        playback_position = 0

    # Give the previous playback thread
    # a moment to exit cleanly.
    threading.Event().wait(0.05)

    playback_stop_event.clear()

    generation_finished = False
    generation_active = False
    playback_paused = False

    play_pause_button.config(
        text="▶ Play"
    )

    progress_var.set(0)

    duration_label.config(
        text="00:00"
    )

    position_label.config(
        text="00:00"
    )


# ==========================================
# Generate Speech
# ==========================================

def generate_speech():

    global generation_active
    global generation_finished

    stop_event.clear()

    text = text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        messagebox.showwarning(
            "No Text",
            "Please enter some text first."
        )

        return

    if not API_KEY:

        messagebox.showerror(
            "API Key Missing",
            "GEMINI_API_KEY was not found.\n\n"
            "Create a .env file and add your Gemini API key."
        )

        return

    voice_name = VOICES[
        voice_var.get()
    ]

    accent = ACCENTS[
        accent_var.get()
    ]

    style = STYLES[
        style_var.get()
    ]

    speed = SPEEDS[
        speed_var.get()
    ]

    prompt = f"""
Read the following text aloud.

Use a {accent} accent.
Speak in a {style} manner.
Use a {speed}.
Keep the pronunciation clear and natural.

Text:
{text}
"""

    output_file = filedialog.asksaveasfilename(
        title="Save Generated Speech",
        defaultextension=".wav",
        filetypes=[
            ("WAV Audio", "*.wav")
        ]
    )

    if not output_file:
        return

    # --------------------------------------
    # Reset previous audio
    # --------------------------------------

    reset_audio()

    generation_active = True
    generation_finished = False

    generate_button.config(
        state="disabled"
    )

    stop_button.config(
        state="normal"
    )

    status_var.set(
        "● Connecting to Gemini..."
    )

    status_label.config(
        fg="#f5b942"
    )

    thread = threading.Thread(
        target=generate_audio,
        args=(
            prompt,
            voice_name,
            output_file
        ),
        daemon=True
    )

    thread.start()


# ==========================================
# Gemini Streaming Worker
# ==========================================

def generate_audio(
    prompt,
    voice_name,
    output_file
):

    global generation_active
    global generation_finished

    try:

        audio_chunks = []

        root.after(
            0,
            lambda: status_var.set(
                "● Connecting to Gemini..."
            )
        )

        response_stream = client.models.generate_content_stream(
            model="gemini-3.1-flash-tts-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                )
            )
        )

        first_chunk = True

        for chunk in response_stream:

            # ----------------------------------
            # User pressed Stop
            # ----------------------------------

            if stop_event.is_set():
                break

            try:

                data = (
                    chunk
                    .candidates[0]
                    .content
                    .parts[0]
                    .inline_data
                    .data
                )

            except (
                IndexError,
                AttributeError,
                TypeError
            ):
                continue

            if not data:
                continue

            audio_chunks.append(data)

            # ----------------------------------
            # Add to playback buffer
            # ----------------------------------

            with audio_lock:

                audio_buffer.extend(data)

            # ----------------------------------
            # Start playback automatically
            # ----------------------------------

            if first_chunk:

                first_chunk = False

                root.after(
                    0,
                    start_playback
                )

                root.after(
                    0,
                    lambda: status_var.set(
                        "● Streaming — playback started"
                    )
                )

        # --------------------------------------
        # User stopped generation
        # --------------------------------------

        if stop_event.is_set():

            generation_active = False

            root.after(
                0,
                generation_stopped
            )

            return

        # --------------------------------------
        # Make sure audio exists
        # --------------------------------------

        complete_audio = b"".join(
            audio_chunks
        )

        if not complete_audio:

            raise RuntimeError(
                "Gemini returned no audio data."
            )

        # --------------------------------------
        # Mark generation finished
        # --------------------------------------

        generation_active = False

        # Tell the playback thread that Gemini
        # has finished producing audio.
        generation_finished = True

        # --------------------------------------
        # Save complete audio
        # --------------------------------------

        save_wav(
            output_file,
            complete_audio
        )

        root.after(
            0,
            generation_success,
            output_file
        )

    except Exception as e:

        generation_active = False
        generation_finished = True

        close_audio_stream()

        root.after(
            0,
            generation_error,
            str(e)
        )


# ==========================================
# Stopped
# ==========================================

def generation_stopped():

    generate_button.config(
        state="normal"
    )

    stop_button.config(
        state="disabled"
    )

    status_var.set(
        "● Streaming stopped — audio available"
    )

    status_label.config(
        fg="#f5b942"
    )


# ==========================================
# Success
# ==========================================

def generation_success(output_file):

    generate_button.config(
        state="normal"
    )

    stop_button.config(
        state="disabled"
    )

    status_var.set(
        "● Streaming complete — speech saved"
    )

    status_label.config(
        fg="#4ade80"
    )

    messagebox.showinfo(
        "Success",
        f"Speech generated successfully!\n\n"
        f"Saved to:\n{output_file}"
    )


# ==========================================
# Error
# ==========================================

def generation_error(error):

    generate_button.config(
        state="normal"
    )

    stop_button.config(
        state="disabled"
    )

    status_var.set(
        "● Generation failed"
    )

    status_label.config(
        fg="#ff6b6b"
    )

    messagebox.showerror(
        "Generation Error",
        f"Something went wrong:\n\n{error}"
    )


# ==========================================
# Clear
# ==========================================

def clear_text():

    text_box.delete(
        "1.0",
        tk.END
    )

    status_var.set(
        "● Ready"
    )

    status_label.config(
        fg="#888f9b"
    )


# ==========================================
# GUI
# ==========================================

root = tk.Tk()

root.title(
    "Gemini Voice Studio"
)

root.geometry(
    "850x760"
)

root.minsize(
    760,
    680
)

root.configure(
    bg="#0e1014"
)


# ==========================================
# Style
# ==========================================

style = ttk.Style()

style.theme_use(
    "clam"
)

style.configure(
    "TCombobox",
    fieldbackground="#191c22",
    background="#191c22",
    foreground="white",
    arrowcolor="white",
    borderwidth=0
)

style.map(
    "TCombobox",
    fieldbackground=[
        ("readonly", "#191c22")
    ],
    foreground=[
        ("readonly", "white")
    ]
)


# ==========================================
# Header
# ==========================================

header = tk.Frame(
    root,
    bg="#0e1014"
)

header.pack(
    fill="x",
    padx=45,
    pady=(30, 10)
)


title = tk.Label(
    header,
    text="Gemini Voice Studio",
    font=("Segoe UI", 27, "bold"),
    fg="#ffffff",
    bg="#0e1014"
)

title.pack(
    anchor="w"
)


subtitle = tk.Label(
    header,
    text="Create natural AI speech with Gemini",
    font=("Segoe UI", 11),
    fg="#858c98",
    bg="#0e1014"
)

subtitle.pack(
    anchor="w",
    pady=(4, 0)
)


# ==========================================
# Main Card
# ==========================================

card = tk.Frame(
    root,
    bg="#181b21",
    highlightthickness=1,
    highlightbackground="#292d35"
)

card.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=20
)


# ==========================================
# Text Section
# ==========================================

text_label = tk.Label(
    card,
    text="TEXT",
    font=("Segoe UI", 9, "bold"),
    fg="#8b929e",
    bg="#181b21"
)

text_label.pack(
    anchor="w",
    padx=25,
    pady=(22, 8)
)


text_box = tk.Text(
    card,
    height=7,
    wrap="word",
    font=("Segoe UI", 12),
    bg="#101216",
    fg="#f2f3f5",
    insertbackground="white",
    selectbackground="#3b82f6",
    relief="flat",
    padx=15,
    pady=12
)

text_box.pack(
    fill="both",
    expand=True,
    padx=25
)


# ==========================================
# Options
# ==========================================

options = tk.Frame(
    card,
    bg="#181b21"
)

options.pack(
    fill="x",
    padx=25,
    pady=20
)


def create_option(
    parent,
    label,
    variable,
    values
):

    frame = tk.Frame(
        parent,
        bg="#181b21"
    )

    frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10)
    )

    lbl = tk.Label(
        frame,
        text=label,
        font=("Segoe UI", 9, "bold"),
        fg="#858c98",
        bg="#181b21"
    )

    lbl.pack(
        anchor="w",
        pady=(0, 6)
    )

    combo = ttk.Combobox(
        frame,
        textvariable=variable,
        values=values,
        state="readonly"
    )

    combo.pack(
        fill="x"
    )

    return combo


# ==========================================
# Variables
# ==========================================

voice_var = tk.StringVar(
    value="Puck — Upbeat"
)

accent_var = tk.StringVar(
    value="American English"
)

style_var = tk.StringVar(
    value="Natural"
)

speed_var = tk.StringVar(
    value="Normal"
)


create_option(
    options,
    "VOICE",
    voice_var,
    list(VOICES.keys())
)

create_option(
    options,
    "ACCENT",
    accent_var,
    list(ACCENTS.keys())
)

create_option(
    options,
    "STYLE",
    style_var,
    list(STYLES.keys())
)

create_option(
    options,
    "SPEED",
    speed_var,
    list(SPEEDS.keys())
)


# ==========================================
# Audio Player
# ==========================================

player = tk.Frame(
    card,
    bg="#111419",
    highlightthickness=1,
    highlightbackground="#292d35"
)

player.pack(
    fill="x",
    padx=25,
    pady=(0, 18)
)


player_title = tk.Label(
    player,
    text="AUDIO PLAYER",
    font=("Segoe UI", 9, "bold"),
    fg="#858c98",
    bg="#111419"
)

player_title.pack(
    anchor="w",
    padx=18,
    pady=(14, 8)
)


# ==========================================
# Player Buttons
# ==========================================

player_buttons = tk.Frame(
    player,
    bg="#111419"
)

player_buttons.pack(
    pady=(0, 10)
)


rewind_button = tk.Button(
    player_buttons,
    text="⏪ 10s",
    command=rewind_10,
    font=("Segoe UI", 9, "bold"),
    bg="#252932",
    fg="#d8dbe1",
    activebackground="#30343e",
    activeforeground="white",
    relief="flat",
    padx=14,
    pady=8,
    cursor="hand2"
)

rewind_button.pack(
    side="left",
    padx=5
)


play_pause_button = tk.Button(
    player_buttons,
    text="▶ Play",
    command=toggle_play_pause,
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#101216",
    activebackground="#dddddd",
    activeforeground="#101216",
    relief="flat",
    padx=20,
    pady=8,
    cursor="hand2"
)

play_pause_button.pack(
    side="left",
    padx=5
)


forward_button = tk.Button(
    player_buttons,
    text="10s ⏩",
    command=forward_10,
    font=("Segoe UI", 9, "bold"),
    bg="#252932",
    fg="#d8dbe1",
    activebackground="#30343e",
    activeforeground="white",
    relief="flat",
    padx=14,
    pady=8,
    cursor="hand2"
)

forward_button.pack(
    side="left",
    padx=5
)


# ==========================================
# Seek Bar
# ==========================================

progress_var = tk.DoubleVar(
    value=0
)

progress_scale = tk.Scale(
    player,
    variable=progress_var,
    from_=0,
    to=0.1,
    orient="horizontal",
    showvalue=False,
    resolution=0.1,
    command=seek_audio,
    bg="#111419",
    fg="#ffffff",
    troughcolor="#292d35",
    highlightthickness=0,
    activebackground="#ffffff",
    sliderrelief="flat",
    bd=0
)

progress_scale.pack(
    fill="x",
    padx=18
)


# ==========================================
# Time Labels
# ==========================================

time_frame = tk.Frame(
    player,
    bg="#111419"
)

time_frame.pack(
    fill="x",
    padx=18,
    pady=(0, 14)
)


position_label = tk.Label(
    time_frame,
    text="00:00",
    font=("Segoe UI", 8),
    fg="#858c98",
    bg="#111419"
)

position_label.pack(
    side="left"
)


duration_label = tk.Label(
    time_frame,
    text="00:00",
    font=("Segoe UI", 8),
    fg="#858c98",
    bg="#111419"
)

duration_label.pack(
    side="right"
)


# ==========================================
# Main Buttons
# ==========================================

buttons = tk.Frame(
    card,
    bg="#181b21"
)

buttons.pack(
    fill="x",
    padx=25,
    pady=(0, 20)
)


clear_button = tk.Button(
    buttons,
    text="Clear",
    command=clear_text,
    font=("Segoe UI", 10, "bold"),
    bg="#252932",
    fg="#d8dbe1",
    activebackground="#30343e",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

clear_button.pack(
    side="right"
)


generate_button = tk.Button(
    buttons,
    text="Generate Speech",
    command=generate_speech,
    font=("Segoe UI", 10, "bold"),
    bg="#ffffff",
    fg="#101216",
    activebackground="#dddddd",
    activeforeground="#101216",
    relief="flat",
    padx=22,
    pady=10,
    cursor="hand2"
)

generate_button.pack(
    side="right",
    padx=(0, 10)
)


stop_button = tk.Button(
    buttons,
    text="Stop Generation",
    command=stop_speech,
    font=("Segoe UI", 10, "bold"),
    bg="#252932",
    fg="#ff6b6b",
    activebackground="#30343e",
    activeforeground="#ff8080",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    state="disabled"
)

stop_button.pack(
    side="right",
    padx=(0, 10)
)


# ==========================================
# Status
# ==========================================

status_var = tk.StringVar(
    value="● Ready"
)

status_label = tk.Label(
    root,
    textvariable=status_var,
    font=("Segoe UI", 9),
    fg="#888f9b",
    bg="#0e1014"
)

status_label.pack(
    pady=(0, 18)
)


# ==========================================
# UI Update Loop
# ==========================================

root.after(
    100,
    update_player_ui
)


# ==========================================
# Start
# ==========================================

root.mainloop()