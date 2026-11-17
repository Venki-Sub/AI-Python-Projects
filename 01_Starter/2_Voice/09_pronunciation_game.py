"""
09 - English pronunciation game
-------------------------------
The program shows an English word. Say it out loud!
If Google understands the right word, you score a point.
It's a fun way to see how speech recognition "hears" you.

Run:  python 09_pronunciation_game.py
Try:  add harder words to the list ("squirrel", "thoroughly"...)
"""

import random
import speech_recognition as sr

WORDS = ["apple", "computer", "beautiful", "weather", "chocolate", "thirty", "orange", "water"]
ROUNDS = 5

recognizer = sr.Recognizer()
score = 0

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

print(f"\nFinal score: {score}/{ROUNDS}")
