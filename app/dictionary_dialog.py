from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path

class DictionaryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('ASL Dictionary')
        self.setGeometry(150, 150, 600, 600)
        self.setMinimumSize(10, 10) 

        self.layout = QVBoxLayout(self)

        self.images_dir = Path(__file__).resolve().parent / "images"

        self.dictionary = [
            {"letter": ch, "image_path": self.images_dir / f"sign_{ch.lower()}.png"}
    for ch in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        ]
        self.current_index = 0

        self.letter_label = QLabel(self)
        self.letter_label.setAlignment(Qt.AlignCenter)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.letter_label)
        self.layout.addWidget(self.image_label)

        navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.show_prev)
        navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.show_next)
        navigation_layout.addWidget(self.next_button)

        self.layout.addLayout(navigation_layout)

        self.show_letter()

    def show_letter(self):
        entry = self.dictionary[self.current_index]
        self.letter_label.setText(entry["letter"])

        img_path = entry["image_path"]
        if img_path.exists():
            pixmap = QPixmap(str(img_path))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(int(pixmap.width() * 0.75), int(pixmap.height() * 0.75), Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText(f"(could not load image)")
        else:
            self.image_label.setText(f"(missing: {img_path.name})")
        

        
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.dictionary) - 1)

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_letter()

    def show_next(self):
        if self.current_index < len(self.dictionary) - 1:
            self.current_index += 1
            self.show_letter()
