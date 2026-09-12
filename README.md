# Face Recognition Attendance System

## 📌 Project Overview

A Face Recognition Based Attendance System that uses a webcam to detect
and recognize student faces and automatically record attendance.

The system trains on photos in the `students/` folder, then compares the
live webcam image against them. When it recognizes someone with enough
confidence, it logs their **name, time, and date** to `Attendance.csv`
(only once per person per day — it won't spam the same entry every frame).

---

## 🚀 Features

* Login screen before the dashboard is accessible
* Real-time face detection and recognition using OpenCV (LBPH algorithm)
* Displays the recognized student's name live on the video feed
* Automatic, once-per-day attendance recording
* Unrecognized faces are saved to `unknown_faces/` for review
* Dashboard button to view the attendance CSV
* Dashboard button to clear out saved unknown-face images

---

## 🛠 Technologies Used

* Python
* OpenCV (`opencv-contrib-python` — needed for the `cv2.face` module)
* NumPy
* Tkinter (built into Python) for the login and dashboard windows

---

## 📂 Project Structure

```
face-recognition-attendance-system/
├── main.py              # entry point — launches the login screen
├── login.py             # login window, opens dashboard on success
├── dashboard.py         # main menu: recognize / view / clean
├── facerecognition.py   # trains on students/ and runs webcam recognition
├── attendance.py        # reads/writes Attendance.csv, cleans unknown_faces/
├── Attendance.csv        # generated attendance log
├── requirements.txt
├── README.md
├── students/             # put one photo per student here, named after them
│   ├── kalyan.jpg
│   ├── ramesh.jpg
│   └── suresh.jpg
├── unknown_faces/        # auto-saved photos of unrecognized faces
└── logs/                 # reserved for future logging
```

---

## ▶ How to Run

1. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

2. Add one clear, front-facing photo per student to the `students/` folder,
   named after that student (e.g. `kalyan.jpg`, `ramesh.jpg`). The filename
   (without extension) becomes the name that gets logged.

3. Run the program:
   ```
   python main.py
   ```

4. Log in with the default credentials (change these in `login.py`):
   - **Username:** `admin`
   - **Password:** `admin123`

5. From the Dashboard, click **Start Face Recognition** to open the webcam.
   Press **q** in the webcam window to stop and return to the dashboard.

6. Click **View Attendance** to open `Attendance.csv`, or **Clean Unknown
   Faces** to delete everything saved in `unknown_faces/`.

---

## 📊 Output

Example row logged to `Attendance.csv`:

```
Name,Time,Date
kalyan,20:10:11,13/03/2026
```

---

## 👨‍💻 Author

Kalyan Kumar Reddy
