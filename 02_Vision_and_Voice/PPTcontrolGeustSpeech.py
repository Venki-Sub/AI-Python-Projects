"""
PPTcontrolGeustSpeech.py
------------------------
Control your computer with HAND + VOICE, without any window (runs in the background).

  - Your index finger moves the mouse cursor (MediaPipe hand tracking)
  - French voice commands click for you (Google Speech Recognition):
        "clic gauche" = left click   "clic droit" = right click
        "double clic" = double click "arrêt"      = stop the program

Great for controlling a presentation from a distance!
(The original comments are in French - English translations are added next to them.)

Run:  python PPTcontrolGeustSpeech.py   (say "arrêt" to quit)
"""

import sys                              # sys: system functions (not used yet, handy for sys.exit())
import cv2                              # OpenCV: image & video
import mediapipe as mp                  # MediaPipe: hand tracking & pose detection
import pyautogui                        # PyAutoGUI: mouse clicks & keyboard
import speech_recognition as sr         # SpeechRecognition: voice -> text
from pynput.mouse import Controller     # pynput: move the mouse
import threading                        # threading: listen to the voice in parallel

# Initialisation de MediaPipe  (= set up the MediaPipe hand detector)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mouse = Controller()  # object used to move the mouse cursor

# Capture de la caméra  (= open the webcam)
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()  # screen resolution in pixels

# Variables pour le lissage  (= smoothing variables, so the cursor doesn't shake)
prev_screen_x, prev_screen_y = 0, 0
alpha = 0.6  # Ajustez pour un lissage plus ou moins fort (= adjust for more/less smoothing)


# Thread d'écoute pour les commandes vocales.  (= background thread that listens to voice commands)
def listen_for_commands():
    # Configuration de la reconnaissance vocale  (= set up speech recognition)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    # Variable pour stocker la commande vocale  (= variable that stores the voice command)
    voice_command = None

    while True:              # outer loop: repeat forever (listen, then act)
        while True:          # inner loop: try to hear ONE command, then break out
            try:
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)       # calibrate to room noise
                    print("Écoute en cours...")                       # "Listening..."
                    audio = recognizer.listen(source, timeout=4)      # record (max 4 s waiting)
                    # Speech -> text using Google, French language, lower-case
                    command = recognizer.recognize_google(audio, language="fr-FR").lower()
                    print(f"Commande vocale détectée : {command}")    # "Voice command detected"
                    voice_command = command
                    break
            except sr.UnknownValueError:            # could not understand the audio
                print("Aucune commande vocale reconnue.")   # "No voice command recognised"
                break
            except sr.RequestError as e:            # internet / API problem
                print(f"Erreur de reconnaissance vocale : {e}")   # "Speech recognition error"
                break
            except sr.WaitTimeoutError:             # nobody spoke in time
                print("Temps d'attente écoulé.")    # "Timeout"
                break
        # Traiter les commandes vocales  (= handle the voice command)
        if voice_command == "clic gauche":          # "left click"
            pyautogui.click(button="left")
            voice_command = None  # Réinitialiser après traitement (= reset after use)
        elif voice_command == "clic droit":         # "right click"
            pyautogui.click(button="right")
            voice_command = None
        elif voice_command == "double clic":        # "double click"
            pyautogui.doubleClick(button="left")
            voice_command = None
        elif voice_command == "arrêt":              # "stop" -> end the thread
            return

        # Lancer le thread d'écoute des commandes vocales


# Start the voice thread (daemon=True: it dies automatically when the main program ends)
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()

# ---------- Main loop: one turn per webcam frame ----------
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Prétraitement  (= pre-processing)
    frame = cv2.flip(frame, 1)                           # mirror the image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # BGR -> RGB for MediaPipe

    # Détection de la main  (= hand detection)
    results_hands = hands.process(rgb_frame)

    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # Coordonnées normalisées  (= normalised coordinates, between 0 and 1)
            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

            # Conversion en coordonnées écran  (= convert to screen pixels)
            screen_x = int(x * screen_width)
            screen_y = int(y * screen_height)

            # Lissage  (= smoothing: mix old and new positions)
            screen_x = int(alpha * prev_screen_x + (1 - alpha) * screen_x)
            screen_y = int(alpha * prev_screen_y + (1 - alpha) * screen_y)
            prev_screen_x, prev_screen_y = screen_x, screen_y

            # Déplacement du curseur  (= move the mouse cursor)
            mouse.position = (screen_x, screen_y)

    # Affichage  (= display). Uncomment the next line to see the webcam video
    # cv2.imshow('Frame', frame)
    if voice_thread.is_alive() == False:   # the user said "arrêt" -> voice thread ended -> quit
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' only works if a cv2 window is open
        break

# Free the camera and close windows
cap.release()
cv2.destroyAllWindows()
