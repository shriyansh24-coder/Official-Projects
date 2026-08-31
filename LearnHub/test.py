import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel("Welcome to LearnHub!")
label.resize(400, 200)
label.show()

sys.exit(app.exec_())