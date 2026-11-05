"""
CampusBot/chat.py
-----------------
A chatbot in the TERMINAL, powered by a local AI model (Llama 3.2) via Ollama.
No internet and no API key needed once the model is downloaded.

Before running:
    1. Install Ollama: https://ollama.com
    2. Download the model:  ollama pull llama3.2:3b

Run:  python chat.py   (type q, quit or exit to leave)
"""

import ollama  # Python library to talk to the Ollama app running on your computer

MODEL = "llama3.2:3b"  # which AI model to use (3b = 3 billion parameters, small & fast)
# The SYSTEM prompt gives the bot its personality and rules.
# (French: "You are CampusBot, assistant of École Schulz in Geneva. Answer in French, short and clear.")
SYSTEM = "Tu es CampusBot, assistant de l'École Schulz à Genève. Réponds en français, court et clair."

# The conversation history = the bot's memory ("la mémoire du bot").
# Each message is a dictionary with a role ("system", "user" or "assistant") and its content.
messages = [{"role": "system", "content": SYSTEM}]

while True:
    question = input("Vous : ")  # "Vous" = "You": wait for the user to type a question
    if question.strip().lower() in ("q", "quit", "exit"):  # exit the loop if the user types 'q', 'quit', or 'exit'
        break
    # Add the user's question to the memory ("on ajoute la question ... à la mémoire du bot")
    messages.append({"role": "user", "content": question})

    # Send the WHOLE conversation to the model and get the answer back
    rep = ollama.chat(model=MODEL, messages=messages)
    texte = rep["message"]["content"]  # extract just the text of the answer

    # Keep the answer in memory too, so the bot remembers what it said ("on garde la réponse")
    messages.append({"role": "assistant", "content": texte})
    print("CampusBot :", texte)



# the full cycle of the chatbot in terminal
# 1. you type a question in the input box and hit enter
# 2. the question is added to the memory of the bot
# 3. the question is sent to the model and the answer is retrieved
# 4. the answer is displayed in the terminal
# 5. the answer is added to the memory of the bot
# 6. the cycle repeats for the next question
# 7. the memory is reset when the app is restarted
# the memory of the bot is stored in the messages list
