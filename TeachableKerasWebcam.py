"""
TeachableKerasWebcam.py
-----------------------
Use a model trained with Google TEACHABLE MACHINE to recognise hand signs live
from your webcam.

The model (Model/keras_model.h5) was trained on 4 classes (Model/labels.txt):
    0 Handsok   1 HandRight   2 HandLeft   3 HandUp

Want your own model? Go to https://teachablemachine.withgoogle.com ,
train an Image project, export it as "Tensorflow -> Keras", and replace the
two files in the Model/ folder.

Run:  python TeachableKerasWebcam.py   (press 'q' to quit)
"""

import cv2                                          # OpenCV: webcam + drawing text on images
import tensorflow as tf                             # TensorFlow: the machine learning library
import numpy as np                                  # NumPy: fast maths on arrays (images are arrays!)
from tensorflow.keras.models import load_model      # function to load a saved Keras model
from tensorflow.keras.layers import DepthwiseConv2D  # a layer type used inside the model

# ---------- 1. Load the class names ----------
try:
    with open('Model/labels.txt', 'r') as f:  # open the file in read mode ('r')
        # Read every line and remove spaces/newlines -> ['0 Handsok', '1 HandRight', ...]
        labels = [line.strip() for line in f.readlines()]
    print("Labels loaded successfully:", labels)
except Exception as e:
    # If the file is missing, explain the problem and stop
    print(f"Error loading labels: {e}")
    exit(1)


# ---------- 2. Fix a compatibility problem ----------
# Teachable Machine saves an extra 'groups' setting that newer Keras versions
# don't accept. We create our own version of the layer that simply removes it.
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, **kwargs):
        kwargs.pop('groups', None)  # Remove 'groups' if present
        super().__init__(**kwargs)  # then build the normal layer


# ---------- 3. Load the trained model ----------
try:
    # custom_objects tells Keras: "when you see DepthwiseConv2D, use our fixed version"
    model = load_model('Model/keras_model.h5', custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D})
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)


def preprocess_frame(frame):
    """Prepare a webcam image so it looks exactly like the images the model was trained on."""
    # Resize the frame to match the model's expected input size (224x224 pixels)
    resized_frame = cv2.resize(frame, (224, 224))
    # Convert the image to an array of decimal numbers (float32)
    img_array = np.array(resized_frame, dtype=np.float32)
    # Models work on BATCHES of images -> add a batch dimension: (224,224,3) -> (1,224,224,3)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the pixel values from 0-255 to 0-1
    img_array /= 255.0
    return img_array


# ---------- 4. Open the webcam ----------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit(1)

print("Press 'q' to quit the webcam feed.")

# ---------- 5. Main loop: predict on every frame ----------
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to capture a frame from the webcam.")
        break

    # Preprocess the frame for prediction
    processed_frame = preprocess_frame(frame)

    try:
        # predict() returns one probability per class, e.g. [[0.05, 0.90, 0.03, 0.02]]
        predictions = model.predict(processed_frame)
        # argmax = position of the highest probability = the class the model believes in
        predicted_class = np.argmax(predictions[0])
        # Convert the class number into its name
        predicted_label = labels[predicted_class]
    except Exception as e:
        print(f"Prediction error: {e}")
        break

    # Build the text, e.g. "Predicted: 1 HandRight (0.90)"  (:.2f = 2 decimals)
    label = f"Predicted: {predicted_label} ({predictions[0][predicted_class]:.2f})"
    # Write the text on the image: position (10,30), font, size 1, green (B,G,R), thickness 2
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the annotated frame
    cv2.imshow("Webcam Feed with Prediction", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
