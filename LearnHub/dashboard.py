import sys

from PyQt5.QtWidgets import(QApplication , QMainWindow , QWidget , QLabel , QPushButton , QVBoxLayout , QHBoxLayout , QFrame , QStackedWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from pages.home import HomePage
from pages.courses import CoursesPage
from pages.notes import NotesPage
from pages.quiz import QuizPage
from pages.profile import ProfilePage
from pages.settings import SettingsPage


class Dashboard(QMainWindow):

    def __init__(self , username):
        super().__init__()

        self.username = username

        self.setWindowTitle("LearnHub")
        self.resize(1200 , 700)

        self.initUI()

    def initUI(self):

        central = QWidget()
        self.setCentralWidget(central)


        #Main Layout
        main_layout = QHBoxLayout()


        central.setLayout(main_layout)


        #SideBar

        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()

        sidebar.setLayout(sidebar_layout)


        #Add LOGO

        logo = QLabel("📚LearnHub")

        logo.setAlignment(Qt.AlignCenter)

        logo.setFont(QFont("Segoe UI" , 18 , QFont.Bold))

        sidebar_layout.addWidget(logo)


        #SideBar Buttons

        menu = ["🏡 DashBoard" , "📚 Courses" , "📋 Notes" , "🧠 Quiz" , "👤 Profile" , "⚙️ Settings" , "🚪 LogOut"]

        self.buttons = []
        
        for item in menu:
            button = QPushButton(item)

            button.setMinimumHeight(45)            

            sidebar_layout.addWidget(button)

            self.buttons.append(button)

            button.setFont(QFont("Segoe UI" , 13))

        self.buttons[0].clicked.connect(lambda: content.setCurrentIndex(0))
        self.buttons[1].clicked.connect(lambda: content.setCurrentIndex(1))
        self.buttons[2].clicked.connect(lambda: content.setCurrentIndex(2))
        self.buttons[3].clicked.connect(lambda: content.setCurrentIndex(3))
        self.buttons[4].clicked.connect(lambda: content.setCurrentIndex(4))
        self.buttons[5].clicked.connect(lambda: content.setCurrentIndex(5))
        


        #Content

        content = QStackedWidget()


        #Style Sheet
        self.setStyleSheet("""

            QMainWindow{

                background:#111827;

            }

            QFrame{

                background:#1F2937;

                border-radius:10px;

            }

            QLabel{

                color:white;

            }

            QPushButton{

                background:#374151;

                color:white;

                border:none;

                border-radius:8px;

                padding:12px;

                text-align:left;

            }

            QPushButton:hover{

                background:#3B82F6;

            }

            """)


        home = HomePage(self.username)
        courses = CoursesPage(self.username)
        notes = NotesPage(self.username)
        quiz = QuizPage(self.username)
        profile = ProfilePage(self.username)
        settings = SettingsPage(self.username)

        content.addWidget(home)
        content.addWidget(courses)
        content.addWidget(notes)
        content.addWidget(quiz)
        content.addWidget(profile)
        content.addWidget(settings)

        self.buttons[0].clicked.connect(lambda: content.setCurrentIndex(0))
        self.buttons[1].clicked.connect(lambda: content.setCurrentIndex(1))
        self.buttons[2].clicked.connect(lambda: content.setCurrentIndex(2))
        self.buttons[3].clicked.connect(lambda: content.setCurrentIndex(3))
        self.buttons[4].clicked.connect(lambda: content.setCurrentIndex(4))
        self.buttons[5].clicked.connect(lambda: content.setCurrentIndex(5))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Dashboard()
    window.show()

    sys.exit(app.exec_())