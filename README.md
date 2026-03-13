# Face Recognition Attendance System

## 📌 Project Overview

This project is a **Face Recognition Based Attendance System** that uses a webcam to detect and recognize student faces and automatically record attendance.

The system compares the live webcam image with stored student images and saves the attendance with **name, time, and date** in a CSV file.

---

## 🚀 Features

* Real-time face detection using webcam
* Face recognition using DeepFace
* Displays detected student name on the screen
* Automatic attendance recording
* Attendance stored in CSV file

---

## 🛠 Technologies Used

* Python
* OpenCV
* DeepFace
* Pandas

---

## 📂 Project Structure

face-recognition-attendance-system
│
├── main.py
├── Attendance.csv
├── requirements.txt
├── README.md
└── students
  ├── kalyan.jpg
  ├── ramesh.jpg
  └── suresh.jpg

---

## ▶ How to Run

1. Clone the repository

```
git clone https://github.com/kalyan18122/face-recognition-attendance-system.git
```

2. Install required libraries

```
pip install -r requirements.txt
```

3. Add student images to the **students** folder.

4. Run the program

```
python main.py
```

5. Press **q** to exit the webcam.

---

## 📊 Output

* Webcam detects the face
* Displays the student name on the screen
* Saves attendance in **Attendance.csv**

Example:

Name,Time,Date
kalyan,20:10:11,13/03/2026

---

## 👨‍💻 Author

Kalyan Kumar Reddy
