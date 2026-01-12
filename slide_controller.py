from __future__ import annotations

import importlib.util
import platform
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional


class SlideController(ABC):
    """Unified interface for slide navigation across multiple control backends."""

    @abstractmethod
    def next_slide(self) -> None:
        """Advance to the next slide."""

    @abstractmethod
    def previous_slide(self) -> None:
        """Return to the previous slide."""


@dataclass(frozen=True)
class KeyboardConfig:
    backend: Literal["pynput", "pyautogui"] = "pynput"
    next_key: str = "pagedown"
    previous_key: str = "pageup"


class KeyboardSlideController(SlideController):
    """Simulate keyboard presses to control slides."""

    def __init__(self, config: Optional[KeyboardConfig] = None) -> None:
        self._config = config or KeyboardConfig()
        self._ensure_backend_available()

    def next_slide(self) -> None:
        self._send_key(self._config.next_key)

    def previous_slide(self) -> None:
        self._send_key(self._config.previous_key)

    def _ensure_backend_available(self) -> None:
        if importlib.util.find_spec(self._config.backend) is None:
            raise RuntimeError(
                f"Keyboard backend '{self._config.backend}' is not available."
            )

    def _send_key(self, key_name: str) -> None:
        if self._config.backend == "pynput":
            self._send_with_pynput(key_name)
        else:
            self._send_with_pyautogui(key_name)

    def _send_with_pynput(self, key_name: str) -> None:
        from pynput.keyboard import Controller, Key

        mapping = {
            "pagedown": Key.page_down,
            "pageup": Key.page_up,
            "right": Key.right,
            "left": Key.left,
            "space": Key.space,
        }
        controller = Controller()
        key = mapping.get(key_name, key_name)
        controller.press(key)
        controller.release(key)

    def _send_with_pyautogui(self, key_name: str) -> None:
        import pyautogui

        pyautogui.press(key_name)


@dataclass(frozen=True)
class WindowsCOMConfig:
    application: str = "PowerPoint.Application"


class WindowsCOMSlideController(SlideController):
    """Use pywin32 COM automation on Windows for enhanced control."""

    def __init__(self, config: Optional[WindowsCOMConfig] = None) -> None:
        self._config = config or WindowsCOMConfig()
        if platform.system() != "Windows":
            raise RuntimeError("Windows COM controller is only available on Windows.")
        if importlib.util.find_spec("win32com.client") is None:
            raise RuntimeError("pywin32 is required for Windows COM control.")

    def next_slide(self) -> None:
        view = self._get_slide_show_view()
        view.Next()

    def previous_slide(self) -> None:
        view = self._get_slide_show_view()
        view.Previous()

    def _get_slide_show_view(self):
        from win32com.client import Dispatch

        app = Dispatch(self._config.application)
        if app.SlideShowWindows.Count > 0:
            return app.SlideShowWindows(1).View
        presentation = app.ActivePresentation
        presentation.SlideShowSettings.Run()
        return app.SlideShowWindows(1).View


@dataclass(frozen=True)
class MacAppleScriptConfig:
    application: str = "Keynote"


class MacAppleScriptSlideController(SlideController):
    """Use AppleScript automation on macOS for slide control."""

    def __init__(self, config: Optional[MacAppleScriptConfig] = None) -> None:
        self._config = config or MacAppleScriptConfig()
        if platform.system() != "Darwin":
            raise RuntimeError("AppleScript controller is only available on macOS.")

    def next_slide(self) -> None:
        self._run_script("show next")

    def previous_slide(self) -> None:
        self._run_script("show previous")

    def _run_script(self, command: str) -> None:
        script = (
            f'tell application "{self._config.application}"\n'
            "    activate\n"
            "    if (count of documents) > 0 then\n"
            f"        tell slideshow 1 to {command}\n"
            "    end if\n"
            "end tell"
        )
        subprocess.run(["osascript", "-e", script], check=True)


def get_slide_controller(
    mode: Literal["keyboard", "windows_com", "mac_applescript"] = "keyboard",
    **kwargs,
) -> SlideController:
    """Factory helper for slide controller implementations."""
    if mode == "keyboard":
        return KeyboardSlideController(**kwargs)
    if mode == "windows_com":
        return WindowsCOMSlideController(**kwargs)
    if mode == "mac_applescript":
        return MacAppleScriptSlideController(**kwargs)
    raise ValueError(f"Unknown slide controller mode: {mode}")
