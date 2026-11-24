# 😴 Real-Time Drowsiness Detection (EAR + MediaPipe)

A real-time camera-based drowsiness detection system using **MediaPipe Face Mesh**, **Eye Aspect Ratio (EAR)**, and **OpenCV**. Automatically triggers an audio alarm when prolonged eye closure is detected.

![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

---

## ✨ Features

- Real-time face & eye landmark detection via **MediaPipe Face Mesh** (468 landmarks)
- **EAR (Eye Aspect Ratio)** calculation to detect drowsy state
- Works with laptop webcam or phone camera (DroidCam)
- **No dataset or model training required**
- Automatic audio alarm when drowsiness is detected
- Lightweight — runs on low-spec laptops

---

## 🔌 Tech Stack

| Library | Purpose |
|---------|---------|
| Python 3.x | Core language |
| OpenCV | Camera capture & frame rendering |
| MediaPipe | Face mesh landmark detection |
| NumPy | EAR computation |
| simpleaudio | Audio alarm playback |

---

## 📁 Project Structure

```
Real-Time-Drowsiness-Detection/
├── drowsiness_detector.py   # Main detection script
├── alarm.wav                # Alarm audio (auto-generated if missing)
└── README.md
```

---

## ⚙️ How It Works

```
Camera Frame
     ↓
MediaPipe Face Mesh (468 landmarks)
     ↓
Extract 6 eye landmarks (left & right)
     ↓
Calculate EAR per frame
     ↓
EAR < threshold for N consecutive frames?
     ↓ Yes
Trigger alarm (simpleaudio)
```

**EAR Formula:**

$$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2 \cdot ||p_1 - p_4||}$$

When EAR drops below `0.21` for `25+` consecutive frames → **drowsiness detected**.

---

## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/PutYourBae/Real-Time-Drowsiness-Detection-Using-EAR-and-OpenCV.git
cd Real-Time-Drowsiness-Detection-Using-EAR-and-OpenCV
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install opencv-python mediapipe numpy simpleaudio
```

---

## ▶️ Run

Make sure your camera is active, then:

```bash
python drowsiness_detector.py
```

Press **Q** to quit.

---

## 📸 Output

The program overlays real-time status on the camera feed:

| Status | Condition |
|--------|-----------|
| **NORMAL** | EAR stable above 0.25 |
| **DROWSY!** 🚨 | EAR below 0.20 for several frames |

Additional info displayed: `EAR Value: 0.xxx` and `Eye Closed Duration: x sec`

---

## ⚙️ Configuration (Optional)

Adjust thresholds directly in the script:

```python
EAR_THRESHOLD = 0.21   # Eye closure threshold
CONSEC_FRAMES = 25     # Consecutive frames to trigger alarm
```

---

## 🔊 Alarm

The program plays `alarm.wav`.  
If the file is missing, it automatically generates a simple beep tone.

---

## 📄 License

MIT License — free to use for academic, research, or personal projects.

---

## 👨‍💻 Author

**Agustian Putra**  
Machine Learning Course Project — 2025
