"""
MediaPipeSpeechUI.py
--------------------
A small desktop APP (Tkinter window) that combines two AI inputs:

  1. HAND  -> your index finger moves the mouse cursor (MediaPipe)
  2. VOICE -> you say a command in French to click (Google Speech Recognition)

Voice commands (French):
  "clic gauche" = left click     "clic droit" = right click
  "double clic" = double click   "arrêt"      = stop listening

Why a thread? Listening to the microphone "blocks" (waits) until you speak.
If we did that in the main program, the video would freeze. So the voice
part runs in a separate THREAD, in parallel with the video.

Run:  python MediaPipeSpeechUI.py   (close the window to quit)
"""

import cv2                                 # OpenCV: webcam + image processing
import mediapipe as mp                     # MediaPipe: hand tracking
import pyautogui                           # PyAutoGUI: clicks + screen size
import speech_recognition as sr            # SpeechRecognition: microphone -> text
from pynput.mouse import Controller        # pynput: move the mouse cursor smoothly
import threading                           # threading: run voice listening in parallel
import tkinter as tk                       # Tkinter: Python's built-in GUI (window) library
from tkinter import messagebox             # messagebox: small pop-up windows
from PIL import Image, ImageTk             # Pillow: convert OpenCV images for Tkinter

# ---------- Set up MediaPipe and the mouse ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mouse = Controller()  # object we use to move the mouse

# Open the webcam and get the screen size in pixels (e.g. 1920 x 1080)
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# ---------- Smoothing ----------
# Hand detection "shakes" a little. To get a smooth cursor we mix the new
# position with the old one:  new = alpha * old + (1 - alpha) * measured
prev_screen_x, prev_screen_y = 0, 0
alpha = 0.6  # 0 = no smoothing (jumpy), closer to 1 = very smooth but slower

# ---------- Create the main window ----------
root = tk.Tk()                       # the main application window
root.title("Gesture Control App")    # text in the title bar
root.geometry("800x600")             # window size: width x height

# A Label widget can display an image -> we use it to show the webcam video
video_label = tk.Label(root)
video_label.pack()  # pack() places the widget in the window


def show_message(command):
    """Show a pop-up telling the user which voice command was detected."""
    messagebox.showinfo("Voice Command Detected", command)


def listen_for_commands():
    """Runs forever in a background thread: listen -> convert to text -> act."""
    recognizer = sr.Recognizer()   # the object that turns audio into text
    microphone = sr.Microphone()   # the default microphone

    while True:
        try:
            with microphone as source:
                # Measure background noise so the recognizer knows what "silence" is
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                # Record until the user stops talking (give up after 4 s of silence)
                audio = recognizer.listen(source, timeout=4)
                # Send the audio to Google's free speech API, in French, and lower-case it
                command = recognizer.recognize_google(audio, language="fr-FR").lower()
                print(f"Detected command: {command}")

                # Do the action that matches the spoken words
                if command == "clic gauche":            # "left click"
                    pyautogui.click(button="left")
                    show_message("Left Click")
                elif command == "clic droit":           # "right click"
                    pyautogui.click(button="right")
                    show_message("Right Click")
                elif command == "double clic":          # "double click"
                    pyautogui.doubleClick(button="left")
                    show_message("Double Click")
                elif command == "arrêt":                # "stop"
                    break  # leave the loop -> the thread ends

        except sr.UnknownValueError:      # Google heard something but couldn't understand it
            print("Command not recognized.")
        except sr.RequestError as e:      # no internet / Google service problem
            print(f"Error with the recognition service: {e}")
        except sr.WaitTimeoutError:       # nobody spoke during the timeout
            print("Listening timeout.")


# Start the voice thread. daemon=True means it stops automatically when the app closes.
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()


def update_cursor():
    """Read one webcam frame, move the mouse, show the frame, then schedule itself again."""
    global prev_screen_x, prev_screen_y  # we update these variables defined outside
    success, frame = cap.read()
    if not success:
        return  # no image -> stop updating

    frame = cv2.flip(frame, 1)                           # mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # MediaPipe wants RGB

    # Find hands in the image
    results_hands = hands.process(rgb_frame)

    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # Position of the index fingertip, between 0 and 1
            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # Convert to screen pixels (0..1 -> 0..screen size)
            screen_x = int(x * screen_width)
            screen_y = int(y * screen_height)

            # Smooth the movement (see explanation of alpha above)
            screen_x = int(alpha * prev_screen_x + (1 - alpha) * screen_x)
            screen_y = int(alpha * prev_screen_y + (1 - alpha) * screen_y)
            prev_screen_x, prev_screen_y = screen_x, screen_y  # remember for next frame

            # Actually move the mouse cursor
            mouse.position = (screen_x, screen_y)

    # Convert the OpenCV image (NumPy array) into an image Tkinter can display
    # Tip for students: 'frame' is BGR, so colours look blue-ish. Try using rgb_frame here!
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk            # keep a reference, otherwise Python deletes the image
    video_label.configure(image=imgtk)   # show the new image in the label

    # Ask Tkinter to call this function again in 10 ms -> this creates our "video loop"
    root.after(10, update_cursor)


# Start the first update (it then keeps calling itself)
update_cursor()

# Start the Tkinter event loop: keeps the window open and responsive until it is closed
root.mainloop()

# Cleanup after the window is closed
cap.release()
cv2.destroyAllWindows()
