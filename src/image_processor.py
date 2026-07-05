
from ultralytics import YOLO
import cv2
import csv
import os
from src.history_logger import log_activity

# Load the model only once
model = YOLO("models/yolov8n.pt")


def analyze_images():

    image_folder = "datasets/images"
    output_file = "datasets/rawdata/image_analysis_raw.csv"

    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

    results_list = []
    total_people = 0
    total_images = 0

    # Check if the folder exists
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"Folder '{image_folder}' not found.")

    image_files = [
        img for img in os.listdir(image_folder)
        if img.lower().endswith(valid_extensions)
    ]

    if len(image_files) == 0:
        return {
            "total_images": 0,
            "total_people": 0,
            "average_people": 0,
            "results": []
        }

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Image_Name", "People_Count"])

        for image_name in image_files:

            image_path = os.path.join(image_folder, image_name)

            image = cv2.imread(image_path)

            if image is None:
                print(f"Could not load {image_name}")
                continue

            detections = model(image, verbose=False)

            person_count = 0

            for box in detections[0].boxes:

                if int(box.cls[0]) == 0:
                    person_count += 1

            writer.writerow([image_name, person_count])

            results_list.append({
                "image": image_name,
                "people": person_count
            })
            log_activity(

    module="Image Analysis",

    source=image_name,

    people=person_count,

    status="Completed"

)

            total_images += 1
            total_people += person_count

            print(f"{image_name} -> {person_count} people")

    print("\nImage analysis completed!")

    # Run data cleaning
    os.system("py src/Clean_data.py")

    average_people = round(total_people / total_images, 2)

    return {
        "total_images": total_images,
        "total_people": total_people,
        "average_people": average_people,
        "results": results_list
    }


if __name__ == "__main__":
    print(analyze_images())
