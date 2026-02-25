# Data Lab – Pandas & Data Quality

## Overview
This project demonstrates how to ingest, clean, validate, and analyze raw product data using Python and pandas.

## Data
The input data (`products.csv`) contains intentionally messy values such as:
- missing prices and currencies
- negative prices
- mixed date formats
- invalid dates

## Processing Steps
1. Load CSV data into pandas
2. Clean and normalize text fields
3. Convert prices to numeric values
4. Parse dates and handle invalid formats
5. Apply basic data quality rules (reject invalid rows)
6. Generate summary analytics

## Output
The script produces `analytics_summary.csv` containing:
- average_price
- median_price
- product_count
- missing_price_count

The average price is affected by extreme outliers, which is why the median price is a more representative metric.

## How to Run
```bash
python3 main.py
