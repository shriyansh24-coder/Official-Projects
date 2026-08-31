import sqlite3

from PyQt5.QtWidgets import(QWidget , QLabel , QLineEdit , QPushButton , QMessageBox , QVBoxLayout)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from database import add_user

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Account")
        self.setFixedSize(500 , 650)

        self.initUI()

    def initUI(self):
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI" , 22 , QFont.Bold))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)

        layout = QVBoxLayout()

        layout.addStretch()

        layout.addWidget(title)

        layout.addSpacing(25)

        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)

        layout.addSpacing(20)

        layout.addWidget(register_button)

        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
                    QWidget{
                        background-color:#111827;
                        color:white;
                        font-family:Segoe UI;
                    }
        
                    QLabel{
                        color:white;
                    }
        
                    QLineEdit{
                        background:#1F2937;
                        border:2px solid #3B82F6;
                        border-radius:12px;
                        padding:10px;
                        color:white;
                        font-size:15px;
                    }
        
                    QLineEdit:focus{
                        border:2px solid #10B981;
                    }
        
                    QPushButton{
                        background:#2563EB;
                        color:white;
                        border:none;
                        border-radius:12px;
                        padding:12px;
                        font-size:16px;
                        font-weight:bold;
                    }
        
                    QPushButton:hover{
                        background:#3B82F6;
                    }
        
                    QPushButton:pressed{
                        background:#1D4ED8;
                    }
                """)

    def register(self):
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text()
        confirm = self.confirm_password.text()

        # Check empty fields
        if not username or not email or not password or not confirm:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        # Check password match
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        conn = sqlite3.connect("learnhub.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Success",
            "Account Created Successfully!"
        )

        self.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = RegisterWindow()
    window.show()

    sys.exit(app.exec_())