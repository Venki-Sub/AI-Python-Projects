"""
10 - Spam detector
------------------
A complete machine learning project in about 10 lines!
The model learns from a few example messages labelled "spam" or "ok",
then guesses the label of YOUR messages.

How it works:
  1. CountVectorizer turns each sentence into word counts ("gratuit": 1, "cours": 0...)
  2. Naive Bayes learns which words appear more often in spam

Run:  python 10_spam_detector.py      (press Enter on an empty line to quit)
Try:  "gagnez de l'argent", "le cours est demain"... then add YOUR examples to make it smarter!
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training data: examples + their correct answer (label)
texts = [
    "gagnez un iphone gratuit", "cliquez ici pour gagner", "argent facile offre gratuite",
    "vous avez gagné un cadeau", "promo exceptionnelle cliquez vite",
    "rendez-vous demain à 10h", "le cours de python est annulé", "tu viens manger ce soir ?",
    "n'oublie pas tes devoirs", "la réunion est à quelle heure ?",
]
labels = ["spam", "spam", "spam", "spam", "spam", "ok", "ok", "ok", "ok", "ok"]

vectorizer = CountVectorizer()                 # sentence -> word counts
X = vectorizer.fit_transform(texts)            # learn the vocabulary + transform the examples
model = MultinomialNB().fit(X, labels)         # train the model

while True:
    message = input("\nMessage: ")
    if message == "":
        break
    prediction = model.predict(vectorizer.transform([message]))[0]  # transform, then predict
    print("->", "🚫 SPAM" if prediction == "spam" else "✅ OK")
