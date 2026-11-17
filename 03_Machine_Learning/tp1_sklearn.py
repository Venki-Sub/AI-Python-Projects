"""
MLclassic/tp1_sklearn.py
------------------------
TP1 - Your first "classic" machine learning model with scikit-learn.

Goal: recognise the SPECIES of an iris flower from 4 measurements:
    sepal length, sepal width, petal length, petal width (in cm)
The 3 possible species (classes) are: 0 = setosa, 1 = versicolor, 2 = virginica.

Steps:
  1. Load the Iris dataset (150 flowers, built into scikit-learn)
  2. Split it into training data (80%) and test data (20%)
  3. Train a Random Forest (= many decision trees that vote together)
  4. Measure how good it is: classification report + confusion matrix

Run:  python MLclassic/tp1_sklearn.py
"""

from sklearn.datasets import load_iris                    # a small, famous dataset of flowers
from sklearn.model_selection import train_test_split      # splits data into train / test
from sklearn.ensemble import RandomForestClassifier       # the model: a forest of decision trees
# Other models to try (uncomment the import AND the matching "clf = ..." line in step 3):
# from sklearn.linear_model import LogisticRegression     # draws straight lines between classes
# from sklearn.neighbors import KNeighborsClassifier      # copies the species of the closest flowers
# from sklearn.svm import SVC                             # Support Vector Machine: widest margin between classes
# from sklearn.tree import DecisionTreeClassifier         # ONE decision tree (a forest has many)
# from sklearn.naive_bayes import GaussianNB              # probabilities, very fast
# from sklearn.ensemble import GradientBoostingClassifier # trees built one by one, each fixing the last one's mistakes
# from sklearn.neural_network import MLPClassifier        # a small neural network
from sklearn.metrics import classification_report, ConfusionMatrixDisplay  # tools to evaluate the model
import matplotlib.pyplot as plt                           # draws charts (needed to show the confusion matrix)

# ---------- 1. Load the data ----------
# return_X_y=True gives us two things directly:
#   X -> the inputs: a table of 150 rows (flowers) x 4 columns (measurements)
#   y -> the answers: the species number (0, 1 or 2) of each flower
X, y = load_iris(return_X_y=True)

# ---------- 2. Split into train and test ----------
# The model learns on the TRAIN part and we check it on the TEST part
# (flowers it has never seen -> an honest score).
#   test_size=0.2   -> 20% of the flowers (30) go to the test set
#   stratify=y      -> keep the same proportion of each species in train and test
#   random_state=42 -> the "random" split is the same every time you run the script
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

# ---------- 3. Create and train the model ----------
# n_estimators=100 -> the forest contains 100 decision trees; the final answer is their majority vote
# random_state=42  -> same trees every run, so everyone in class gets the same result
clf = RandomForestClassifier(n_estimators=100, random_state=42)
# Swap the model: comment out the line above and uncomment ONE line below (+ its import at the top).
# Everything else stays the same, because every scikit-learn model has fit() and predict().
# clf = LogisticRegression(max_iter=1000)                          # max_iter=1000 avoids a "did not converge" warning
# clf = KNeighborsClassifier(n_neighbors=5)                        # try 3, 7, 15... and watch the F1 change
# clf = SVC(kernel="rbf", C=1.0)                                   # also try kernel="linear"
# clf = DecisionTreeClassifier(max_depth=3, random_state=42)       # max_depth limits how deep the tree grows
# clf = GaussianNB()                                               # no settings needed
# clf = GradientBoostingClassifier(n_estimators=100, random_state=42)
# clf = MLPClassifier(hidden_layer_sizes=(16,), max_iter=2000, random_state=42)
clf.fit(X_tr, y_tr)  # fit() = training: the model learns the link between measurements and species

# ---------- 4. Evaluate the model ----------
# clf.predict(X_te) -> the model guesses the species of each test flower
# classification_report compares the guesses with the true answers (y_te) and prints, per species:
#   precision -> when the model says "setosa", how often is it right?
#   recall    -> of all real setosas, how many did the model find?
#   f1-score  -> a mix of precision and recall (1.0 = perfect)
#   support   -> how many test flowers of that species there are
print(classification_report(y_te, clf.predict(X_te)))

# Confusion matrix: a grid of true species (rows) vs predicted species (columns).
# Numbers on the diagonal = correct answers; anything outside the diagonal = mistakes.
ConfusionMatrixDisplay.from_estimator(clf, X_te, y_te)
plt.show()  # open the chart window (without this, nothing appears when run as a script)
