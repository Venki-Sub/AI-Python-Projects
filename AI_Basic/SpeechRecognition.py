"""
SpeechRecognition.py
--------------------
The simplest VOICE project: speak French commands to click the mouse.

  "clic gauche" = left click     "clic droit" = right click
  "double clic" = double click   "arrêt"      = stop the program

Uses Google's free speech-to-text service, so you need an internet connection.
(Change language="fr-FR" to "en-US" and the command words to use English!)

Run:  python SpeechRecognition.py
"""

import speech_recognition as sr  # SpeechRecognition: turns microphone audio into text
import pyautogui                 # PyAutoGUI: controls the mouse & keyboard
import threading                 # threading: run code in parallel (in a "thread")


def listen_for_commands():
    """Listen to the microphone in a loop and click when a command is recognised."""
    recognizer = sr.Recognizer()          # the speech-to-text engine
    with sr.Microphone() as source:       # open the default microphone
        print("Listening for voice commands...")
        while True:
            try:
                # Learn what the background noise sounds like (helps accuracy)
                recognizer.adjust_for_ambient_noise(source)
                # Record what you say (gives up after 4 seconds of silence)
                audio = recognizer.listen(source, timeout=4)
                # Send audio to Google -> get text back (French), in lower case
                command = recognizer.recognize_google(audio, language="fr-FR").lower()
                print(f"Voice command detected: {command}")

                # Voice commands handling: compare the text with our commands
                if command == "clic gauche":                 # left click
                    pyautogui.click(button="left")
                elif command == "clic droit":                # right click
                    pyautogui.click(button="right")
                elif command == "double clic":               # double click
                    pyautogui.doubleClick(button="left")
                elif command == "arrêt":                     # stop
                    print("Stopping voice command listener.")
                    break  # exit the while loop -> function ends -> thread ends

            # Catch the 3 common errors in ONE line:
            #   UnknownValueError -> speech not understood
            #   RequestError      -> no internet / API problem
            #   WaitTimeoutError  -> nobody spoke
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
                print(f"Error: {str(e)}")


# Start voice command listening in a separate thread
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()

voice_thread.join()  # join() = wait here until the thread is finished (after "arrêt")
print("Voice command thread has completed.")
