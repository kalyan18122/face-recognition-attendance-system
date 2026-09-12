"""
dashboard.py
The main menu shown after a successful login. Lets the user start
face recognition (attendance marking), view the attendance CSV, or
clean up saved "unknown face" images.
"""

import tkinter as tk
import facerecognition
import attendance


def start_dashboard():
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("300x270")
    root.resizable(False, False)

    tk.Label(root, text="FACE ATTENDANCE SYSTEM", font=("Arial", 14, "bold")).pack(pady=15)

    tk.Button(root, text="Start Face Recognition",
              command=facerecognition.start_recognition,
              width=25).pack(pady=8)

    tk.Button(root, text="View Attendance",
              command=attendance.open_attendance_file,
              width=25).pack(pady=8)

    tk.Button(root, text="Clean Unknown Faces",
              command=attendance.clean_unknown,
              width=25).pack(pady=8)

    tk.Button(root, text="Exit",
              command=root.destroy, width=25).pack(pady=8)

    root.mainloop()


if __name__ == "__main__":
    start_dashboard()
