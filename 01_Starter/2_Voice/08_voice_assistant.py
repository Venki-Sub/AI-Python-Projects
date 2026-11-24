"""
08 - Mini voice assistant
-------------------------
A tiny "Siri" that listens and answers OUT LOUD (in French).

Say a sentence containing:
    "heure"     -> tells the time
    "date"      -> tells today's date
    "youtube"   -> opens YouTube
    "blague"    -> tells a joke
    "au revoir" -> stops   (or type q + Enter in the terminal)

We check if a KEYWORD is IN the sentence, so "quelle heure est-il ?" and
"donne-moi l'heure" both work.

Run:  python 08_voice_assistant.py
Try:  add your own command (e.g. "météo" -> open a weather website)!
"""

import datetime
import random
import subprocess
import threading
import time
import webbrowser
import speech_recognition as sr

JOKES = [
    "Pourquoi les plongeurs plongent-ils en arrière ? Parce que sinon, ils tombent dans le bateau.",
    "Quel est le comble pour un électricien ? De ne pas être au courant.",
]


def speak(text):
    """Print the answer and read it out loud (macOS 'say' command)."""
    print("Assistant:", text)
    subprocess.run(["say", "-v", "Thomas", text])


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


def assistant():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        print("(Say 'au revoir' or type q + Enter to quit)")
        speak("Bonjour, je vous écoute")
        while True:
            try:
                sentence = recognizer.recognize_google(recognizer.listen(mic), language="fr-FR").lower()
            except sr.UnknownValueError:
                continue                                   # not understood -> listen again
            print("You:", sentence)

            now = datetime.datetime.now()
            if "heure" in sentence:
                speak(f"Il est {now.hour} heures {now.minute}")
            elif "date" in sentence:
                speak(f"Nous sommes le {now.day}/{now.month}/{now.year}")
            elif "youtube" in sentence:
                speak("J'ouvre YouTube")
                webbrowser.open("https://www.youtube.com")
            elif "blague" in sentence:
                speak(random.choice(JOKES))
            elif "au revoir" in sentence:
                speak("Au revoir !")
                break
            else:
                speak("Je n'ai pas compris")


run_until_q(assistant)
