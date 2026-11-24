"""
06 - The talking computer
-------------------------
Type a sentence: the computer reads it out loud (text-to-speech).

Uses the "say" command built into macOS.
Windows: pip install pyttsx3, then replace the subprocess line with:
    import pyttsx3; engine = pyttsx3.init(); engine.say(text); engine.runAndWait()

Run:  python 06_talking_computer.py      (type q, or press Enter on an empty line, to quit)
Try:  change the voice! List them with:  say -v "?"   (e.g. "Amélie", "Jacques", "Samantha")
"""

import subprocess  # lets Python run a terminal command

VOICE = "Thomas"   # a French voice installed on macOS

while True:
    text = input("What should I say? ")
    if text.strip().lower() in ("", "q"):   # empty line or q -> stop
        break
    # Same as typing  say -v Thomas "your text"  in the terminal
    subprocess.run(["say", "-v", VOICE, text])
