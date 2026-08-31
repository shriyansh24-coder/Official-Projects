from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel , QFrame , QProgressBar , QLineEdit , QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomePage(QWidget):

    def __init__(self , username):
        super().__init__()

        self.username = username

        self.initUI()

    def create_card(self, icon, title, description, progress):

        card = QFrame()
        card.setMinimumSize(260, 180)

        layout = QVBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 28))

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))

        description_label = QLabel(description)
        description_label.setFont(QFont("Segoe UI", 15))

        progress_label = QLabel(f"{progress}% Completed")
        progress_label.setFont(QFont("Segoe UI", 15))

        bar = QProgressBar()
        bar.setValue(progress)

        continue_button = QPushButton("Continue Learning")
        continue_button.setFont(QFont("Segoe UI", 12))

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addSpacing(10)
        layout.addWidget(progress_label)
        layout.addWidget(bar)
        layout.addStretch()
        layout.addWidget(continue_button)

        card.setLayout(layout)

        return card

    def initUI(self):

        main_layout = QVBoxLayout()

        #Top Bar

        top_bar = QHBoxLayout()

        logo = QLabel("📚LearnHub")
        logo.setFont(QFont("Segoe UI" , 25 , QFont.Bold))

        search = QLineEdit()
        search.setPlaceholderText("Search courses...")
        search.setFont(QFont("Segoe UI" , 13))

        profile = QLabel(f"👤 {self.username}")
        profile.setFont(QFont("Segoe UI" , 15))

        top_bar.addWidget(logo)
        top_bar.addStretch()
        top_bar.addWidget(search)
        top_bar.addSpacing(15)
        top_bar.addWidget(profile)

        main_layout.addLayout(top_bar)
        main_layout.addSpacing(25)

        #Title and Subtitle

        title = QLabel("Welcome Back !")
        title.setFont(QFont("Segoe UI" , 26 , QFont.Bold))

        subtitle = QLabel("Continue your learning Journey.")
        subtitle.setFont(QFont("Segoe UI" , 20))

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(30)

        cards = QHBoxLayout()

        cards.addWidget(self.create_card("🐍","Python","Beginner to Advanced",80))

        cards.addWidget(self.create_card("☕","Java","Object Oriented Programming",45))

        cards.addWidget(self.create_card("💻","C++","DSA & Competitive Coding",20))

        main_layout.addLayout(cards)

        main_layout.addSpacing(30)

        overall = QLabel("📈 Overall Progress")
        overall.setFont(QFont("Segoe UI" , 18 , QFont.Bold))

        progress = QProgressBar()
        progress.setValue(75)
        progress.setFont(QFont("Segoe UI" , 15))

        main_layout.addWidget(overall)
        main_layout.addWidget(progress)

        main_layout.addStretch()

        self.setLayout(main_layout)

        self.setStyleSheet("""

            QWidget{

                background:#111827;
                color:white;

            }

            QFrame{

                background:#1F2937;
                border-radius:12px;
                padding:10px;

            }

            QLabel{

                color:white;

            }

            QProgressBar{

                height:25px;
                font-size:16px;
                font-weight:bold;
                border-radius:8px;
                text-align:center;

            }

            QProgressBar::chunk{

                background:#3B82F6;
                border-radius:8px;

            }

            QLineEdit{

            background:#1F2937;
            border:2px solid #3B82F6;
            border-radius:10px;
            padding:8px;
            color:white;
            min-width:250px;

            }
            QPushButton{

            background:#2563EB;
            color:white;
            border:none;
            border-radius:10px;
            padding:8px;
            font-weight:bold;

            }

        QPushButton:hover{

            background:#3B82F6;

        }

        """)