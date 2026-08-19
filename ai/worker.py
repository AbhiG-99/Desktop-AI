from screen.capture import capture_as_base64
from PySide6.QtCore import QObject, Signal, Slot
from ai.llm import ask_ai
from ai.memory import add_user_message, add_ai_message, get_messages
from screen.capture import capture_as_base64

class AIWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    @Slot(str)
    def run(self, user_message):
        try:
            add_user_message(user_message)
            response = ask_ai(get_messages(), image_b64=capture_as_base64())
            add_ai_message(response)
            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e))