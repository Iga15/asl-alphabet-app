"""
ASL Alphabet Recognition App
----------------------------
Main application entry point for the PyQt-based ASL Alphabet Recognition tool.
Switches between home, camera, and dictionary interfaces.
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from home_page import HomePage
from camera_page import CameraPage
from dictionary_dialog import DictionaryDialog

class ASLRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ASL Alphabet Recognition')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage(self)
        self.stacked_widget.addWidget(self.home_page)

        self.camera_page = CameraPage(self)
        self.stacked_widget.addWidget(self.camera_page)

        self.home_page.dictionary_button.clicked.connect(self.open_dictionary)
        self.home_page.learning_button.clicked.connect(self.start_learning)
        self.home_page.recognition_button.clicked.connect(self.start_recognition)

    def open_dictionary(self):
        self.dictionary_dialog = DictionaryDialog(self)
        self.dictionary_dialog.show()

    def start_learning(self):
        self.camera_page.start_learning()
        self.stacked_widget.setCurrentWidget(self.camera_page)

    def start_recognition(self):
        self.camera_page.start_recognition()
        self.stacked_widget.setCurrentWidget(self.camera_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ASLRecognitionApp()
    window.show()
    sys.exit(app.exec_())
