from ultralytics import YOLO
import cv2
import csv
import time
from datetime import datetime
import os

model = YOLO("models/yolov8n.pt")


def analyze_webcam():

    output_file = "datasets/rawdata/occupancy_raw.csv"

    with open(output_file, "w", newline="") as file:

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

                if int(box.cls[0]) == 0:
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

            cv2.imshow("AthenaVision Webcam", annotated_frame)

            if cv2.waitKey(1) == 27:
                break

        camera.release()

    cv2.destroyAllWindows()

    print("Webcam analysis completed!")

    os.system("py src/Clean_data.py")

    return {
        "status": "completed",
        "message": "Webcam analysis finished successfully."
    }


if __name__ == "__main__":
    analyze_webcam()