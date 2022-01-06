import os
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
import cv2
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(7, activation="softmax"))

model.load_weights(os.path.join(os.path.dirname(__file__), "../../model.h5"))


def detectEmotion(np_picture):
    # FIXME: verify if the max % is bigger than a certain threshold
    from app.utils import Mood

    facecasc = cv2.CascadeClassifier(
        os.path.join(
            os.path.dirname(__file__), "../../haarcascade_frontalface_default.xml"
        )
    )
    # facecasc = cv2.CascadeClassifier("../../haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(np_picture, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    (x, y, w, h) = faces[0]
    roi_gray = gray[y : y + h, x : x + w]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
    prediction = model.predict(cropped_img)
    maxindex = int(np.argmax(prediction))
    return Mood(maxindex)
