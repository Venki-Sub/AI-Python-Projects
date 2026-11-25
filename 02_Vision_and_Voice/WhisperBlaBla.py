"""
WhisperBlaBla.py
----------------
Talk into your microphone and Whisper writes what you say, 100 % offline.

How it works:
  1. The microphone listens. When you PAUSE (stop talking ~1 second),
     the sentence you just said is cut out as one piece of audio.
  2. That piece is put in a queue (a waiting line).
  3. A second thread takes pieces from the queue and gives them to Whisper,
     which turns the audio into text and prints it.
  Thanks to the 2 threads, you can keep talking while Whisper is still writing.

Uses faster-whisper, a fast version of OpenAI's Whisper speech-to-text model.
The model is downloaded the first time you run it, then everything stays local.

Install:  pip install faster-whisper SpeechRecognition PyAudio
Run:      python WhisperBlaBla.py                 (live microphone, type q + Enter to quit)
          python WhisperBlaBla.py my_audio.wav    (transcribe a file instead)
"""

import os                                  # os: force the program to stop (os._exit)
import sys                                 # sys: read the file name from the command line
import queue                               # queue: a safe "waiting line" between threads
import threading                           # threading: run code in parallel
import numpy as np                         # numpy: turn raw audio bytes into numbers
import speech_recognition as sr            # SpeechRecognition: microphone + cut on pauses
from faster_whisper import WhisperModel    # faster-whisper: offline speech-to-text

LANGUAGE = "fr"  # the language you speak ("en" for English, None to auto-detect)

# Téléchargé au 1er lancement, puis 100 % local
# "small" = good balance of speed and accuracy ("tiny", "base", "medium", "large-v3" also exist)
# int8 = lighter maths so it runs fast on a normal CPU
print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")


# ---------- Mode 1: a file was given -> transcribe it and stop ----------
if len(sys.argv) > 1:
    segments, info = model.transcribe(sys.argv[1], language=LANGUAGE)
    print("Langue :", info.language)
    # Each segment = a piece of speech with its start and end time (in seconds)
    for seg in segments:
        print(f"[{seg.start:5.1f}s -> {seg.end:5.1f}s] {seg.text}")
    sys.exit()


# ---------- Mode 2: live microphone ----------
audio_queue = queue.Queue()  # sentences waiting to be transcribed


def transcribe_worker():
    """Runs in its own thread: take audio from the queue -> Whisper -> print text."""
    while True:
        audio = audio_queue.get()  # waits here until a sentence arrives
        # Whisper wants: 16 000 samples per second, numbers between -1 and 1
        raw = audio.get_raw_data(convert_rate=16000, convert_width=2)  # 16-bit bytes
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        # vad_filter=True skips parts with no voice (avoids writing nonsense on noise)
        segments, _ = model.transcribe(samples, language=LANGUAGE, vad_filter=True)
        text = "".join(seg.text for seg in segments).strip()
        if text:
            print(">>", text)


# daemon=True -> this thread stops automatically when the program ends
threading.Thread(target=transcribe_worker, daemon=True).start()

def listen_worker():
    """Runs in its own thread: microphone -> cut on pauses -> put in the queue."""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8  # seconds of silence that mean "end of sentence"
    with sr.Microphone(sample_rate=16000) as source:  # open the default microphone
        print("Calibrating to background noise, stay quiet...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Talk now! (type q + Enter to quit)\n")
        while True:
            # Records until you pause, then returns that piece of audio
            audio = recognizer.listen(source)
            audio_queue.put(audio)  # hand it to the Whisper thread, keep listening


threading.Thread(target=listen_worker, daemon=True).start()

# The main program just waits for you to type q (the 2 threads do the work)
try:
    while input().strip().lower() != "q":
        pass
except (KeyboardInterrupt, EOFError):  # Ctrl+C still works too
    pass
print("Bye!")
# os._exit = stop RIGHT NOW, even if Whisper is still busy writing a sentence
# (a normal exit can get stuck waiting for the microphone / Whisper threads)
os._exit(0)
