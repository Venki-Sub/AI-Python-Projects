"""
15 - AI quiz maker
------------------
Paste any text (a lesson, a Wikipedia paragraph...) and a local AI model
writes 3 quiz questions about it.

Needs Ollama (free, runs on your computer, no internet needed):
    1. Install it from https://ollama.com
    2. In a terminal:  ollama pull llama3.2:3b

Run:  python 15_quiz_maker.py
Try:  change the PROMPT: ask for true/false questions, or answers in English.
"""

import ollama

MODEL = "llama3.2:3b"

text = input("Paste your text, then press Enter:\n")

# The prompt = the instruction we give to the AI
prompt = f"""Écris 3 questions de quiz à choix multiples (A, B, C) sur ce texte,
avec la bonne réponse après chaque question. Texte :
{text}"""

print("\nThinking...\n")
answer = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
print(answer["message"]["content"])
