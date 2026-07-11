import sys

from PySide6.QtWidgets import QApplication

from ui import AssistantWindow

app = QApplication(sys.argv)

window = AssistantWindow()
window.show()

app.exec()