import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from pathlib import Path

WEIGHTS_PATH = Path(__file__).resolve().parent.parent / "models" / "asl_recognition_model.h5"
model = tf.keras.models.load_model(str(WEIGHTS_PATH))

mp_hands = mp.solutions.hands
hands_processor = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def extract_landmarks(frame):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands_processor.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = [landmark for landmark in hand_landmarks.landmark]
            landmarks_flat = [item for landmark in landmarks for item in (landmark.x, landmark.y, landmark.z)]
            return landmarks_flat
    return None

def predict_gesture(landmarks_flat):
    if landmarks_flat is not None:
        landmarks_array = np.array(landmarks_flat).reshape(1, -1)
        prediction = model.predict(landmarks_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        gesture_name_mapping = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        return gesture_name_mapping[predicted_class]
    return None

def get_bounding_box(landmarks_flat, width, height):
    if landmarks_flat:
        x_coordinates = [int(landmark_x * width) for landmark_x in landmarks_flat[0::3]]
        y_coordinates = [int(landmark_y * height) for landmark_y in landmarks_flat[1::3]]
        return (min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))
    return None, None
