"""
CapturePhoto.py
---------------
Beginner project: take ONE photo with your webcam and save it to your Desktop.

What you learn:
  - How to open the webcam with OpenCV
  - How to read a single frame (= one image)
  - How to show an image in a window and save it to a file

Run:  python CapturePhoto.py   (press any key in the photo window to close it)
"""

import cv2  # OpenCV: the library we use to work with cameras and images
import os   # os: helps us build file paths that work on Mac, Windows and Linux

# Build the path to the Desktop folder, e.g. "/Users/you/Desktop"
# os.path.expanduser("~") gives the home folder of the current user
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Open the webcam. 0 = the default (built-in) camera, 1 = a second camera, etc.
cap = cv2.VideoCapture(0)

# Make sure the camera really opened (it can fail if another app is using it
# or if the terminal has no permission to use the camera)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()  # stop the program, nothing else can work without a camera

# Read one frame from the camera
#   ret   -> True if reading worked, False otherwise
#   frame -> the image itself (a NumPy array of pixels in BGR colour order)
ret, frame = cap.read()

# Only continue if we actually got an image
if ret:
    # Open a window called 'Captured Image' and show the photo inside it
    cv2.imshow('Captured Image', frame)

    # Build the full file name: <Desktop>/captured_image.jpg
    file_path = os.path.join(desktop_path, 'captured_image.jpg')
    # Write the image to disk as a JPG file
    cv2.imwrite(file_path, frame)
    # Tell the user where the photo was saved (f-string inserts the variable)
    print(f"Photo taken and saved as '{file_path}'")
else:
    # The camera opened but did not give us a picture
    print("Error: Could not read frame.")

# Wait until the user presses any key (0 = wait forever)
cv2.waitKey(0)
# Release the camera so other apps can use it again
cap.release()
# Close every window that OpenCV opened
cv2.destroyAllWindows()
