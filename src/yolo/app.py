import time

import cv2

from .camera import CameraConfig, CameraStream
from .controller import ControllerConfig, SlideController
from .gesture import Gesture, GestureConfig, GestureDetector
from .laser import LaserConfig, LaserPointer


def draw_status(frame, gesture: Gesture, mode: str) -> None:
    cv2.putText(
        frame,
        f"Gesture: {gesture.value}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        f"Mode: {mode}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )


def run() -> None:
    camera = CameraStream(CameraConfig())
    detector = GestureDetector(GestureConfig())
    laser = LaserPointer(LaserConfig())
    controller = SlideController(ControllerConfig(), laser)

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gesture, hand_state = detector.detect(frame_rgb)
            controller.handle_gesture(gesture, hand_state, time.time())

            draw_status(frame, gesture, controller.mode.value)
            cv2.imshow("Yolo Presenter", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        detector.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
