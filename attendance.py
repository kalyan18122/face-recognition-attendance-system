"""
attendance.py
Handles reading/writing the Attendance.csv file, preventing duplicate
same-day entries, opening the file for viewing, and cleaning up the
folder of captured "unknown face" images.
"""

import os
import csv
from datetime import datetime

ATTENDANCE_FILE = "Attendance.csv"
UNKNOWN_DIR = "unknown_faces"


def _ensure_file_exists():
    """Create Attendance.csv with a header row if it doesn't exist yet."""
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Time", "Date"])


def _already_marked_today(name, today_str):
    """Check the CSV to see if `name` already has an entry for today's date."""
    if not os.path.exists(ATTENDANCE_FILE):
        return False

    with open(ATTENDANCE_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 3 and row[0] == name and row[2] == today_str:
                return True
    return False


def mark(name):
    """
    Record attendance for `name` if they have not already been marked
    today. This avoids the old bug where the same person got logged
    dozens of times per second while the camera kept detecting them.
    """
    _ensure_file_exists()

    now = datetime.now()
    today_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")

    if _already_marked_today(name, today_str):
        return False  # already marked, nothing to do

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, time_str, today_str])

    print(f"[Attendance] Marked {name} present at {time_str} on {today_str}")
    return True


def open_attendance_file():
    """Open Attendance.csv in the OS's default application (Excel, etc.)."""
    _ensure_file_exists()
    try:
        if os.name == "nt":  # Windows
            os.startfile(ATTENDANCE_FILE)
        elif os.uname().sysname == "Darwin":  # macOS
            os.system(f'open "{ATTENDANCE_FILE}"')
        else:  # Linux
            os.system(f'xdg-open "{ATTENDANCE_FILE}"')
    except Exception as e:
        print(f"Could not open {ATTENDANCE_FILE} automatically: {e}")
        print("You can open it manually from the project folder.")


def clean_unknown():
    """Delete every captured image in the unknown_faces folder."""
    if not os.path.exists(UNKNOWN_DIR):
        os.makedirs(UNKNOWN_DIR, exist_ok=True)
        print("No unknown_faces folder existed — created an empty one.")
        return

    removed = 0
    for filename in os.listdir(UNKNOWN_DIR):
        file_path = os.path.join(UNKNOWN_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                removed += 1
        except Exception as e:
            print(f"Could not delete {file_path}: {e}")

    print(f"[Attendance] Removed {removed} unknown face image(s).")
