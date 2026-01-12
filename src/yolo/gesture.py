from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Deque, Optional

import mediapipe as mp


class Gesture(Enum):
    NONE = "none"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    FIST = "fist"
    OPEN_PALM = "open_palm"
    INDEX_POINT = "index_point"


@dataclass
class GestureConfig:
    history_size: int = 8
    swipe_threshold: float = 0.2
    fist_threshold: float = 0.2
    open_palm_threshold: float = 0.6


@dataclass
class HandState:
    wrist_x: float
    wrist_y: float
    index_tip_x: float
    index_tip_y: float
    thumb_tip_y: float
    middle_tip_y: float
    ring_tip_y: float
    pinky_tip_y: float


class GestureDetector:
    def __init__(self, config: GestureConfig) -> None:
        self._config = config
        self._history: Deque[float] = deque(maxlen=config.history_size)
        self._hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        )

    def _to_hand_state(self, landmarks) -> HandState:
        wrist = landmarks.landmark[0]
        index_tip = landmarks.landmark[8]
        thumb_tip = landmarks.landmark[4]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        return HandState(
            wrist_x=wrist.x,
            wrist_y=wrist.y,
            index_tip_x=index_tip.x,
            index_tip_y=index_tip.y,
            thumb_tip_y=thumb_tip.y,
            middle_tip_y=middle_tip.y,
            ring_tip_y=ring_tip.y,
            pinky_tip_y=pinky_tip.y,
        )

    def detect(self, frame_rgb) -> tuple[Gesture, Optional[HandState]]:
        result = self._hands.process(frame_rgb)
        if not result.multi_hand_landmarks:
            self._history.clear()
            return Gesture.NONE, None

        landmarks = result.multi_hand_landmarks[0]
        state = self._to_hand_state(landmarks)
        self._history.append(state.wrist_x)

        finger_score = sum(
            1
            for tip in (
                state.thumb_tip_y,
                state.index_tip_y,
                state.middle_tip_y,
                state.ring_tip_y,
                state.pinky_tip_y,
            )
            if tip < state.wrist_y
        )
        finger_ratio = finger_score / 5.0

        if finger_ratio <= self._config.fist_threshold:
            return Gesture.FIST, state
        if finger_ratio >= self._config.open_palm_threshold:
            return Gesture.OPEN_PALM, state

        if len(self._history) >= self._config.history_size:
            delta = self._history[-1] - self._history[0]
            if delta >= self._config.swipe_threshold:
                self._history.clear()
                return Gesture.SWIPE_RIGHT, state
            if delta <= -self._config.swipe_threshold:
                self._history.clear()
                return Gesture.SWIPE_LEFT, state

        return Gesture.INDEX_POINT, state

    def close(self) -> None:
        self._hands.close()
