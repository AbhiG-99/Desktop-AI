"""Keyboard automation controller."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pyautogui
from pynput import keyboard as pynput_keyboard
from PySide6.QtCore import QObject, Signal


@dataclass
class KeyboardResult:
    success: bool
    action: str
    data: dict[str, Any] | None = None
    error: str | None = None


class KeyboardController(QObject):
    """Controls keyboard input via pyautogui and listens via pynput."""

    action_performed = Signal(str, dict)
    hotkey_detected = Signal(list)
    error_occurred = Signal(str)

    def __init__(self, dry_run: bool = False, parent: QObject | None = None):
        super().__init__(parent)
        self.dry_run = dry_run
        self._listener: pynput_keyboard.Listener | None = None
        self._pressed_keys: set[str] = set()
        pyautogui.PAUSE = 0.01

    def type_text(self, text: str, interval: float = 0.0) -> KeyboardResult:
        if self.dry_run:
            return self._emit("type_text", {"text": text, "interval": interval})

        try:
            pyautogui.typewrite(text, interval=interval) if text.isascii() else pyautogui.write(text)
            return self._emit("type_text", {"text": text, "interval": interval})
        except Exception as e:
            return self._error("type_text", str(e))

    def press_key(self, keys: list[str]) -> KeyboardResult:
        if self.dry_run:
            return self._emit("press_key", {"keys": keys})

        try:
            for key in keys:
                pyautogui.press(key)
            return self._emit("press_key", {"keys": keys})
        except Exception as e:
            return self._error("press_key", str(e))

    def hotkey(self, keys: list[str]) -> KeyboardResult:
        if self.dry_run:
            return self._emit("hotkey", {"keys": keys})

        try:
            pyautogui.hotkey(*keys)
            return self._emit("hotkey", {"keys": keys})
        except Exception as e:
            return self._error("hotkey", str(e))

    def key_down(self, key: str) -> KeyboardResult:
        if self.dry_run:
            return self._emit("key_down", {"key": key})

        try:
            pyautogui.keyDown(key)
            return self._emit("key_down", {"key": key})
        except Exception as e:
            return self._error("key_down", str(e))

    def key_up(self, key: str) -> KeyboardResult:
        if self.dry_run:
            return self._emit("key_up", {"key": key})

        try:
            pyautogui.keyUp(key)
            return self._emit("key_up", {"key": key})
        except Exception as e:
            return self._error("key_up", str(e))

    def get_pressed_keys(self) -> list[str]:
        return list(self._pressed_keys)

    def start_listening(self) -> None:
        if self._listener and self._listener.is_alive():
            return

        def on_press(key):
            name = self._key_name(key)
            self._pressed_keys.add(name)

        def on_release(key):
            name = self._key_name(key)
            self._pressed_keys.discard(name)

        self._listener = pynput_keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
        )
        self._listener.start()

    def stop_listening(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._pressed_keys.clear()

    @staticmethod
    def _key_name(key) -> str:
        try:
            return key.char
        except AttributeError:
            return key.name

    def _emit(self, action: str, data: dict[str, Any]) -> KeyboardResult:
        result = KeyboardResult(success=True, action=action, data=data)
        self.action_performed.emit(action, data)
        return result

    def _error(self, action: str, message: str) -> KeyboardResult:
        result = KeyboardResult(success=False, action=action, error=message)
        self.error_occurred.emit(message)
        return result
