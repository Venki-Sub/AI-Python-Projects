"""
SpeechRecognition.py
--------------------
The simplest VOICE project: speak French commands to click the mouse.

  "clic gauche" = left click     "clic droit" = right click
  "double clic" = double click   "arrêt"      = stop the program

To quit from the keyboard: type q then press Enter in the terminal.

Uses Google's free speech-to-text service, so you need an internet connection.
(Change language="fr-FR" to "en-US" and the command words to use English!)

Run:  python SpeechRecognition.py   (type q + Enter, or say "arrêt", to quit)
"""

import speech_recognition as sr  # SpeechRecognition: turns microphone audio into text
import pyautogui                 # PyAutoGUI: controls the mouse & keyboard
import threading                 # threading: run code in parallel (in a "thread")
import time                      # time: small pauses with time.sleep()


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


def wait_for_q():
    """Wait until the user types q + Enter in the terminal.
    (A terminal only sends what you type after you press Enter.)"""
    try:
        while input().strip().lower() != "q":
            pass
    except EOFError:      # Ctrl+D also counts as "quit"
        pass


# Start voice command listening in a separate thread
voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
voice_thread.start()
# And the keyboard in another one, so both can happen at the same time
key_thread = threading.Thread(target=wait_for_q, daemon=True)
key_thread.start()

print("Type q + Enter (or say \"arrêt\") to quit.")
# Wait until one of the two threads ends: "arrêt" was said OR q was typed
while voice_thread.is_alive() and key_thread.is_alive():
    time.sleep(0.1)
print("Voice command listener stopped.")  # daemon=True -> the other thread stops with the program
