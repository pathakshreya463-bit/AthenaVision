from ultralytics import YOLO
import cv2
import csv
import os

# Load the model only once
model = YOLO("models/yolov8n.pt")


def analyze_images():

    image_folder = "datasets/images"

    output_file = "datasets/rawdata/image_analysis_raw.csv"

    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

    results_list = []

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Image_Name", "People_Count"])

        for image_name in os.listdir(image_folder):

            if image_name.lower().endswith(valid_extensions):

                image_path = os.path.join(image_folder, image_name)

                image = cv2.imread(image_path)

                if image is None:
                    print(f"Could not load {image_name}")
                    continue

                results = model(image, verbose=False)

                person_count = 0

                for box in results[0].boxes:

                    if int(box.cls[0]) == 0:

                        person_count += 1

                writer.writerow([image_name, person_count])

                results_list.append({

                    "image": image_name,

                    "people": person_count

                })

                print(f"{image_name} -> {person_count} people")

    print("\nImage analysis completed!")

    os.system("py src/Clean_data.py")

    return results_list


if __name__ == "__main__":

    analyze_images()