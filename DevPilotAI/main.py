import sys

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from pages.dashboard import Dashboard
from pages.project_explorer import ProjectExplorer
from pages.code_review import CodeReviewPage
from pages.debugger import DebuggerPage


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()