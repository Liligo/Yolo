from dataclasses import dataclass
from typing import Optional

import pyautogui

from .gesture import HandState


@dataclass
class LaserConfig:
    smoothing: float = 0.35
    clamp_margin: float = 0.02


class LaserPointer:
    def __init__(self, config: LaserConfig) -> None:
        self._config = config
        self._last_x: Optional[float] = None
        self._last_y: Optional[float] = None
        self._screen_width, self._screen_height = pyautogui.size()

    def update(self, hand_state: HandState) -> None:
        x = min(max(hand_state.index_tip_x, 0.0), 1.0)
        y = min(max(hand_state.index_tip_y, 0.0), 1.0)
        x = self._config.clamp_margin + x * (1 - 2 * self._config.clamp_margin)
        y = self._config.clamp_margin + y * (1 - 2 * self._config.clamp_margin)

        if self._last_x is None or self._last_y is None:
            self._last_x = x
            self._last_y = y
        else:
            self._last_x = self._last_x + (x - self._last_x) * self._config.smoothing
            self._last_y = self._last_y + (y - self._last_y) * self._config.smoothing

        screen_x = int(self._last_x * self._screen_width)
        screen_y = int(self._last_y * self._screen_height)
        pyautogui.moveTo(screen_x, screen_y)
