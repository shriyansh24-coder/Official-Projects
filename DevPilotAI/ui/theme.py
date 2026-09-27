APP_STYLE = """
QMainWindow {
    background-color: #080B10;
}

QWidget {
    color: #E6EDF3;
    font-family: "Segoe UI";
}

QLabel#project_label {
    color: #718096;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
}

/* ================= CODE REVIEW ================= */

QTextEdit {
    background-color: #0D141B;
    color: #E6EDF3;
    border: 1px solid #1C2935;
    border-radius: 6px;
    padding: 10px;
    font-family: "Consolas";
    font-size: 13px;
    selection-background-color: #123D47;
    selection-color: #FFFFFF;
}

QTextEdit:focus {
    border: 1px solid #00E5FF;
}


/* ================= FILE SELECTOR ================= */

QComboBox {
    background-color: #0D141B;
    color: #E6EDF3;
    border: 1px solid #1C2935;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #00E5FF;
}

QComboBox:focus {
    border: 1px solid #00E5FF;
}

QComboBox QAbstractItemView {
    background-color: #0D141B;
    color: #E6EDF3;
    border: 1px solid #1C2935;
    selection-background-color: #123D47;
    selection-color: #00E5FF;
}

/* ================= SIDEBAR ================= */

#sidebar {
    background-color: #0D1117;
    border-right: 1px solid #1C2935;
}

#logo {
    color: #E6EDF3;
    font-size: 21px;
    font-weight: bold;
    padding: 8px;
}

#logo_accent {
    color: #00E5FF;
}

#workspace_label {
    color: #526273;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 12px 8px 5px 8px;
}

#separator {
    color: #1C2935;
}

/* ================= NAVIGATION ================= */

QPushButton {
    background-color: transparent;
    color: #8795A5;
    border: none;
    border-radius: 6px;
    padding: 11px 12px;
    text-align: left;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #111B24;
    color: #D8E2EA;
}

QPushButton:pressed {
    background-color: #14242E;
}

#active_button {
    background-color: #10242C;
    color: #00E5FF;
    border-left: 2px solid #00E5FF;
}

/* ================= HEADER ================= */

#page_title {
    color: #E6EDF3;
    font-size: 25px;
    font-weight: 600;
}

#system_status {
    color: #52E88B;
    font-size: 12px;
}

#status_dot {
    color: #52E88B;
}

/* ================= WELCOME ================= */

#welcome {
    color: #F1F5F9;
    font-size: 29px;
    font-weight: 600;
}

#subtitle {
    color: #657486;
    font-size: 14px;
}

/* ================= STAT CARDS ================= */

#stat_card {
    background-color: #111821;
    border: 1px solid #1C2935;
    border-radius: 8px;
}

#stat_card:hover {
    border: 1px solid #294352;
}

#stat_title {
    color: #627284;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
}

#stat_value {
    color: #E6EDF3;
    font-size: 27px;
    font-weight: 600;
}

#stat_accent {
    color: #00E5FF;
}

/* ================= SECTION ================= */

#section_title {
    color: #667789;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
}

/* ================= AI CORE ================= */

#ai_frame {
    background-color: #0D151D;
    border: 1px solid #1D3541;
    border-radius: 8px;
}

#ai_header {
    color: #00E5FF;
    font-size: 13px;
    font-weight: bold;
}

#ai_description {
    color: #738396;
    font-size: 13px;
}

#ai_input {
    background-color: #080D12;
    color: #DCE6ED;
    border: 1px solid #20323D;
    border-radius: 5px;
    padding: 12px;
    font-size: 13px;
}

#ai_input:focus {
    border: 1px solid #00AFC4;
}

#ai_button {
    background-color: #00B8CC;
    color: #061015;
    border-radius: 5px;
    padding: 10px 18px;
    font-weight: bold;
}

#ai_button:hover {
    background-color: #00E5FF;
}

/* ================= ACTION BUTTONS ================= */

#primary_button {
    background-color: #00B8CC;
    color: #061015;
    border-radius: 5px;
    padding: 11px 18px;
    font-weight: bold;
}

#primary_button:hover {
    background-color: #00E5FF;
}

#secondary_button {
    background-color: #111821;
    color: #9AA9B8;
    border: 1px solid #263542;
    border-radius: 5px;
    padding: 10px 18px;
}

#secondary_button:hover {
    color: #00E5FF;
    border-color: #00AFC4;
}
"""