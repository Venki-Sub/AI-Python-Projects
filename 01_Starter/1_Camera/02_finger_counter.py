"""
02 - Finger counter
-------------------
Shows how many fingers you are holding up (0 to 5), using MediaPipe hand tracking.

How do we know a finger is UP?
  MediaPipe gives 21 points on the hand (see the picture in the README).
  For a finger, if its TIP is higher on the screen than its middle joint, it is up.
  (On images, y = 0 is the TOP, so "higher" means a SMALLER y.)

Run:  python 02_finger_counter.py      (press 'q' to quit)
"""

import cv2
import mediapipe as mp

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)  # hand detector
draw = mp.solutions.drawing_utils                                                # to draw the hand

FINGER_TIPS = [8, 12, 16, 20]  # tips of index, middle, ring and pinky fingers


def count_fingers(points):
    """Count the raised fingers from the 21 hand points."""
    count = 0
    for tip in FINGER_TIPS:
        if points[tip].y < points[tip - 2].y:  # tip above the middle joint -> finger is up
            count += 1
    # The thumb moves sideways, not up: it is "open" when its tip (4) is
    # farther from the pinky base (17) than its joint (3) is.
    if abs(points[4].x - points[17].x) > abs(points[3].x - points[17].x):
        count += 1
    return count


cap = cv2.VideoCapture(0)
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)  # mirror effect

    # MediaPipe needs RGB colours, OpenCV gives BGR
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    fingers = 0
    if result.multi_hand_landmarks:                      # a hand was found
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        fingers = count_fingers(hand.landmark)

    cv2.putText(frame, f"Fingers: {fingers}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
    cv2.imshow("Finger counter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
