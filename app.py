import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QThread

from ui.assistant_window import AssistantWindow

from ai.worker import AIWorker


class WorkerSignals(QObject):
    ask = Signal(str)


app = QApplication(sys.argv)

window = AssistantWindow()
window.show()


# -----------------------
# Create background thread
# -----------------------

thread = QThread()

worker = AIWorker()
worker.moveToThread(thread)

signals = WorkerSignals()

signals.ask.connect(worker.run)

thread.start()


# -----------------------
# Send Button
# -----------------------

def send_message():

    prompt = window.input_box.toPlainText().strip()

    if not prompt:
        return

    window.chat.append(f"<b>You:</b> {prompt}")

    window.input_box.clear()


    signals.ask.emit(prompt)


window.send.clicked.connect(send_message)


# -----------------------
# AI Finished
# -----------------------

def ai_finished(response):
    window.chat.append(f"<b>Desktop AI:</b> {response}")
    window.chat.append("")


worker.finished.connect(ai_finished)


# -----------------------
# Error
# -----------------------

def ai_error(error):

    window.chat.append(f"<font color='red'>{error}</font>")


worker.error.connect(ai_error)


sys.exit(app.exec())