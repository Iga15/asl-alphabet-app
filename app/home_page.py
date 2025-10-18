from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel(self)
        image_path = Path(__file__).resolve().parent / "images" / "home.png"
        self.logo_pixmap = QPixmap(str(image_path))
        self.logo_label.setPixmap(self.logo_pixmap)
        self.layout.addWidget(self.logo_label)

        self.dictionary_button = QPushButton('ASL Dictionary', self)
        self.layout.addWidget(self.dictionary_button)

        self.learning_button = QPushButton('Learning Mode', self)
        self.layout.addWidget(self.learning_button)

        self.recognition_button = QPushButton('Recognition Mode', self)
        self.layout.addWidget(self.recognition_button)
