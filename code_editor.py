# code_editor.py
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont
from syntax_highlighter import PythonHighlighter  # Import the highlighter class
import json


class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.theme_data = self.load_theme_data()
        self.highlighter = None
        self.setFont(QFont('Consolas', 10))  # Ensure the font is set
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
    
    def setPlainText(self, text):
        super().setPlainText(text)
        # After setting the text, apply the theme
        self.apply_theme('default')  # Apply the default theme after text is set
    
    def load_theme_data(self):
        try:
            with open("themes.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading theme data: {e}")
            return {}

    def apply_theme(self, theme_name):
        if self.highlighter:
            self.highlighter.load_theme(theme_name)
        else:
            self.highlighter = PythonHighlighter(self.document(), self.theme_data)
            self.highlighter.load_theme(theme_name)
