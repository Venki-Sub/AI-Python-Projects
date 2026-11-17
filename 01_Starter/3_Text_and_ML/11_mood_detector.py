"""
11 - Mood detector (sentiment analysis)
---------------------------------------
Same idea as the spam detector, but the model guesses if a sentence is
HAPPY or SAD - and how SURE it is (a probability).

Run:  python 11_mood_detector.py      (press Enter on an empty line to quit)
Try:  "je suis super content", "quelle journée horrible"... What about "pas mal" ? Why is it hard?
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

happy = ["je suis content", "super journée", "j'adore ce film", "c'est génial", "trop bien",
         "je suis heureux", "merci beaucoup c'est parfait", "quelle belle surprise"]
sad = ["je suis triste", "journée horrible", "je déteste ça", "c'est nul", "trop dommage",
       "je suis fatigué et déçu", "rien ne marche", "quelle mauvaise nouvelle"]

texts = happy + sad                                          # all sentences in one list
labels = ["😀 happy"] * len(happy) + ["😢 sad"] * len(sad)   # the matching answers

vectorizer = CountVectorizer()
model = MultinomialNB().fit(vectorizer.fit_transform(texts), labels)

while True:
    sentence = input("\nHow do you feel? ")
    if sentence == "":
        break
    X = vectorizer.transform([sentence])
    mood = model.predict(X)[0]
    confidence = model.predict_proba(X).max()        # probability of the chosen answer (0 to 1)
    print(f"-> {mood}  (sure at {confidence:.0%})")  # :.0% shows 0.87 as 87%
