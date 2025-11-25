# Real-Time Drowsiness Detection Using Eye Aspect Ratio (EAR) and MediaPipe

Sistem deteksi kantuk real-time berbasis kamera yang menggunakan **MediaPipe Face Mesh**, **Eye Aspect Ratio (EAR)**, dan **OpenCV** untuk mendeteksi kondisi mata tertutup terlalu lama.  
Ketika kantuk terdeteksi, sistem akan memicu **alarm suara otomatis** menggunakan *simpleaudio*.

---

## ✨ Fitur Utama
- Deteksi wajah dan landmark mata menggunakan **MediaPipe Face Mesh**
- Perhitungan **EAR (Eye Aspect Ratio)** untuk menentukan keadaan mengantuk
- Real-time menggunakan kamera laptop atau kamera HP (DroidCam)
- Tidak membutuhkan dataset (tanpa training)
- Alarm otomatis ketika kantuk terdeteksi
- Ringan dan dapat berjalan di laptop berspesifikasi rendah

---

## 📌 Teknologi yang Digunakan
- Python 3.x  
- OpenCV  
- MediaPipe  
- NumPy  
- simpleaudio  

---

## 📁 Struktur Folder

Real-Time-Drowsiness-Detection/
│── venv/ → Virtual environment
│── drowsiness_detector.py → Program utama deteksi kantuk
│── alarm.wav → Suara alarm (dibuat otomatis jika belum ada)
│── README.md → Dokumentasi proyek

---

## 📦 Instalasi & Persiapan

### 1️⃣ Clone Repository
```bash
git clone https://github.com/USERNAME/Real-Time-Drowsiness-Detection.git
cd Real-Time-Drowsiness-Detection
```
### 2️⃣ Buat Virtual Environment
```bash
python -m venv venv
```
### 3️⃣ Aktifkan Virtual Environment
```bash
Windows
venv\Scripts\activate\

Mac / Linux
source venv/bin/activate
```
### 4️⃣ Install Dependensi
```bash
pip install opencv-python mediapipe numpy simpleaudio
```
### ▶️ Menjalankan Program
Pastikan kamera aktif, lalu jalankan:
```bash
python drowsiness_detector.py
```
Tekan Q untuk keluar dari program.

---

🧠 Cara Kerja Program

1.Kamera menangkap wajah pengguna

2.MediaPipe Face Mesh mendeteksi 468 titik landmark

3.Program mengambil 6 landmark khusus untuk mata kiri & kanan

4.EAR dihitung setiap frame

5.Jika EAR < threshold selama beberapa frame → dianggap mengantuk

6.Alarm berbunyi menggunakan simpleaudio

---

📸 Output Program

• Status yang tampil pada layar:

• NORMAL (EAR stabil di > 0.25)

• MENGANTUK! (EAR turun < 0.20 selama beberapa frame)

• EAR Value: 0.xxx

• Eye Closed Duration: x sec

---

🎧 Alarm

Program akan memutar file alarm.wav.
Jika tidak ada, sistem otomatis membuat suara alarm sederhana.

---

⚙️ Konfigurasi (Opsional)

Ubah parameter pada kode:
```bash
EAR_THRESHOLD = 0.21     # Ambang batas mata tertutup
CONSEC_FRAMES = 25       # Jumlah frame berturut-turut untuk dianggap kantuk
```

---

📝 Lisensi

Proyek ini bebas digunakan untuk tugas kuliah, penelitian, maupun pengembangan lebih lanjut.

---

👨‍💻 Pembuat

Agustian Putra
Machine Learning Course Project — 2025

---
