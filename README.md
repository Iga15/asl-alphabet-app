## ASL Alphabet Recognition App

An interactive application that recognizes ASL (American Sign Language) alphabet letters in real time using a webcam feed.
Built with PyQt5, OpenCV, TensorFlow, and MediaPipe.

## 🎯 Overview
- Real-time ASL alphabet recognition using a trained neural network.
- Custom dataset collected with MediaPipe for accurate hand landmark tracking.
- Features a Learning Mode and Recognition Mode.
- Includes a built-in ASL Dictionary for visual reference.

## 🧠 Project Structure

```asl-alphabet-app/
│
├── app/                 # PyQt5 app code
│   ├── main.py
│   ├── camera_page.py
│   ├── home_page.py
│   ├── dictionary_dialog.py
│   ├── utils.py
│   └── images/          # UI + ASL sign images
│
├── notebooks/           # Jupyter notebooks (data collection + model training)
│   ├── get_training_data.ipynb
│   └── train_asl_model.ipynb
│
├── models/              # Trained .h5 models (not included)
│   └── README.md
│
├── configs/             # Paths and YAML configs
│
├── data/                # Dataset (not included)
│
├── runs/                # Outputs, logs, saved CSVs
│
├── requirements.txt
└── README.md
```

## ⚙️ How It Works
1. Data Collection:
- Uses get_training_data.ipynb to record custom ASL gesture data.
-	Captures 21 hand landmarks (x, y, z) using MediaPipe.

2. Model Training:
-	Neural network (Keras Sequential model).
-	Trains on custom dataset of labeled hand landmarks.

3. Application:
-	Real-time camera input analyzed by trained model.
-	Displays recognized letter on screen.
-	Learning mode asks users to sign random letters for practice.

## 🚀 Running the App
1.	Install dependencies:

  ```bash
pip install -r requirements.txt
```

2.	Run the application:

```bash
python app/main.py
```

## 📦 Requirements

- Python 3.10+
- PyQt5
- OpenCV
- MediaPipe
- TensorFlow
- NumPy
- Pandas

## 🖐️ Notes
- Datasets and trained models are excluded due to size.
- You can collect your own dataset using the included notebook.
