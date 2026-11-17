"""
04 - Draw in the air
--------------------
Your index finger becomes a pen!
  - Index finger UP, middle finger DOWN  -> you draw
  - Index AND middle fingers UP          -> pen lifted (move without drawing)

Run:  python 04_air_drawing.py      ('c' = clear the drawing, 'q' = quit)
"""

import cv2
import numpy as np
import mediapipe as mp

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

canvas = None       # a black image where we keep the drawing (created with the first frame)
previous = None     # where the finger was in the previous frame (None = pen lifted)
COLOR = (255, 0, 255)  # pen colour in B, G, R -> purple

cap = cv2.VideoCapture(0)
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)  # same size as the camera image, all black

    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        p = result.multi_hand_landmarks[0].landmark
        h, w, _ = frame.shape
        x, y = int(p[8].x * w), int(p[8].y * h)       # index fingertip in pixels

        index_up = p[8].y < p[6].y                    # tip above its joint
        middle_up = p[12].y < p[10].y

        if index_up and not middle_up:                # drawing mode
            if previous is not None:
                cv2.line(canvas, previous, (x, y), COLOR, 8)   # draw from last point to new point
            previous = (x, y)
        else:                                         # pen lifted
            previous = None
        cv2.circle(frame, (x, y), 10, COLOR, -1)      # show where the pen is (-1 = filled)
    else:
        previous = None

    # Put the drawing on top of the camera image: wherever the canvas is not black, use its colour
    mask = canvas.any(axis=2)
    frame[mask] = canvas[mask]

    cv2.putText(frame, "c = clear   q = quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Air drawing", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("c"):
        canvas[:] = 0        # set every pixel back to black
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
