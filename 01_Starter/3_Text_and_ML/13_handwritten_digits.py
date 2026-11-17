"""
13 - Handwritten digit recognition
----------------------------------
scikit-learn includes 1,797 tiny images (8x8 pixels) of handwritten digits 0-9.
We train a model on most of them, then test it on images it has never seen.

Run:  python 13_handwritten_digits.py
Try:  replace KNeighborsClassifier() by SVC() (from sklearn.svm import SVC). Better or worse?
"""

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

digits = load_digits()                                        # images + correct answers
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=0)

model = KNeighborsClassifier().fit(X_train, y_train)          # train
print(f"Accuracy on {len(X_test)} new images: {model.score(X_test, y_test):.1%}")

# Show the first 10 test images with the model's guess
predictions = model.predict(X_test[:10])
fig, axes = plt.subplots(1, 10, figsize=(12, 2))
for ax, image, guess in zip(axes, X_test[:10], predictions):
    ax.imshow(image.reshape(8, 8), cmap="gray_r")             # 64 numbers -> 8x8 picture
    ax.set_title(f"guess: {guess}")
    ax.axis("off")
plt.show()
