"""Automation module — mouse, keyboard, and browser control."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal

from automation.browser import BrowserAutomation
from automation.keyboard import KeyboardController
from automation.mouse import MouseController


class AutomationManager(QObject):
    """Facade that coordinates mouse and keyboard automation."""

    action_performed = Signal(str, dict)
    error_occurred = Signal(str)

    def __init__(self, dry_run: bool = False, parent: QObject | None = None):
        super().__init__(parent)
        self.dry_run = dry_run
        self.mouse = MouseController(dry_run=dry_run, parent=self)
        self.keyboard = KeyboardController(dry_run=dry_run, parent=self)
        self.browser = BrowserAutomation(dry_run=dry_run, parent=self)

        self.mouse.action_performed.connect(self._on_action)
        self.mouse.error_occurred.connect(self._on_error)
        self.keyboard.action_performed.connect(self._on_action)
        self.keyboard.error_occurred.connect(self._on_error)
        self.browser.action_performed.connect(self._on_action)
        self.browser.error_occurred.connect(self._on_error)

        self._actions: dict[str, Any] = {
            "mouse.click": self.mouse.click,
            "mouse.right_click": self.mouse.right_click,
            "mouse.double_click": self.mouse.double_click,
            "mouse.move": self.mouse.move,
            "mouse.drag": self.mouse.drag,
            "mouse.scroll": self.mouse.scroll,
            "mouse.get_position": self.mouse.get_position,
            "mouse.get_screen_size": self.mouse.get_screen_size,
            "keyboard.type_text": self.keyboard.type_text,
            "keyboard.press_key": self.keyboard.press_key,
            "keyboard.hotkey": self.keyboard.hotkey,
            "keyboard.key_down": self.keyboard.key_down,
            "keyboard.key_up": self.keyboard.key_up,
            "browser.open": self.browser.open,
            "browser.find_element": self.browser.find_element,
            "browser.click_element": self.browser.click_element,
            "browser.fill_input": self.browser.fill_input,
            "browser.get_text": self.browser.get_text,
            "browser.screenshot": self.browser.screenshot,
            "browser.close": self.browser.close,
        }

    def execute(self, action: str, params: dict[str, Any] | None = None) -> Any:
        if action not in self._actions:
            self.error_occurred.emit(f"Unknown action: {action}")
            return None
        return self._actions[action](**(params or {}))

    def get_capabilities(self) -> list[str]:
        return list(self._actions.keys())

    def cleanup(self) -> None:
        self.keyboard.stop_listening()
        self.browser.close()

    def _on_action(self, action: str, data: dict) -> None:
        self.action_performed.emit(action, data)

    def _on_error(self, message: str) -> None:
        self.error_occurred.emit(message)
