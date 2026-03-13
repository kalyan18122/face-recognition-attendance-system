import cv2
import os
from datetime import datetime
from deepface import DeepFace

# Folder containing student images
path = "students"
images = os.listdir(path)

# Start webcam
cap = cv2.VideoCapture(0)

# Attendance function
def markAttendance(name):
    with open("Attendance.csv","a+") as f:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        f.write(f"\n{name},{time},{date}")

print("Loaded images:", images)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    detected_name = "Unknown"

    # Compare webcam face with stored images
    for img in images:
        try:
            result = DeepFace.verify(
                frame,
                f"{path}/{img}",
                enforce_detection=False
            )

            if result["verified"]:
                detected_name = img.split(".")[0]
                markAttendance(detected_name)
                break

        except:
            pass

    # Draw rectangle
    height, width, _ = frame.shape
    cv2.rectangle(frame,(100,100),(width-100,height-100),(0,255,0),2)

    # Show name
    cv2.putText(frame,
                detected_name,
                (120,140),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.imshow("Face Recognition Attendance", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()