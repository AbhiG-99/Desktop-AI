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

        self.title = QLabel("Desktop AI")
        self.title.setAlignment(Qt.AlignCenter)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setPlaceholderText("Conversation will appear here...")

        self.input_box = QTextEdit()
        self.input_box.setFixedHeight(70)
        self.input_box.setPlaceholderText("Ask anything...")

        self.send = QPushButton("Send")

        layout.addWidget(self.title)
        layout.addWidget(self.chat)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)