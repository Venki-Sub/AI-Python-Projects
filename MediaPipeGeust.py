"""
MediaPipeGeust.py
-----------------
Change slides by SWIPING your index finger left or right in front of the webcam.

Idea: we remember where the index fingertip was in the previous frame.
If it moved more than `swipe_threshold` pixels horizontally, it's a swipe!

  - Swipe to the right -> Right arrow (next slide)
  - Swipe to the left  -> Left arrow  (previous slide)

Run:  python MediaPipeGeust.py   (press 'q' in the video window to quit)
"""

import cv2              # OpenCV for webcam and image processing
import mediapipe as mp  # MediaPipe for hand detection
import pyautogui        # PyAutoGUI to press keyboard keys (controls the presentation)
import time             # time, so we can wait between two swipes

# Create the MediaPipe hand detector (70% confidence needed to detect/track a hand)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open the default webcam
cap = cv2.VideoCapture(0)

# ---------- Swipe detection variables ----------
previous_position = None         # fingertip position in the previous frame (None at the start)
swipe_threshold = 100            # how many pixels the finger must move to count as a swipe
last_swipe_time = time.time()    # time of the last swipe (used to avoid double swipes)

while True:
    success, frame = cap.read()  # read one image from the webcam
    if not success:              # stop if the camera fails
        break

    # Mirror the image so moving your hand right also moves it right on screen
    frame = cv2.flip(frame, 1)
    # Convert BGR (OpenCV format) to RGB (MediaPipe format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the image
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:  # at least one hand was found
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmark for the tip of the index finger
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # Landmarks are between 0 and 1 -> multiply by image width/height to get pixels
            # frame.shape = (height, width, channels)
            current_position = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))

            # Draw the hand skeleton on the frame (just for display)
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # We can only measure movement if we know where the finger was before
            if previous_position is not None:
                # Horizontal distance moved since the last frame (positive = moved right)
                delta_x = current_position[0] - previous_position[0]
                # Big enough movement AND at least 1 second since the last swipe
                if abs(delta_x) > swipe_threshold and time.time() - last_swipe_time > 1:
                    if delta_x > 0:
                        pyautogui.press('right')  # moved right -> next slide
                        print("Next Slide")
                    else:
                        pyautogui.press('left')   # moved left -> previous slide
                        print("Previous Slide")
                    last_swipe_time = time.time()  # remember when this swipe happened

            # Save the current position for the next frame
            previous_position = current_position

    # Show the video in a window
    cv2.imshow('Hand Gesture Control', frame)

    # Wait 5 ms for a key press; quit if the key is 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Free the camera and close windows
cap.release()
cv2.destroyAllWindows()
