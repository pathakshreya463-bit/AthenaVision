# AthenaVision - Data Cleaning Report

## Objective

Improve dataset quality by removing inconsistencies and unnecessary noise.

## Dataset Checked

datasets/occupancy.csv

## Cleaning Operations Performed

### 1. Missing Value Check

Result: No missing values found.

### 2. Duplicate Record Check

Result: No duplicate records found.

### 3. Timestamp Standardization

Original Format:
2026-06-17 16:50:20.146757

Cleaned Format:
17:01:09

Reason:
Microseconds and full date information were unnecessary for occupancy monitoring.

### 4. Noise Reduction

Original collection frequency:
Every frame

Cleaned collection frequency:
Every 5 seconds

Reason:
Reduced redundant observations and improved dataset readability.

## Outcome

The dataset was verified, standardized, and prepared for analytics and reporting.
