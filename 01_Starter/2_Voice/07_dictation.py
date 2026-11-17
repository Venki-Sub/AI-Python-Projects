"""
07 - Dictation
--------------
Speak, and everything you say is written into notes.txt (next to this file).
Say "stop" to finish.

Uses Google's free speech-to-text, so you need an internet connection.

Run:  python 07_dictation.py
Try:  change LANGUAGE to "en-US" and dictate in English!
"""

import os
import speech_recognition as sr

LANGUAGE = "fr-FR"
NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.txt")

recognizer = sr.Recognizer()
with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic)        # learn the background noise level
    print("Speak... (say 'stop' to finish)")
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

print("Your notes are in", NOTES)
