import cv2
import os
from datetime import datetime
from deepface import DeepFace

# --------------------------
# Paths
# --------------------------
STUDENTS_PATH = "students"
UNKNOWN_PATH = "unknown_faces"
LOGS_PATH = "logs"

os.makedirs(STUDENTS_PATH, exist_ok=True)
os.makedirs(UNKNOWN_PATH, exist_ok=True)
os.makedirs(LOGS_PATH, exist_ok=True)

# --------------------------
# Load students
# --------------------------
def load_students():
    students = os.listdir(STUDENTS_PATH)
    return {img.split(".")[0]: os.path.join(STUDENTS_PATH, img) for img in students}

student_paths = load_students()
print("Loaded students:", list(student_paths.keys()))

# --------------------------
# Attendance storage
# --------------------------
attendance_today = {}

# --------------------------
# Attendance function
# --------------------------
def markAttendance(name):

    today = datetime.now().strftime("%d/%m/%Y")

    if not os.path.exists("Attendance.csv"):
        with open("Attendance.csv", "w") as f:
            f.write("Name,Time,Date\n")

    with open("Attendance.csv", "r+") as f:

        lines = f.readlines()

        names_today = set(line.split(",")[0] for line in lines if today in line)

        if name not in names_today:

            now = datetime.now()
            time = now.strftime("%H:%M:%S")

            f.write(f"{name},{time},{today}\n")

            attendance_today[name] = time

            print(f"Attendance marked for {name}")

# --------------------------
# Webcam
# --------------------------
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

print("Press 's' to register student | 'q' to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    unknown_detected = False

    for (x, y, w, h) in faces:

        face_img = frame[y:y+h, x:x+w]

        detected_name = "Unknown"
        confidence = 0

        for name, path in student_paths.items():

            try:

                result = DeepFace.verify(face_img, path, enforce_detection=True)

                if result["verified"]:

                    detected_name = name
                    confidence = 1 - result["distance"]

                    markAttendance(name)

                    cv2.imwrite(
                        f"{LOGS_PATH}/{name}_{datetime.now().strftime('%H%M%S')}.jpg",
                        frame
                    )

                    break

            except:
                continue

        if detected_name == "Unknown":

            unknown_detected = True

            cv2.imwrite(
                f"{UNKNOWN_PATH}/unknown_{datetime.now().strftime('%H%M%S')}.jpg",
                face_img
            )

        color = (0,255,0) if detected_name!="Unknown" else (0,0,255)

        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)

        cv2.putText(
            frame,
            f"{detected_name} ({confidence*100:.1f}%)",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    # --------------------------
    # Unknown Alert
    # --------------------------
    if unknown_detected:

        cv2.putText(
            frame,
            "⚠ UNKNOWN PERSON DETECTED",
            (50,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )

    # --------------------------
    # Attendance Panel
    # --------------------------
    y_offset = 80

    cv2.putText(
        frame,
        "Attendance Today",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    for name,time in attendance_today.items():

        cv2.putText(
            frame,
            f"{name} {time}",
            (20,y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        y_offset += 30

    cv2.imshow("Face Recognition Attendance",frame)

    key = cv2.waitKey(1)

    # --------------------------
    # Register Student
    # --------------------------
    if key == ord('s'):

        name = input("Enter student name: ")

        if name != "":

            cv2.imwrite(f"{STUDENTS_PATH}/{name}.jpg", frame)

            print("Student registered successfully")

            student_paths = load_students()

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()