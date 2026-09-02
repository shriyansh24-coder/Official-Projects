APP_STYLE = """

/* ==================================================
   MAIN WINDOW
   ================================================== */

QMainWindow {
    background-color: #09000F;
}

QWidget {
    color: #FFFFFF;
    font-family: "Segoe UI";
}


/* ==================================================
   SIDEBAR
   ================================================== */

QFrame {
    background-color: #100018;
}

QPushButton {
    background-color: transparent;
    color: #D8C7FF;

    border: none;
    border-radius: 10px;

    text-align: left;

    padding: 12px 15px;

    font-size: 14px;
}

QPushButton:hover {
    background-color: #28113D;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #7B2CFF;
    color: #FFFFFF;
}


/* ==================================================
   LOGO
   ================================================== */

QLabel#logo {
    color: #B66DFF;

    font-size: 24px;
    font-weight: bold;
}


/* ==================================================
   PAGE TITLE
   ================================================== */

QLabel#page_title {
    color: #FFFFFF;

    font-size: 30px;
    font-weight: bold;
}


/* ==================================================
   SUBTITLE
   ================================================== */

QLabel#subtitle {
    color: #9D8AAA;

    font-size: 14px;
}


/* ==================================================
   CURRENT SONG
   ================================================== */

QLabel#current_song {
    color: #B66DFF;

    font-size: 15px;
    font-weight: bold;

    padding: 5px;
}


/* ==================================================
   SEARCH BOX
   ================================================== */

QLineEdit {
    background-color: #12001C;

    border: 1px solid #35204A;
    border-radius: 10px;

    padding: 12px;

    color: #FFFFFF;

    font-size: 14px;
}

QLineEdit:hover {
    border: 1px solid #5F3690;
}

QLineEdit:focus {
    border: 1px solid #9B5CFF;
}


/* ==================================================
   PLAYLIST
   ================================================== */

QListWidget {
    background-color: #100018;

    border: 1px solid #28113D;
    border-radius: 14px;

    padding: 10px;

    font-size: 16px;

    outline: none;
}

QListWidget::item {
    padding: 14px;

    border-radius: 9px;

    margin: 3px;
}

QListWidget::item:hover {
    background-color: #28113D;
}

QListWidget::item:selected {
    background-color: #7B2CFF;

    color: #FFFFFF;
}


/* ==================================================
   PLAYER CONTROL BUTTONS
   ================================================== */

QPushButton#control_button {
    background-color: #21102F;

    border: 1px solid #42205E;
    border-radius: 25px;

    min-width: 45px;
    min-height: 45px;

    padding: 8px;

    text-align: center;

    font-size: 17px;
}

QPushButton#control_button:hover {
    background-color: #351550;

    border: 1px solid #7B2CFF;
}

QPushButton#control_button:pressed {
    background-color: #5A16CC;
}


/* ==================================================
   PLAY BUTTON
   ================================================== */

QPushButton#play_button {
    background-color: #7B2CFF;

    border: none;
    border-radius: 30px;

    min-width: 58px;
    min-height: 58px;

    padding: 8px;

    text-align: center;

    font-size: 20px;
    font-weight: bold;
}

QPushButton#play_button:hover {
    background-color: #9B5CFF;
}

QPushButton#play_button:pressed {
    background-color: #5A16CC;
}


/* ==================================================
   SLIDER
   ================================================== */

QSlider::groove:horizontal {
    height: 6px;

    background-color: #28113D;

    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 14px;
    height: 14px;

    margin: -4px 0;

    background-color: #9B5CFF;

    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background-color: #B66DFF;
}


/* ==================================================
   CHECKBOX
   ================================================== */

QCheckBox {
    color: #CDB9E8;

    font-size: 14px;

    spacing: 8px;
}

QCheckBox:hover {
    color: #FFFFFF;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;

    border: 1px solid #5F3690;
    border-radius: 4px;

    background-color: #12001C;
}

QCheckBox::indicator:checked {
    background-color: #7B2CFF;

    border: 1px solid #9B5CFF;
}


/* ==================================================
   MESSAGE BOX
   ================================================== */

QMessageBox {
    background-color: #100018;
}

QMessageBox QLabel {
    color: #FFFFFF;
}

QMessageBox QPushButton {
    background-color: #7B2CFF;

    color: #FFFFFF;

    border-radius: 8px;

    padding: 8px 18px;

    min-width: 70px;

    text-align: center;
}

QMessageBox QPushButton:hover {
    background-color: #9B5CFF;
}

"""