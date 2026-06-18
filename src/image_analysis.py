from ultralytics import YOLO
import cv2
import csv
import os

model = YOLO("yolov8n.pt")

image_folder = "datasets/images"

file = open("datasets/image_analysis.csv", "w", newline="")
writer = csv.writer(file)

writer.writerow(["Image_Name", "People_Count"])

valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

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
            class_id = int(box.cls[0])

            if class_id == 0:
                person_count += 1

        writer.writerow([image_name, person_count])

        print(f"{image_name} -> {person_count} people")

file.close()

print("\nAnalysis completed!")
print("Results saved in datasets/image_analysis.csv")