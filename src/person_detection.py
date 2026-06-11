from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    frame=cv2.resize(frame, (640, 480))

    results = model(frame, verbose=False)

    annotated_frame = results[0].plot()

    cv2.imshow("AthenaVision YOLO", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()