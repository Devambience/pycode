# terminal_thread.py

import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

class TerminalThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.Popen(
            self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        output = stdout.decode() + stderr.decode()
        self.output_signal.emit(output)