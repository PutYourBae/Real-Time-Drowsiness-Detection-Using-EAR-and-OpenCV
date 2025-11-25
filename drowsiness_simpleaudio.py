# drowsiness_simpleaudio.py
# Drowsiness detection (EAR) + simpleaudio alarm (file WAV) + Auto Screenshot
# Run: python drowsiness_simpleaudio.py

import os
import cv2
import mediapipe as mp
import numpy as np
import datetime
import threading

# Audio libs
import simpleaudio as sa   # expect installed
import pyttsx3              # expect installed

# ---------------- Config ----------------
CAMERA_SOURCE = 0            # 0=webcam laptop, ganti ke 1 jika DroidCam
EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES = 18      
ALARM_FILENAME = "alarm_pengguna_terdeteksi.wav"
LOG_DETECTIONS = True
OUTPUT_CSV = "drowsiness_log.csv"
SAVE_SCREENSHOT_ON_DETECT = True  # <- AKTIFKAN SCREENSHOT
SCREENSHOT_FOLDER = "drowsiness_shots"  # <- FOLDER KHUSUS
# ----------------------------------------

LEFT_EYE_IDX  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [263, 387, 385, 362, 380, 373]

def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def compute_ear(landmarks, eye_indices, image_w, image_h):
    pts = []
    for idx in eye_indices:
        lm = landmarks[idx]
        x, y = int(lm.x * image_w), int(lm.y * image_h)
        pts.append((x, y))
    p1, p2, p3, p4, p5, p6 = pts
    horiz = euclidean(p1, p4)
    vert1 = euclidean(p2, p6)
    vert2 = euclidean(p3, p5)
    ear = (vert1 + vert2) / (2.0 * horiz + 1e-8)
    return ear, pts

def create_alarm_wav(text, filename):
    """Create WAV file using pyttsx3 (offline). Overwrites if exists=False."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(text, filename)
        engine.runAndWait()
        engine.stop()
        return True
    except Exception as e:
        print("[Alarm] Gagal membuat WAV lewat pyttsx3:", e)
        return False

def play_alarm_file(filename):
    """Play WAV once using simpleaudio (non-blocking)."""
    try:
        if not os.path.exists(filename):
            print("[Alarm] File tidak ditemukan:", filename)
            return False
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play() 
        return True
    except Exception as e:
        print("[Alarm] simpleaudio gagal memutar:", e)
        return False

def ensure_alarm_file():
    if os.path.exists(ALARM_FILENAME):
        return True
    print("[Alarm] File WAV tidak ditemukan. Membuat dengan pyttsx3...")
    ok = create_alarm_wav("Pengguna terdeteksi mengantuk", ALARM_FILENAME)
    if ok:
        print("[Alarm] File WAV dibuat:", ALARM_FILENAME)
    else:
        print("[Alarm] Gagal membuat file WAV.")
    return ok

def main():
    # create alarm wav if missing
    ensure_alarm_file()
    
    # Buat folder screenshot jika aktif
    if SAVE_SCREENSHOT_ON_DETECT:
        os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
        print(f"[SCREENSHOT] Folder screenshot: {SCREENSHOT_FOLDER}")

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                      max_num_faces=1,
                                      refine_landmarks=True,
                                      min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print("ERROR: Tidak dapat membuka kamera. Coba ganti CAMERA_SOURCE.")
        return

    frame_counter = 0
    alarm_triggered = False
    screenshot_taken = False  # Flag untuk mencegah multiple screenshot

    if LOG_DETECTIONS:
        import csv
        csv_file = open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "ear_mean", "frame_count", "detected"])

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Gagal membaca frame.")
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            ear_mean = None

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0].landmark
                ear_l, pts_l = compute_ear(face_landmarks, LEFT_EYE_IDX, w, h)
                ear_r, pts_r = compute_ear(face_landmarks, RIGHT_EYE_IDX, w, h)
                ear_mean = (ear_l + ear_r) / 2.0

                # draw debug points
                for p in pts_l + pts_r:
                    cv2.circle(frame, p, 2, (0,255,0), -1)

                # threshold logic
                if ear_mean < EAR_THRESHOLD:
                    frame_counter += 1
                else:
                    frame_counter = 0
                    alarm_triggered = False
                    screenshot_taken = False  # Reset flag saat mata terbuka

                if frame_counter >= CONSECUTIVE_FRAMES:
                    cv2.putText(frame, "DROWSINESS DETECTED!", (30,80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3)
                    
                    if not alarm_triggered:
                        # play alarm in thread so we don't block video loop
                        t = threading.Thread(target=play_alarm_file, args=(ALARM_FILENAME,), daemon=True)
                        t.start()
                        alarm_triggered = True

                    # SCREENSHOT OTOMATIS - hanya sekali saat pertama kali terdeteksi
                    if SAVE_SCREENSHOT_ON_DETECT and not screenshot_taken:
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        fname = os.path.join(SCREENSHOT_FOLDER, f"drowsy_{timestamp}.jpg")
                        success = cv2.imwrite(fname, frame)
                        if success:
                            print(f"[SCREENSHOT] Tersimpan: {fname}")
                            screenshot_taken = True
                        else:
                            print(f"[SCREENSHOT] Gagal menyimpan: {fname}")

                    if LOG_DETECTIONS:
                        ts = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
                        csv_writer.writerow([ts, f"{ear_mean:.3f}", frame_counter, "yes"])

                else:
                    cv2.putText(frame, f"EAR: {ear_mean:.3f}", (30,40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
                    if LOG_DETECTIONS:
                        ts = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
                        csv_writer.writerow([ts, f"{ear_mean:.3f}", frame_counter, "no"])
            else:
                frame_counter = 0
                alarm_triggered = False
                screenshot_taken = False
                cv2.putText(frame, "No face detected", (30,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

            cv2.imshow("Drowsiness Detector (press q or ESC to quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if LOG_DETECTIONS:
            csv_file.close()
        face_mesh.close()
        print("Program selesai.")

if __name__ == "__main__":
    main()