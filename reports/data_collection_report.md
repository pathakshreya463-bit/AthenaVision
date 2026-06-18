# Data Collection Report

## Project Name

AthenaVision – Intelligent Vision-Based Analytics Platform for Academic Spaces

## Objective

The objective of this phase is to collect occupancy data from different sources and store it for further processing and analysis.

## Data Sources

1. Webcam Feed

   * Live video captured using OpenCV.
   * YOLOv8 is used to detect people in real time.
   * Person count is recorded every 5 seconds.

2. Image Dataset

   * Images are stored in the datasets/images directory.
   * YOLOv8 analyzes each image and detects the number of people present.
   * Results are stored in a raw dataset.

## Tools and Technologies

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* CSV Files

## Output Files

* occupancy_raw.csv
* image_analysis_raw.csv

## Result

AthenaVision successfully collects occupancy data from webcam feeds and image datasets, generating raw datasets for further cleaning and processing.
