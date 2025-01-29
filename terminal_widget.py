from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess, Qt

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.process = QProcess(self)  # Create a QProcess for terminal commands
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyRead.connect(self.read_output)

    def init_ui(self):
        """Initialize the terminal UI"""
        layout = QVBoxLayout(self)

        self.output = QTextEdit(self)  # QTextEdit for terminal output
        self.output.setReadOnly(True)  # Set it to read-only
        self.output.setStyleSheet("background-color: black; color: white; font-family: Consolas, monospace; font-size: 12px;")
        
        self.command_input = QLineEdit(self)  # QLineEdit for entering commands
        self.command_input.setStyleSheet("background-color: black; color: white; font-family: Consolas, monospace; font-size: 12px;")
        self.command_input.returnPressed.connect(self.run_command)

        layout.addWidget(self.output)
        layout.addWidget(self.command_input)

        self.setLayout(layout)

    def run_command(self):
        """Run the command entered in the terminal input"""
        command = self.command_input.text()
        if command.strip() != "":
            self.output.append(f"$ {command}")  # Display the command in the terminal
            self.process.start(command)  # Start the process for the command
            self.command_input.clear()

    def read_output(self):
        """Read the output from the terminal process and append it to the terminal output"""
        data = self.process.readAllStandardOutput().data().decode("utf-8")
        self.output.append(data)

    def set_terminal_size(self, width, height):
        """Optional: Adjust terminal size"""
        self.output.setFixedHeight(height)
        self.output.setFixedWidth(width)

    def clear_terminal(self):
        """Clear the terminal output."""
        self.output.clear()  # Corrected to use self.output instead of self.output_area

    def write_output(self, text):
        """Write text to the terminal."""
        self.output.append(text)  # Corrected to use self.output instead of self.output_area
