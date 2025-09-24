import numpy as np
import mediapipe as mp
import cv2
import tensorflow as tf
import csv
import os

class GestureDetector:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        model_path = os.path.join(base_path, 'keypoint_classifier.tflite')
        label_path = os.path.join(base_path, 'keypoint_classifier_label.csv')

        # Cargar modelo TFLite SIN delegados (solo CPU)
        self.interpreter = tf.lite.Interpreter(model_path=model_path, experimental_delegates=[])
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Cargar etiquetas
        with open(label_path, encoding='utf-8-sig') as f:
            self.labels = [row[0] for row in csv.reader(f)]

        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5
        )

    def process_image(self, img):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return None, "No se detectó una mano."

        hand_landmarks = results.multi_hand_landmarks[0]
        landmark_array = self._landmarks_to_np(hand_landmarks)

        # Normalizar puntos
        normalized_landmarks = self._preprocess_landmarks(landmark_array)

        input_data = np.array([normalized_landmarks], dtype=np.float32)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        gesture_id = np.argmax(output_data)

        return {
            "gesture_id": gesture_id,
            "gesture_name": self.labels[gesture_id],
            "probabilities": output_data.tolist()
        }, None

    def _landmarks_to_np(self, landmarks):
        return np.array([[lm.x, lm.y] for lm in landmarks.landmark])

    def _preprocess_landmarks(self, landmarks):
        base_x, base_y = landmarks[0]
        landmarks = landmarks - [base_x, base_y]
        flat = landmarks.flatten()
        max_value = np.max(np.abs(flat))
        return flat / max_value if max_value != 0 else flat
