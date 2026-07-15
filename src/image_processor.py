from ultralytics import YOLO
from src.history_logger import log_activity

import cv2
import numpy as np
import csv
import os

# Load YOLO model only once
model = YOLO("models/yolov8n.pt")


def analyze_images(image_file):

    # ----------------------------------------
    # Read uploaded image
    # ----------------------------------------

    image_bytes = image_file.read()

    np_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:

        return {
            "status": "error",
            "message": "Invalid image."
        }

    # ----------------------------------------
    # Run YOLO
    # ----------------------------------------

    results = model(image, verbose=False)

    people = 0

    for box in results[0].boxes:

        if int(box.cls[0]) == 0:

            people += 1

    # ----------------------------------------
    # Save result to CSV
    # ----------------------------------------

    output_file = "datasets/rawdata/image_analysis_raw.csv"

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Image_Name",
                "People_Count"
            ])

        writer.writerow([
            image_file.filename,
            people
        ])

    # ----------------------------------------
    # Update History
    # ----------------------------------------

    log_activity(

        module="Image Analysis",

        source=image_file.filename,

        people=people,

        status="Completed"

    )

    # ----------------------------------------
    # Clean Dataset
    # ----------------------------------------

    os.system("py src/Clean_data.py")

    # ----------------------------------------
    # Return Result
    # ----------------------------------------

    return {

        "status": "success",

        "image": image_file.filename,

        "people": people,

        "message": "Image analyzed successfully."

    }