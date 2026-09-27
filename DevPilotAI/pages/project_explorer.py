import os

from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTreeWidget,
    QTreeWidgetItem,
    QPlainTextEdit
)

from PyQt5.QtCore import Qt

from services.file_service import (
    scan_project,
    read_file
)


class ProjectExplorer(QWidget):

    def __init__(self):
        super().__init__()

        self.project_path = None

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30, 25, 30, 25
        )

        # Header
        header = QHBoxLayout()

        title = QLabel("Project Explorer")
        title.setObjectName("page_title")

        self.project_label = QLabel(
            "No project selected"
        )

        self.project_label.setObjectName(
            "subtitle"
        )

        open_button = QPushButton(
            "▣  Open Project"
        )

        open_button.setObjectName(
            "primary_button"
        )

        open_button.clicked.connect(
            self.open_project
        )

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.project_label)
        header.addWidget(open_button)

        main_layout.addLayout(header)

        # Explorer + Editor
        content = QHBoxLayout()
        content.setSpacing(15)

        # File tree
        self.file_tree = QTreeWidget()

        self.file_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #0D141B;
                color: #AAB8C5;
                border: 1px solid #1C2935;
                border-radius: 6px;
                font-family: "Segoe UI";
                font-size: 13px;
                outline: none;
            }

            QTreeWidget::item {
                padding: 6px 4px;
            }

            QTreeWidget::item:hover {
                background-color: #14212A;
                color: #DCE6ED;
            }

            QTreeWidget::item:selected {
                background-color: #102F38;
                color: #00E5FF;
            }

            QHeaderView::section {
                background-color: #111821;
                color: #718096;
                border: none;
                border-bottom: 1px solid #1C2935;
                padding: 8px;
                font-size: 10px;
                font-weight: bold;
            }
        """)

        self.file_tree.setHeaderLabel(
            "PROJECT FILES"
        )

        self.file_tree.setMinimumWidth(280)

        self.file_tree.itemClicked.connect(
            self.file_selected
        )

        content.addWidget(
            self.file_tree
        )

        # Code viewer
        code_layout = QVBoxLayout()

        code_title = QLabel(
            "SOURCE CODE"
        )

        code_title.setObjectName(
            "section_title"
        )

        self.code_editor = QPlainTextEdit()

        self.code_editor.setReadOnly(True)

        self.code_editor.setPlaceholderText(
            "Select a source file to inspect..."
        )

        self.code_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0B1016;
                border: 1px solid #243440;
                border-radius: 6px;
                padding: 12px;
                color: #B8C7D3;
                font-family: Consolas;
                font-size: 13px;
                selection-background-color: #16404A;
                selection-color: #E6EDF3;
            }
        """)

        code_layout.addWidget(code_title)
        code_layout.addWidget(
            self.code_editor
        )

        content.addLayout(
            code_layout
        )

        main_layout.addLayout(content)

        self.setLayout(main_layout)

    # --------------------------------------------------

    def open_project(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder"
        )

        if not folder:
            return

        self.project_path = folder

        self.project_label.setText(
            os.path.basename(folder)
        )

        self.load_project()

    # --------------------------------------------------

    def load_project(self):

        self.file_tree.clear()

        files = scan_project(
            self.project_path
        )

        root_item = QTreeWidgetItem([
            os.path.basename(
                self.project_path
            )
        ])

        self.file_tree.addTopLevelItem(
            root_item
        )

        folders = {}

        for file_path in files:

            parts = file_path.split(
                os.sep
            )

            parent = root_item
            current_path = ""

            for index, part in enumerate(parts):

                current_path = os.path.join(
                    current_path,
                    part
                )

                if index == len(parts) - 1:

                    item = QTreeWidgetItem([
                        f"📄 {part}"
                    ])

                    item.setData(
                        0,
                        Qt.UserRole,
                        os.path.join(
                            self.project_path,
                            file_path
                        )
                    )

                    parent.addChild(item)

                else:

                    if current_path not in folders:

                        folder_item = QTreeWidgetItem([
                            f"📁 {part}"
                        ])

                        parent.addChild(
                            folder_item
                        )

                        folders[current_path] = (
                            folder_item
                        )

                    parent = folders[
                        current_path
                    ]

        root_item.setExpanded(True)

    # --------------------------------------------------

    def file_selected(self, item, column):

        file_path = item.data(
            0,
            Qt.UserRole
        )

        if not file_path:
            return

        content = read_file(
            file_path
        )

        self.code_editor.setPlainText(
            content
        )