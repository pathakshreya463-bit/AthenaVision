# Data Cleaning Report

## Project Name

AthenaVision – Intelligent Vision-Based Analytics Platform for Academic Spaces

## Objective

The objective of this phase is to clean and standardize raw occupancy datasets collected from different sources.

## Raw Datasets

1. occupancy_raw.csv
2. image_analysis_raw.csv

## Cleaning Operations Performed

* Removal of missing values.
* Removal of duplicate records.
* Validation of occupancy counts.
* Standardization of dataset structure.

## Unified Schema

All datasets are converted into the following format:

Source | File_Name | Time | People_Count

### Example

webcam | | 17:40:22 | 1

image | classroom.webp | | 19

image | library.webp | | 10

## Tools Used

* Python
* Pandas

## Output File

athena_cleaned.csv

## Result

The cleaning pipeline successfully combines multiple raw datasets into a single standardized dataset, making the data ready for analytics and visualization.
