from PySide6.QtCore import QObject, Signal, Slot

from ai.llm import ask_ai
from ai.memory import (
    add_user_message,
    add_ai_message,
    get_messages,
)


class AIWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    @Slot(str)
    def run(self, user_message):
        try:
            # Save user message
            add_user_message(user_message)

            # Ask the AI using full conversation history
            response = ask_ai(get_messages())

            # Save assistant response
            add_ai_message(response)

            # Send response back to UI
            self.finished.emit(response)

        except Exception as e:
            self.error.emit(str(e))