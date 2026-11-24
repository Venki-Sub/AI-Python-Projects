"""
07 - Dictation
--------------
Speak, and everything you say is written into notes.txt (next to this file).
Say "stop" (or type q + Enter in the terminal) to finish.

Uses Google's free speech-to-text, so you need an internet connection.

Run:  python 07_dictation.py
Try:  change LANGUAGE to "en-US" and dictate in English!
"""

import os
import threading
import time
import speech_recognition as sr

LANGUAGE = "fr-FR"
NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.txt")

def wait_for_q():
    """Wait until the user types q + Enter in the terminal."""
    try:
        while input().strip().lower() != "q":
            pass
    except EOFError:      # Ctrl+D also counts as "quit"
        pass


def run_until_q(task):
    """Run task() (the listening loop) and the keyboard at the same time.
    Stops as soon as the task ends by itself OR you type q + Enter.
    Why threads? listen() waits for the microphone and can't check the keyboard."""
    voice = threading.Thread(target=task, daemon=True)
    keys = threading.Thread(target=wait_for_q, daemon=True)
    voice.start()
    keys.start()
    while voice.is_alive() and keys.is_alive():
        time.sleep(0.1)


def dictate():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)        # learn the background noise level
        print("Speak... (say 'stop' or type q + Enter to finish)")
        while True:
            audio = recognizer.listen(mic)              # record until you stop talking
            try:
                text = recognizer.recognize_google(audio, language=LANGUAGE)  # audio -> text
            except sr.UnknownValueError:                # nothing understood -> listen again
                continue
            if text.lower() == "stop":
                break
            print("Written:", text)
            # "a" = append: add at the end of the file without erasing what is already there
            with open(NOTES, "a", encoding="utf-8") as f:
                f.write(text + "\n")


run_until_q(dictate)
print("Your notes are in", NOTES)
