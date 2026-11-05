"""
ControlPPTGesture.py
--------------------
Control a PowerPoint / Keynote / Google Slides presentation with HAND GESTURES.

How it works:
  1. The webcam films your hand.
  2. MediaPipe finds 21 "landmarks" (key points) on your hand.
  3. We compare the positions of the thumb and index finger to guess a gesture.
  4. PyAutoGUI presses a keyboard key for you (Right, Left, F5, Esc).

Gestures:
  - Index finger LEFT of thumb, same height  -> "next"     -> Right arrow
  - Index finger RIGHT of thumb, same height -> "previous" -> Left arrow
  - Thumb up                                 -> "start"    -> F5
  - Thumb down                               -> "exit"     -> Esc

Hand landmark numbers used here (MediaPipe numbering):
  3 = thumb joint, 4 = thumb tip, 8 = index tip, 9 = middle finger base, 12 = middle finger tip

Run:  python ControlPPTGesture.py   (press 'q' in the video window to quit)
"""

import cv2                 # OpenCV: read the webcam and draw on images
import mediapipe as mp     # MediaPipe: Google's library for hand tracking & pose detection
import pyautogui           # PyAutoGUI: lets Python press keys and move the mouse

# ---------- Set up MediaPipe ----------
mp_hands = mp.solutions.hands  # shortcut to the "hands" solution
# Create the hand detector:
#   max_num_hands=1              -> only track one hand (simpler, faster)
#   min_detection_confidence=0.7 -> must be 70% sure it sees a hand
#   min_tracking_confidence=0.7  -> must be 70% sure while following the hand
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils  # helper to draw the hand skeleton on the image

# ---------- Open the webcam ----------
cap = cv2.VideoCapture(0)  # 0 = default camera

# This variable stores the last gesture we recognised (None = no gesture)
gesture = None


def detect_gesture(landmarks):
    """Look at the hand landmarks and set the global 'gesture' variable."""
    global gesture  # we want to change the variable defined outside this function

    # Landmarks have x and y between 0 and 1 (0 = left/top, 1 = right/bottom of the image)
    thumb_tip = landmarks[4]   # tip of the thumb
    index_tip = landmarks[8]   # tip of the index finger

    # Index is to the LEFT of the thumb and both are at about the same height -> next slide
    if index_tip.x < thumb_tip.x and abs(index_tip.y - thumb_tip.y) < 0.1:
        gesture = "next"
    # Index is to the RIGHT of the thumb and both are at about the same height -> previous slide
    elif index_tip.x > thumb_tip.x and abs(index_tip.y - thumb_tip.y) < 0.1:
        gesture = "previous"
    # Thumb tip is ABOVE its joint (smaller y = higher) and middle finger is folded -> thumbs up
    elif thumb_tip.y < landmarks[3].y and landmarks[12].y > landmarks[9].y:
        gesture = "start"
    # Thumb tip is BELOW its joint and middle finger is pointing up -> thumbs down
    elif thumb_tip.y > landmarks[3].y and landmarks[12].y < landmarks[9].y:
        gesture = "exit"


# ---------- Main loop: runs once per video frame ----------
while cap.isOpened():
    ret, frame = cap.read()  # grab one image from the webcam
    if not ret:              # if the camera stopped sending images, leave the loop
        break

    # Flip horizontally so the video behaves like a mirror (more natural for the user)
    frame = cv2.flip(frame, 1)
    # OpenCV uses BGR colours but MediaPipe expects RGB, so we convert
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Ask MediaPipe to find hands in this image
    result = hands.process(rgb_frame)

    # multi_hand_landmarks is None when no hand is visible
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw the 21 points and the lines between them on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Decide which gesture the hand is making
            detect_gesture(hand_landmarks.landmark)

            # Press the matching key, then reset the gesture so it is not repeated
            if gesture == "next":
                pyautogui.press("right")   # Right arrow = next slide
                print("Swipe Right")
                gesture = None
            elif gesture == "previous":
                pyautogui.press("left")    # Left arrow = previous slide
                print("Swipe Left")
                gesture = None
            elif gesture == "start":
                pyautogui.press("f5")      # F5 = start the slideshow (PowerPoint)
                print("Thumb Up Start")
                gesture = None
            elif gesture == "exit":
                pyautogui.press("esc")     # Esc = leave the slideshow
                print("Thumb Down Exit")
                gesture = None

    # Show the webcam image (with the hand drawing) in a window
    cv2.imshow("Hand Gesture Control", frame)

    # Wait 1 ms for a key; if it is 'q', stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------- Cleanup ----------
cap.release()            # free the webcam
cv2.destroyAllWindows()  # close the video window
hands.close()            # free MediaPipe resources
