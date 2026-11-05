"""
CampusBot/app.py
----------------
The same CampusBot, but as a WEB PAGE with a chat interface, built with Streamlit.
The answer appears word by word ("streaming"), like ChatGPT.

Before running:
    1. Install Ollama (https://ollama.com) and run:  ollama pull llama3.2:3b
    2. pip install streamlit ollama

Run:  streamlit run app.py   (it opens http://localhost:8501 in your browser)
"""

import ollama            # talk to the local Ollama AI model
import streamlit as st   # builds the web app/page with pure Python

MODEL = "llama3.2:3b"
# system prompt to set the behavior of the bot
# (French: "You are CampusBot, assistant of École Schulz in Geneva. Answer in French, short and clear.")
SYSTEM = "Tu es CampusBot, assistant de l'École Schulz à Genève. Réponds en français, court et clair."

# initialisation de la page web with title and icon (tab title + emoji favicon)
st.set_page_config(page_title="CampusBot", page_icon="🎓")
st.title("🎓 CampusBot")  # big title at the top of the page

# initialise la mémoire du bot  (= initialise the bot's memory)
# IMPORTANT: Streamlit re-runs this whole script after EVERY click or message.
# st.session_state is a special dictionary that survives those re-runs.
# If the user has not yet asked a question, we initialise the memory with the system prompt.
if "messages" not in st.session_state:          # mémoire entre les clics (memory between clicks)
    st.session_state.messages = [{"role": "system", "content": SYSTEM}]

# affiche l'historique des messages dans le chat  (= show the chat history)
for m in st.session_state.messages:             # réaffiche l'historique (re-display history)
    if m["role"] != "system":                   # never show the hidden system prompt
        st.chat_message(m["role"]).write(m["content"])  # a chat bubble for user or assistant

# traitement de la question posée par l'utilisateur  (= handle the user's question)
# ':=' (walrus operator) stores the input in 'question' AND checks it is not empty
if question := st.chat_input("Posez votre question…"):   # "Ask your question…"
    st.session_state.messages.append({"role": "user", "content": question})  # save to memory
    st.chat_message("user").write(question)                                  # show user bubble

    with st.chat_message("assistant"):   # everything inside appears in the bot's bubble
        # stream=True -> the model sends the answer in small pieces (chunks)
        flux = ollama.chat(model=MODEL, messages=st.session_state.messages, stream=True)
        # write_stream shows each piece as it arrives and returns the full text at the end
        texte = st.write_stream(c["message"]["content"] for c in flux)

    st.session_state.messages.append({"role": "assistant", "content": texte})  # save the answer

# the full cycle of the chatbot in Streamlit
# 1. you type a question in the input box and hit enter
# 2. the question is added to the memory of the bot
# 3. the question is sent to the model and the answer is retrieved
# 4. the answer is displayed in the chat interface
# 5. the answer is added to the memory of the bot
# 6. the cycle repeats for the next question
# 7. the memory is reset when the app is restarted
# the memory of the bot is stored in the session state
