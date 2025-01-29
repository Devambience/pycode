# file_manager.py

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QTreeView


class FileManager(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize QFileSystemModel
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())  # Set the root directory

        # Set the model for the QTreeView (file manager)
        self.setModel(self.file_model)

        # Set the initial root directory for the file manager
        self.setRootIndex(self.file_model.index(QDir.rootPath()))

        # Set column width and other options
        self.setColumnWidth(0, 250)

        # Enable drag-and-drop
        self.setAcceptDrops(True)

    def set_root_path(self, path):
        """Set the root path for the file manager."""
        self.file_model.setRootPath(path)
        self.setRootIndex(self.file_model.index(path))