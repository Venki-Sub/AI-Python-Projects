"""
01 - Face detector
------------------
Draws a green box around every face seen by the webcam.
No training needed: OpenCV comes with a ready-made face detector
(a "Haar cascade" - a model trained years ago on thousands of faces).

Run:  python 01_face_detector.py      (press 'q' to quit)
Try:  how many faces can it find at once? Does it work with a photo on your phone?
"""

import cv2  # OpenCV: camera + image processing

# Load the ready-made face detector that is installed with OpenCV
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)  # open the webcam (0 = default camera)

while True:
    ok, frame = cap.read()  # read one image
    if not ok:
        break

    # The detector works on black & white images (faster, colours don't matter for shapes)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find faces -> a list of rectangles (x, y, width, height)
    # 1.3 = how much the image is shrunk at each search step, 5 = how sure it must be
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw a rectangle: top-left corner, bottom-right corner, colour (B, G, R), thickness
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Write the number of faces at the top of the image
    cv2.putText(frame, f"Faces: {len(faces)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Face detector", frame)        # show the image in a window
    if cv2.waitKey(1) & 0xFF == ord("q"):     # quit with 'q'
        break

cap.release()            # free the camera
cv2.destroyAllWindows()  # close the window
