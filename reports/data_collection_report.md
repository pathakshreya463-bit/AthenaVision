# AthenaVision - Data Collection Report

## Project Name

AthenaVision: Intelligent Occupancy Analytics System

## Objective

To collect occupancy data from classrooms, libraries, and study spaces using computer vision techniques.

## Data Source

* Webcam video stream
* YOLOv8 Nano (yolov8n.pt) pretrained model
* Person detection class (Class ID = 0)

## Data Collection Method

The system captures live video frames from a webcam and performs person detection using YOLOv8. The number of detected people is counted and recorded at 5-second intervals.

## Dataset Fields

| Field        | Description               |
| ------------ | ------------------------- |
| Time         | Timestamp of observation  |
| People_Count | Number of detected people |

## Sample Dataset

| Time     | People_Count |
| -------- | ------------ |
| 17:01:09 | 1            |
| 17:01:14 | 1            |
| 17:01:19 | 1            |

## Storage Format

CSV (Comma Separated Values)

## Dataset Location

datasets/occupancy.csv

## Tools Used

* Python
* OpenCV
* Ultralytics YOLOv8
* CSV Module

## Outcome

A structured occupancy dataset was successfully generated and stored for future analytics and reporting.
