"""
05 - Smile camera
-----------------
Takes a photo automatically when you smile! :)
Uses two ready-made OpenCV detectors: one for faces, one for smiles.
Photos are saved in a "photos" folder next to this file (they are NOT uploaded to GitHub).

Run:  python 05_smile_camera.py      (press 'q' to quit)
"""

import os
import time
import cv2

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

# Folder where photos are saved: <this file's folder>/photos
PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")
os.makedirs(PHOTO_DIR, exist_ok=True)  # create it if it doesn't exist yet

last_photo = 0  # time of the last photo, so we don't take 30 photos per second

cap = cv2.VideoCapture(0)
while True:
    ok, frame = cap.read()
    if not ok:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smiling = False

    for (x, y, w, h) in face_detector.detectMultiScale(gray, 1.3, 5):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Only look for a smile INSIDE the face, in its lower half (where the mouth is)
        mouth_zone = gray[y + h // 2: y + h, x: x + w]
        # 1.7 and 22: smiles are hard to detect, so we need to be strict to avoid mistakes
        if len(smile_detector.detectMultiScale(mouth_zone, 1.7, 22)) > 0:
            smiling = True

    # Smile + at least 3 seconds since the last photo -> take a photo
    if smiling and time.time() - last_photo > 3:
        name = os.path.join(PHOTO_DIR, f"smile_{int(time.time())}.jpg")
        cv2.imwrite(name, frame)       # save the image (before writing text on it)
        print("Photo saved:", name)
        last_photo = time.time()

    text = "SMILE DETECTED!" if smiling else "Smile for a photo..."
    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Smile camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
