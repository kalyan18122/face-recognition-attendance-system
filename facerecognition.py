"""
facerecognition.py
Trains an OpenCV LBPH face recognizer on the images in students/,
then opens the webcam and marks attendance for anyone it recognizes
with reasonable confidence. Unrecognized faces get saved into
unknown_faces/ so you can review them later.
"""

import cv2
import os
import numpy as np
from datetime import datetime
import attendance

STUDENTS_DIR = "students"
UNKNOWN_DIR = "unknown_faces"
LOGS_DIR = "logs"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")
RECOGNITION_SIZE = (200, 200)  # all training/detected faces are resized to this
CONFIDENCE_THRESHOLD = 80       # lower = stricter match required
UNKNOWN_SAVE_COOLDOWN_SECONDS = 5

os.makedirs(STUDENTS_DIR, exist_ok=True)
os.makedirs(UNKNOWN_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


def _load_training_data(face_detector):
    """Read every valid image in students/, find the face inside it with
    the SAME detector used on the live webcam feed, crop just that face,
    and resize it consistently. Training on a cropped face (not the whole
    photo) is essential — otherwise the recognizer compares a squashed
    full-body photo against a tightly-cropped webcam face and never
    matches, even for the right person."""
    faces = []
    labels = []
    label_map = {}

    student_files = [
        f for f in os.listdir(STUDENTS_DIR)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    for i, filename in enumerate(student_files):
        path = os.path.join(STUDENTS_DIR, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"Skipping {filename} — could not be read as an image.")
            continue

        detected = face_detector.detectMultiScale(img, 1.3, 5)
        if len(detected) == 0:
            print(f"Skipping {filename} — no face detected in this photo. "
                  f"Use a clearer, front-facing photo.")
            continue

        # Use the largest detected face in the photo (in case of multiple).
        x, y, w, h = max(detected, key=lambda box: box[2] * box[3])
        face_crop = cv2.resize(img[y:y + h, x:x + w], RECOGNITION_SIZE)

        faces.append(face_crop)
        labels.append(i)

        name = os.path.splitext(filename)[0]
        label_map[i] = name

    return faces, labels, label_map


def start_recognition():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        print("ERROR: cv2.face is not available.")
        print("You likely have 'opencv-python' installed instead of")
        print("'opencv-contrib-python'. Run:")
        print("    pip uninstall opencv-python")
        print("    pip install opencv-contrib-python")
        return

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces, labels, label_map = _load_training_data(face_detector)

    if len(faces) == 0:
        print(f"No usable student images found in '{STUDENTS_DIR}/'. "
              f"Add .jpg/.jpeg/.png photos named after each student "
              f"(e.g. kalyan.jpg) and try again.")
        return

    recognizer.train(faces, np.array(labels))

    # On Windows, the default camera backend (MSMF) is sometimes blocked
    # by privacy/driver issues even when the camera works fine elsewhere.
    # Forcing the older DirectShow backend usually gets around this.
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        # Fall back to the default backend if DirectShow isn't available.
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open the webcam. Check that it's connected "
              "and not being used by another application.")
        return

    last_unknown_save = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from webcam. Stopping.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces_detected:
                face_roi = cv2.resize(gray[y:y + h, x:x + w], RECOGNITION_SIZE)
                label, confidence = recognizer.predict(face_roi)

                if confidence < CONFIDENCE_THRESHOLD:
                    name = label_map[label]
                    attendance.mark(name)

                    cv2.putText(frame, f"{name} ({100 - int(confidence)}%)",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    now_ts = datetime.now().timestamp()
                    if now_ts - last_unknown_save > UNKNOWN_SAVE_COOLDOWN_SECONDS:
                        filename = f"unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        cv2.imwrite(os.path.join(UNKNOWN_DIR, filename),
                                    frame[y:y + h, x:x + w])
                        last_unknown_save = now_ts

            cv2.imshow("Attendance System - press q to quit", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    start_recognition()
