"""
IMDBmoviePrediction.py
----------------------
Machine learning on real data: train a NEURAL NETWORK on the IMDB movie
dataset (Model/imdb.csv) to predict if a movie will be "liked".

We say a movie is "liked" if its rating is above 7.0.
Steps:
  1. Load the CSV with pandas
  2. Clean the data (fill missing values)
  3. Split into training data and test data
  4. Turn text columns into numbers (one-hot encoding) and scale numbers
  5. Build and train a small neural network with TensorFlow/Keras
  6. Predict on one random movie the model has never seen

Note for students: 'rating' is used both as an input AND to create the label,
so the model can "cheat". Challenge: remove 'rating' from numeric_features
and see how the accuracy changes!

Run:  python IMDBmoviePrediction.py
"""

import pandas as pd                                            # pandas: read & manipulate tables (CSV)
from sklearn.model_selection import train_test_split           # split data into train / test
from sklearn.preprocessing import StandardScaler, OneHotEncoder  # scale numbers / encode categories
from sklearn.compose import ColumnTransformer                  # apply different transforms to different columns
import tensorflow as tf                                        # TensorFlow: neural networks
from tensorflow.keras import layers                            # building blocks of a neural network

# ---------- 1. Load dataset ----------
data = pd.read_csv('Model/imdb.csv')  # a DataFrame = a table with rows (movies) and columns

# ---------- 2. Choose the columns (features) ----------
# Categorical = text values (e.g. genre "Drama")
categorical_features = ['kind', 'genre', 'country', 'language', 'cast', 'director', 'composer', 'writer']
# Numeric = number values
numeric_features = ['year', 'rating', 'vote', 'runtime']

# ---------- Handle missing values (empty cells) ----------
for col in categorical_features:
    data[col].fillna('Unknown', inplace=True)           # empty text -> "Unknown"
for col in numeric_features:
    data[col].fillna(data[col].median(), inplace=True)  # empty number -> the median (middle value)

# Make sure every categorical value is a string (some may be read as numbers)
for col in categorical_features:
    data[col] = data[col].astype(str)

# ---------- Create the label (what we want to predict) ----------
# True/False (rating > 7) converted to 1/0
data['liked'] = (data['rating'] > 7.0).astype(int)

# Features (inputs X) and labels (answers y)
features = data[['title'] + categorical_features + numeric_features]  # Include 'title' for reference
labels = data['liked']

# ---------- 3. Train-test split ----------
# 80% of movies to train, 20% to test. random_state=42 -> same split every run
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# The title is not useful for learning -> remove it from the training inputs
X_train_no_title = X_train.drop(columns=['title'])
X_test_no_title = X_test.drop(columns=['title'])

# ---------- 4. Preprocessing pipeline ----------
# Neural networks only understand numbers, so:
#   - StandardScaler: puts numbers on the same scale (mean 0, std 1)
#   - OneHotEncoder: turns each category into 0/1 columns (genre_Drama=1, genre_Comedy=0, ...)
#     handle_unknown='ignore' -> new categories in the test set won't crash the program
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# fit_transform on TRAIN data (learn the scaling/categories), only transform on TEST data
X_train_transformed = preprocessor.fit_transform(X_train_no_title)
X_test_transformed = preprocessor.transform(X_test_no_title)

# ---------- 5. Neural network ----------
model = tf.keras.Sequential([                                  # layers stacked one after another
    layers.Input(shape=(X_train_transformed.shape[1],)),       # input size = number of columns
    layers.Dense(64, activation='relu'),                       # hidden layer with 64 neurons
    layers.Dense(32, activation='relu'),                       # hidden layer with 32 neurons
    layers.Dense(1, activation='sigmoid')                      # output: 1 number between 0 and 1
])
# adam = optimizer (how weights are updated), binary_crossentropy = loss for yes/no problems
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model: 10 passes (epochs) over the data, 32 movies at a time,
# keeping 20% of the training data aside to check progress (validation)
model.fit(X_train_transformed, y_train, epochs=10, batch_size=32, validation_split=0.2)

# ---------- 6. Random movie prediction ----------
random_movie = X_test.sample(1)                                  # pick 1 random movie from the test set
random_movie_no_title = random_movie.drop(columns=['title'])     # remove 'title' for prediction
random_movie_transformed = preprocessor.transform(random_movie_no_title)  # same preprocessing as training
prediction = model.predict(random_movie_transformed)             # e.g. [[0.83]]
predicted_like = prediction[0][0] > 0.5                          # above 0.5 -> "liked"

# Print the result
print("Random Movie Features:")
print(f"Title: {random_movie['title'].iloc[0]}")
for col in random_movie.columns:            # print every feature of the movie
    if col != 'title':
        print(f"{col}: {random_movie.iloc[0][col]}")
if predicted_like:
    print("Prediction: Likely to like the movie.")
else:
    print("Prediction: Unlikely to like the movie.")
