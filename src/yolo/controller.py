from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pyautogui

from .gesture import Gesture, HandState
from .laser import LaserPointer


class Mode(Enum):
    SLIDE = "slide"
    LASER = "laser"


@dataclass
class ControllerConfig:
    cooldown_seconds: float = 0.5


class SlideController:
    def __init__(self, config: ControllerConfig, laser: LaserPointer) -> None:
        self._config = config
        self._laser = laser
        self._mode = Mode.SLIDE
        self._last_trigger: Optional[float] = None

    @property
    def mode(self) -> Mode:
        return self._mode

    def handle_gesture(self, gesture: Gesture, hand_state: Optional[HandState], now: float) -> None:
        if gesture == Gesture.FIST:
            self._mode = Mode.SLIDE
            return
        if gesture == Gesture.OPEN_PALM:
            self._mode = Mode.LASER
            return

        if self._mode == Mode.LASER:
            if hand_state:
                self._laser.update(hand_state)
            return

        if gesture == Gesture.SWIPE_RIGHT and self._can_trigger(now):
            pyautogui.press("right")
            self._last_trigger = now
        elif gesture == Gesture.SWIPE_LEFT and self._can_trigger(now):
            pyautogui.press("left")
            self._last_trigger = now

    def _can_trigger(self, now: float) -> bool:
        if self._last_trigger is None:
            return True
        return (now - self._last_trigger) >= self._config.cooldown_seconds
