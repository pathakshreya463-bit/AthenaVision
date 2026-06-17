# AthenaVision - Data Storage Report

## Objective

Store cleaned occupancy data in a structured and retrievable format for future analytics.

## Storage Method

CSV File Storage

## Dataset Location

datasets/occupancy.csv

## Dataset Structure

| Column       | Description               |
| ------------ | ------------------------- |
| Time         | Timestamp of observation  |
| People_Count | Number of people detected |

## Example Data

| Time     | People_Count |
| -------- | ------------ |
| 17:01:09 | 1            |
| 17:01:14 | 1            |
| 17:01:19 | 1            |

## Advantages of CSV Storage

* Simple and lightweight
* Human-readable
* Compatible with Excel
* Easy to process using Python
* Suitable for small and medium datasets

## Retrieval Method

The dataset can be accessed directly from:

datasets/occupancy.csv

and processed using Python libraries such as Pandas.

## Outcome

Occupancy data was successfully stored in a structured CSV format and made available for future analytics and reporting.
