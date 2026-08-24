import json

from PySide6.QtCore import QObject, Signal, Slot

from ai.llm import ask_ai
from ai.memory import (
    add_user_message,
    add_ai_message,
    add_system_note,
    get_messages,
)
from services.automation import execute_action, parse_ai_action
from screen.capture import capture_as_base64


class AIWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    @Slot(str)
    def run(self, user_message):
        try:
            # Save user message
            add_user_message(user_message)

            # Ask the AI using full conversation history + current screen
            response = ask_ai(get_messages(), image_b64=capture_as_base64())

            # Check if the AI requested a desktop action
            request = parse_ai_action(response)

            if request is None:
                # Save assistant response
                add_ai_message(response)

                # Send response back to UI
                self.finished.emit(response)
                return

            action = request["action"]
            params = request.get("params") or {}
            say = request.get("say") or ""

            result = execute_action(action, params)

            # Keep the outcome in context for follow-up turns
            add_ai_message(say or f"Performed {action}.")
            add_system_note(f"Action {action} result: {json.dumps(result)}")

            if result["success"]:
                line = f"[{action}] done"
                data = result.get("data")
                if data:
                    line += f" — {json.dumps(data)}"
            else:
                line = f"[{action}] failed — {result.get('error')}"

            text = f"{say}\n{line}" if say else line
            self.finished.emit(text)

        except Exception as e:
            self.error.emit(str(e))
