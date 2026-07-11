from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class AssistantWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Desktop AI")
        self.resize(420, 500)

        layout = QVBoxLayout()

        title = QLabel("Desktop AI")
        title.setAlignment(Qt.AlignCenter)

        chat = QTextEdit()
        chat.setReadOnly(True)
        chat.setPlaceholderText("Conversation will appear here...")

        input_box = QTextEdit()
        input_box.setFixedHeight(70)
        input_box.setPlaceholderText("Ask anything...")

        send = QPushButton("Send")

        layout.addWidget(title)
        layout.addWidget(chat)
        layout.addWidget(input_box)
        layout.addWidget(send)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)