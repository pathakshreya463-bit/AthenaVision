
from ultralytics import YOLO
import cv2
import csv
import time
from datetime import datetime
import os
from src.history_logger import log_activity
# Load the model only once
model = YOLO("models/yolov8n.pt")


def analyze_webcam():

    output_file = "datasets/rawdata/occupancy_raw.csv"

    total_people = 0
    frames_processed = 0
    max_people = 0

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Time", "People_Count"])

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise Exception("Unable to access webcam.")

        last_save_time = time.time()

        while True:

            success, frame = camera.read()

            if not success:
                break

            frame = cv2.resize(frame, (640, 480))

            detections = model(frame, verbose=False)

            person_count = 0

            for box in detections[0].boxes:

                if int(box.cls[0]) == 0:
                    person_count += 1

            total_people += person_count
            frames_processed += 1
            max_people = max(max_people, person_count)

            annotated_frame = detections[0].plot()

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

    average_people = 0

    if frames_processed > 0:
        average_people = round(total_people / frames_processed, 2)
        
        log_activity(

    module="Live Monitoring",

    source="Webcam",

    people=round(average_people, 2),

    status="Completed"

)

    return {

        "frames_processed": frames_processed,

        "average_people": average_people,

        "maximum_people": max_people,

        "status": "completed",

        "message": "Webcam analysis finished successfully."

    }


if __name__ == "__main__":
    print(analyze_webcam())

