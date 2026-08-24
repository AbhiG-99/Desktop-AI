"""Automation service — bridges the AI layer to desktop automation."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from automation import AutomationManager


_manager: AutomationManager | None = None


def get_manager() -> AutomationManager:
    global _manager

    if _manager is None:
        dry_run = os.getenv("DESKTOP_AI_DRY_RUN", "0") == "1"
        _manager = AutomationManager(dry_run=dry_run)

    return _manager


def get_capabilities() -> list[str]:
    return get_manager().get_capabilities()


def execute_action(action: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        result = get_manager().execute(action, params or {})
    except Exception as e:
        return {"success": False, "action": action, "error": str(e)}

    if result is None:
        return {"success": False, "action": action, "error": f"Unknown action: {action}"}

    return {
        "success": bool(result.success),
        "action": result.action,
        "data": result.data,
        "error": result.error,
    }


def parse_ai_action(response: str) -> dict[str, Any] | None:
    """Extract an automation request from an AI response.

    Expected shape: {"action": "<name>", "params": {...}, "say": "<message>"}
    Returns the parsed dict, or None if the response contains no valid action.
    """
    text = response.strip()
    candidates: list[str] = []

    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        candidates.append(fence.group(1))

    start = text.find("{")
    while start != -1:
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(text[start:i + 1])
                    break
        start = text.find("{", start + 1)

    for candidate in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("action"), str):
            return obj

    return None
