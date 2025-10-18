import random
import string
import cv2
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from utils import extract_landmarks, predict_gesture

class CameraPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.last_recognized_letter = None
        self.random_letter = ''
        self.in_learning_mode = False
        self.letter_start_time = QTime()
        self.letter_start_time.start()
        self.accumulated_text = ''
        self.recognition_threshold = 2000  # 2 seconds

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
        self.gesture_stable = False

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.camera_label = QLabel(self)
        self.layout.addWidget(self.camera_label)

        self.text_label = QLabel('SIGN: ', self)
        self.layout.addWidget(self.text_label)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_text)
        self.layout.addWidget(self.clear_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.clear_button.setVisible(False)

    def start_learning(self):
        self.in_learning_mode = True
        self.random_letter = random.choice(string.ascii_uppercase)
        self.update_label_text(f'SIGN: {self.random_letter}')
        self.letter_start_time.restart()
        self.clear_button.setVisible(False)

    def update_label_text(self, text):
        self.text_label.setText(text)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_image.shape
            step = channel * width
            qImg = QImage(rgb_image.data, width, height, step, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qImg))

            landmarks_flat = extract_landmarks(frame)
            gesture_prediction = predict_gesture(landmarks_flat)

            if gesture_prediction:
                if self.in_learning_mode:
                    if gesture_prediction == self.random_letter:
                        if self.letter_start_time.elapsed() >= 1000:  # 1 second
                            self.update_label_text('GREAT')
                            QTimer.singleShot(2000, self.reset_learning)
                    else:
                        self.letter_start_time.restart()
                else:
                    self.process_recognition_mode(gesture_prediction)

    def reset_learning(self):
        self.random_letter = random.choice(string.ascii_uppercase)
        self.update_label_text(f'SIGN: {self.random_letter}')
        self.letter_start_time.restart()

    def clear_text(self):
        self.accumulated_text = ''
        self.text_label.setText('Recognized Text: ')

    def go_back(self):
        self.in_learning_mode = False
        self.clear_button.setVisible(True)
        self.parent.stacked_widget.setCurrentWidget(self.parent.home_page)

    def start_recognition(self):
        self.in_learning_mode = False
        self.clear_button.setVisible(True)
        self.accumulated_text = ''
        self.text_label.setText('Recognized Text: ')
        self.last_recognized_letter = None
        self.letter_start_time.restart()

    def process_recognition_mode(self, gesture_prediction):
        if gesture_prediction != self.last_recognized_letter:
            self.last_recognized_letter = gesture_prediction
            self.letter_start_time.restart()
            self.gesture_stable = False
        elif self.letter_start_time.elapsed() >= self.recognition_threshold and not self.gesture_stable:
            self.accumulated_text += gesture_prediction + ' '
            self.text_label.setText(f'Recognized Text: {self.accumulated_text}')
            self.gesture_stable = True

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        super().closeEvent(event)

