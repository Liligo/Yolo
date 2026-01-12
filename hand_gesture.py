import collections
import time

import cv2
import mediapipe as mp


class GestureState:
    def __init__(self, cooldown_s=0.6, swipe_window_s=0.6, swipe_threshold=0.18):
        self.cooldown_s = cooldown_s
        self.swipe_window_s = swipe_window_s
        self.swipe_threshold = swipe_threshold
        self.last_emit_time = 0.0
        self.track = collections.deque()

    def in_cooldown(self):
        return time.time() - self.last_emit_time < self.cooldown_s

    def mark_emit(self):
        self.last_emit_time = time.time()

    def update_track(self, center_x):
        now = time.time()
        self.track.append((now, center_x))
        while self.track and now - self.track[0][0] > self.swipe_window_s:
            self.track.popleft()

    def detect_swipe(self):
        if len(self.track) < 2:
            return None
        start_t, start_x = self.track[0]
        end_t, end_x = self.track[-1]
        delta = end_x - start_x
        if abs(delta) < self.swipe_threshold:
            return None
        return "right" if delta > 0 else "left"


def finger_extended(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y


def thumb_extended(landmarks):
    return landmarks[4].x > landmarks[3].x


def classify_hand(landmarks):
    extended = [
        thumb_extended(landmarks),
        finger_extended(landmarks, 8, 6),
        finger_extended(landmarks, 12, 10),
        finger_extended(landmarks, 16, 14),
        finger_extended(landmarks, 20, 18),
    ]
    count = sum(extended)
    if count >= 4:
        return "open"
    if count <= 1:
        return "fist"
    return "unknown"


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera")

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    state = GestureState()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        gesture = None
        swipe = None

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                gesture = classify_hand(landmarks)
                center_x = landmarks[0].x
                state.update_track(center_x)
                swipe = state.detect_swipe()
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                break

        label = None
        if gesture in {"open", "fist"}:
            label = gesture
        if swipe:
            label = f"swipe_{swipe}"

        if label and not state.in_cooldown():
            state.mark_emit()
            cv2.putText(
                frame,
                f"Gesture: {label}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
            )
        else:
            cv2.putText(
                frame,
                "Gesture: ...",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (100, 100, 100),
                2,
            )

        cv2.imshow("Hand Gesture", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
