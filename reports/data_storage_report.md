# Data Storage Report

## Project Name

AthenaVision – Intelligent Vision-Based Analytics Platform for Academic Spaces

## Objective

To organize and store occupancy data in a structured format for future analytics and dashboard generation.

## Directory Structure

datasets/

├── rawdata/

│ ├── occupancy_raw.csv

│ └── image_analysis_raw.csv

│

├── cleaneddata/

│ └── athena_cleaned.csv

│

├── images/

└── videos/

## Storage Strategy

### Raw Data Storage

Raw datasets are stored without modification in the rawdata directory.

Examples:

* occupancy_raw.csv
* image_analysis_raw.csv

### Cleaned Data Storage

After cleaning and standardization, all records are stored in a single master dataset:

athena_cleaned.csv

This file acts as the central data source for future analytics and dashboard modules.

## Advantages

* Centralized storage architecture.
* Easier analytics and reporting.
* Reduced data duplication.
* Scalable for future image and video analysis modules.

## Result

AthenaVision now maintains a structured storage pipeline consisting of raw datasets and a unified cleaned dataset, providing a foundation for analytics and dashboard development.
