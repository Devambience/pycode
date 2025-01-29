from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme_data):
        super().__init__(document)  # Correct initialization with the document
        self.theme_data = theme_data
        self.highlightingRules = []
        self.load_theme('default')

    def load_theme(self, theme_name):
        if theme_name not in self.theme_data:
            raise ValueError(f"Theme '{theme_name}' not found in theme data.")
        
        theme = self.theme_data[theme_name]
        self.highlightingRules.clear()

        # Example rule for 'def' keyword
        self._add_highlight_rule(r"\bdef\b", {"color": "#faa789", "font": "normal"})
        self._add_highlight_rule(r"\b(class|import|from|return|if|else)\b", theme["keywords"])
        self._add_highlight_rule(r"#.*", theme["comments"])
        self._add_highlight_rule(r'"[^"]*"', theme["strings"])
        self._add_highlight_rule(r"'[^']*'", theme["strings"])

    def _add_highlight_rule(self, pattern, style):
        regex = QRegularExpression(pattern)
        format = QTextCharFormat()
        format.setForeground(QColor(style["color"]))
        if style["font"] == "italic":
            format.setFontItalic(True)
        elif style["font"] == "bold":
            format.setFontWeight(QFont.Weight.Bold)
        self.highlightingRules.append((regex, format))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                # Use capturedStart and capturedLength to get the match position and length
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)
        self.setCurrentBlockState(0)

