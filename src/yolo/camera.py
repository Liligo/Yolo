from dataclasses import dataclass

import cv2


@dataclass
class CameraConfig:
    device_index: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30


class CameraStream:
    def __init__(self, config: CameraConfig) -> None:
        self._config = config
        self._capture = cv2.VideoCapture(config.device_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self._capture.set(cv2.CAP_PROP_FPS, config.fps)

    def read(self):
        return self._capture.read()

    def release(self) -> None:
        self._capture.release()
