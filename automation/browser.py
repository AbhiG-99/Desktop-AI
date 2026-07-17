"""Browser automation controller."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, Signal


@dataclass
class BrowserResult:
    success: bool
    action: str
    data: dict[str, Any] | None = None
    error: str | None = None


class BrowserAutomation(QObject):
    """Controls browser interactions via playwright."""

    action_performed = Signal(str, dict)
    page_loaded = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, dry_run: bool = False, parent: QObject | None = None):
        super().__init__(parent)
        self.dry_run = dry_run
        self._browser = None
        self._page = None

    def _ensure_browser(self):
        if self._browser is None:
            try:
                from playwright.sync_api import sync_playwright
                self._pw = sync_playwright().start()
                self._browser = self._pw.chromium.launch(headless=False)
                self._page = self._browser.new_page()
            except ImportError:
                raise RuntimeError("playwright is not installed. Run: pip install playwright && playwright install")

    def open(self, url: str) -> BrowserResult:
        if self.dry_run:
            return self._emit("open", {"url": url})

        try:
            self._ensure_browser()
            self._page.goto(url)
            self.page_loaded.emit(url)
            return self._emit("open", {"url": url})
        except Exception as e:
            return self._error("open", str(e))

    def find_element(self, selector: str, by: str = "css") -> BrowserResult:
        if self.dry_run:
            return self._emit("find_element", {"selector": selector, "by": by})

        try:
            self._ensure_browser()
            if by == "css":
                element = self._page.locator(selector)
            elif by == "text":
                element = self._page.get_by_text(selector)
            elif by == "role":
                element = self._page.get_by_role(selector)
            else:
                return self._error("find_element", f"Unknown selector type: {by}")

            return self._emit("find_element", {"selector": selector, "by": by, "found": element.count() > 0})
        except Exception as e:
            return self._error("find_element", str(e))

    def click_element(self, selector: str, by: str = "css") -> BrowserResult:
        if self.dry_run:
            return self._emit("click_element", {"selector": selector, "by": by})

        try:
            self._ensure_browser()
            if by == "css":
                self._page.locator(selector).click()
            elif by == "text":
                self._page.get_by_text(selector).click()
            elif by == "role":
                self._page.get_by_role(selector).click()
            else:
                return self._error("click_element", f"Unknown selector type: {by}")

            return self._emit("click_element", {"selector": selector, "by": by})
        except Exception as e:
            return self._error("click_element", str(e))

    def fill_input(self, selector: str, text: str) -> BrowserResult:
        if self.dry_run:
            return self._emit("fill_input", {"selector": selector, "text": text})

        try:
            self._ensure_browser()
            self._page.locator(selector).fill(text)
            return self._emit("fill_input", {"selector": selector, "text": text})
        except Exception as e:
            return self._error("fill_input", str(e))

    def get_text(self, selector: str | None = None) -> BrowserResult:
        if self.dry_run:
            return self._emit("get_text", {"selector": selector})

        try:
            self._ensure_browser()
            if selector:
                text = self._page.locator(selector).inner_text()
            else:
                text = self._page.inner_text("body")
            return self._emit("get_text", {"selector": selector, "text": text})
        except Exception as e:
            return self._error("get_text", str(e))

    def screenshot(self, path: str | None = None) -> BrowserResult:
        if self.dry_run:
            return self._emit("screenshot", {"path": path})

        try:
            self._ensure_browser()
            path = path or "screenshot.png"
            self._page.screenshot(path=path)
            return self._emit("screenshot", {"path": path})
        except Exception as e:
            return self._error("screenshot", str(e))

    def close(self) -> BrowserResult:
        if self.dry_run:
            return self._emit("close", {})

        try:
            if self._browser:
                self._browser.close()
            if self._pw:
                self._pw.stop()
            self._browser = None
            self._page = None
            self._pw = None
            return self._emit("close", {})
        except Exception as e:
            return self._error("close", str(e))

    def _emit(self, action: str, data: dict[str, Any]) -> BrowserResult:
        result = BrowserResult(success=True, action=action, data=data)
        self.action_performed.emit(action, data)
        return result

    def _error(self, action: str, message: str) -> BrowserResult:
        result = BrowserResult(success=False, action=action, error=message)
        self.error_occurred.emit(message)
        return result
