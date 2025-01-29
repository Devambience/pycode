from PyQt6.QtCore import Qt, QDir
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QSplitter, QWidget, QMenuBar, QTabWidget
# from terminal_widget import TerminalWidget
from PyQt6.QtGui import QAction
from file_manager import FileManager
from code_editor import CodeEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Open Source Code")
        self.setGeometry(100, 100, 1200, 800)

        # Central layout with splitter
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create a tab widget to handle multiple code editors
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)  # Allow closing tabs
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Create the file manager
        self.file_manager = FileManager(self)
        self.file_manager.setMinimumWidth(250)
        self.file_manager.set_root_path(QDir.rootPath())  # Root directory
        self.file_manager.clicked.connect(self.open_selected_file)

        # Create a splitter for horizontal split between file manager and code editor
        self.splitter = QSplitter(Qt.Orientation.Horizontal, self.central_widget)
        self.splitter.addWidget(self.file_manager)
        self.splitter.addWidget(self.tab_widget)

        # Create terminal widget at the bottom
        # self.terminal_widget = TerminalWidget(self)

        # Create a splitter for the bottom (code editor and terminal)
        self.bottom_splitter = QSplitter(Qt.Orientation.Vertical, self.central_widget)
        self.bottom_splitter.addWidget(self.splitter)
        # self.bottom_splitter.addWidget(self.terminal_widget)

        layout.addWidget(self.bottom_splitter)

        # Add Menu Bar
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setEnabled(False)  # Initially disable undo
        undo_action.triggered.connect(self.undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setEnabled(False)  # Initially disable redo
        redo_action.triggered.connect(self.redo_action)
        edit_menu.addAction(redo_action)

        # Terminal menu (placeholder for now)
        # terminal_menu = menu_bar.addMenu("Terminal")
        # run_action = QAction("Run Command", self)
        # run_action.triggered.connect(self.run_command_placeholder)
        # terminal_menu.addAction(run_action)

    def open_selected_file(self, index):
        """Open a new tab when a file is clicked in the file manager."""
        file_path = self.file_manager.file_model.filePath(index)
        if not file_path.endswith("/"):  # Ensure it's not a directory
            # Create a new CodeEditor and add it to the tab widget
            file_name = file_path.split("/")[-1]
            editor = CodeEditor()
            with open(file_path, "r") as file:
                content = file.read()
                editor.setPlainText(content)
            self.add_tab(file_name, editor)


    # def run_command_placeholder(self):
    #     """Placeholder for terminal command."""
    #     print("Terminal -> Run Command selected!")

    def add_tab(self, file_name, editor):
        """Add a new tab with the file name and code editor."""
        index = self.tab_widget.addTab(editor, file_name)
        self.tab_widget.setCurrentIndex(index)

    def close_tab(self, index):
        """Close the tab when the close button is clicked."""
        self.tab_widget.removeTab(index)

    def save_file(self):
        """Save the currently open file in the active tab."""
        current_widget = self.tab_widget.currentWidget()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
        if file_name:
            with open(file_name, "w") as file:
                file.write(current_widget.toPlainText())

    def undo_action(self):
        """Undo action for the currently selected editor."""
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            current_editor.undo()

    def redo_action(self):
        """Redo action for the currently selected editor."""
        current_editor = self.tab_widget.currentWidget()
        if current_editor:
            current_editor.redo()

    def open_file(self):
        """Open a file dialog to select and open a file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            file_name = file_name.split("/")[-1]
            editor = CodeEditor()
            with open(file_name, "r") as file:
                content = file.read()
                editor.setPlainText(content)
            self.add_tab(file_name, editor)