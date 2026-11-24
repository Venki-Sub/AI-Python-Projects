"""
09 - English pronunciation game
-------------------------------
The program shows an English word. Say it out loud!
If Google understands the right word, you score a point.
It's a fun way to see how speech recognition "hears" you.

Run:  python 09_pronunciation_game.py      (type q + Enter to quit early)
Try:  add harder words to the list ("squirrel", "thoroughly"...)
"""

import random
import threading
import time
import speech_recognition as sr

WORDS = ["apple", "computer", "beautiful", "weather", "chocolate", "thirty", "orange", "water"]
ROUNDS = 5

score = 0


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


def play():
    global score                      # play() changes the score defined outside
    recognizer = sr.Recognizer()

    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        for word in random.sample(WORDS, ROUNDS):       # pick 5 different words at random
            print(f"\nSay: {word.upper()}")
            try:
                heard = recognizer.recognize_google(recognizer.listen(mic, timeout=5), language="en-US").lower()
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                heard = "(nothing)"
            if word in heard:                           # the word appears in what Google heard
                score += 1
                print(f"Correct! Google heard: '{heard}'")
            else:
                print(f"Not quite... Google heard: '{heard}'")


run_until_q(play)
print(f"\nFinal score: {score}/{ROUNDS}")
