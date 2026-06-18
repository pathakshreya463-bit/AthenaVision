from ultralytics import YOLO
import cv2
import csv
import time
from datetime import datetime

model = YOLO("yolov8n.pt")

file = open("datasets/rawdata/occupancy_raw.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["Time", "People_Count"])

camera = cv2.VideoCapture(0)

last_save_time = time.time()

while True:
    success, frame = camera.read()

    if not success:
        break

    frame = cv2.resize(frame, (640, 480))

    results = model(frame, verbose=False)

    person_count = 0

    for box in results[0].boxes:
        class_id = int(box.cls[0])

        if class_id == 0:
            person_count += 1

    annotated_frame = results[0].plot()

    current_time = time.time()

    if current_time - last_save_time >= 5:
        timestamp = datetime.now().strftime("%H:%M:%S")

        writer.writerow([timestamp, person_count])

        last_save_time = current_time

    cv2.putText(
        annotated_frame,
        f"People Count: {person_count}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 80, 140),
        2
    )

    cv2.imshow("AthenaVision YOLO", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

file.close()
camera.release()
cv2.destroyAllWindows()
print("\nWebcam analysis completed!")

import os

os.system("py src/Clean_data.py")