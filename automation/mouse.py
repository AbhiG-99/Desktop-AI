"""Mouse automation controller."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import pyautogui
from PySide6.QtCore import QObject, Signal


@dataclass
class MouseResult:
    success: bool
    action: str
    data: dict[str, Any] | None = None
    error: str | None = None


class MouseController(QObject):
    """Controls mouse movements and clicks via pyautogui."""

    action_performed = Signal(str, dict)
    error_occurred = Signal(str)

    def __init__(self, dry_run: bool = False, parent: QObject | None = None):
        super().__init__(parent)
        self.dry_run = dry_run
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

    def click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: str = "left",
        clicks: int = 1,
    ) -> MouseResult:
        if self.dry_run:
            return self._emit("click", {"x": x, "y": y, "button": button, "clicks": clicks})

        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, clicks=clicks, button=button)
            else:
                pyautogui.click(clicks=clicks, button=button)
            return self._emit("click", {"x": x, "y": y, "button": button, "clicks": clicks})
        except Exception as e:
            return self._error("click", str(e))

    def right_click(self, x: int | None = None, y: int | None = None) -> MouseResult:
        return self.click(x, y, button="right", clicks=1)

    def double_click(self, x: int | None = None, y: int | None = None) -> MouseResult:
        return self.click(x, y, button="left", clicks=2)

    def move(self, x: int, y: int, duration: float = 0.0) -> MouseResult:
        if self.dry_run:
            return self._emit("move", {"x": x, "y": y, "duration": duration})

        try:
            pyautogui.moveTo(x, y, duration=duration)
            return self._emit("move", {"x": x, "y": y, "duration": duration})
        except Exception as e:
            return self._error("move", str(e))

    def drag(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: float = 0.5,
        button: str = "left",
    ) -> MouseResult:
        if self.dry_run:
            return self._emit("drag", {
                "start": {"x": start_x, "y": start_y},
                "end": {"x": end_x, "y": end_y},
                "duration": duration,
                "button": button,
            })

        try:
            pyautogui.moveTo(start_x, start_y)
            pyautogui.drag(
                end_x - start_x,
                end_y - start_y,
                duration=duration,
                button=button,
            )
            return self._emit("drag", {
                "start": {"x": start_x, "y": start_y},
                "end": {"x": end_x, "y": end_y},
                "duration": duration,
                "button": button,
            })
        except Exception as e:
            return self._error("drag", str(e))

    def scroll(self, clicks: int, x: int | None = None, y: int | None = None) -> MouseResult:
        if self.dry_run:
            return self._emit("scroll", {"clicks": clicks, "x": x, "y": y})

        try:
            if x is not None and y is not None:
                pyautogui.scroll(clicks, x, y)
            else:
                pyautogui.scroll(clicks)
            return self._emit("scroll", {"clicks": clicks, "x": x, "y": y})
        except Exception as e:
            return self._error("scroll", str(e))

    def get_position(self) -> MouseResult:
        try:
            pos = pyautogui.position()
            return self._emit("get_position", {"x": pos[0], "y": pos[1]})
        except Exception as e:
            return self._error("get_position", str(e))

    def get_screen_size(self) -> MouseResult:
        try:
            size = pyautogui.size()
            return self._emit("get_screen_size", {"width": size[0], "height": size[1]})
        except Exception as e:
            return self._error("get_screen_size", str(e))

    def _emit(self, action: str, data: dict[str, Any]) -> MouseResult:
        result = MouseResult(success=True, action=action, data=data)
        self.action_performed.emit(action, data)
        return result

    def _error(self, action: str, message: str) -> MouseResult:
        result = MouseResult(success=False, action=action, error=message)
        self.error_occurred.emit(message)
        return result
