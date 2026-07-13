import sys
import keyboard

from PySide6.QtWidgets import QApplication

from ui.assistant_window import AssistantWindow
from ai.llm import ask_ai
# print("Creating app")

app = QApplication(sys.argv)
# print("Creating window")
window = AssistantWindow()
# print("Showing window")
window.show()

# print("Starting event loop")
def toggle_window():
    if window.isVisible():
        window.hide()
    else:
        window.show()
        window.activateWindow()


def send_message():
    # Get user's message
    user_message = window.input_box.toPlainText().strip()

    if not user_message:
        return

    # Show user message
    window.chat.append(f"<b>You:</b> {user_message}")

    # Clear input box
    window.input_box.clear()

    # Ask AI
    ai_response = ask_ai(user_message)

    # Show AI response
    window.chat.append(f"<b>AI:</b> {ai_response}")
    window.chat.append("")  # Empty line for spacing


# Connect Send button
window.send.clicked.connect(send_message)

# Hotkeys
# keyboard.add_hotkey("ctrl+alt", toggle_window)
# keyboard.add_hotkey("esc", lambda: window.hide())

sys.exit(app.exec())