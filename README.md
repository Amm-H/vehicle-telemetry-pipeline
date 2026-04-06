# Vehicle Telemetry Data Pipeline

## Overview
This project implements an end-to-end Python pipeline for vehicle telemetry data processing and analysis. It ingests raw telemetry, cleans and validates the signals, derives additional driving-performance metrics, detects braking events, and generates reports.

## Features
- Raw telemetry ingestion from CSV
- Data cleaning and normalization
- Validation of automotive telemetry fields
- Derived feature generation
- Braking event detection
- Summary report generation
- Plot generation
- Docker support
- GitHub Actions automation

## Project Structure
```text
vehicle-telemetry-pipeline/
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ reports/
├─ src/
├─ tests/
├─ .github/workflows/
├─ Dockerfile
├─ requirements.txt
├─ README.md
└─ run_pipeline.py
```

## Input Schema
Expected telemetry columns:
- timestamp
- speed_kmh
- engine_rpm
- throttle_pct
- brake
- gear

## How to Run
### Local
```bash
pip install -r requirements.txt
python run_pipeline.py
```

### Tests
```bash
python -m pytest
```

### Docker
```bash
docker build -t vehicle-telemetry-pipeline .
docker run --rm vehicle-telemetry-pipeline
```

## Outputs
The pipeline generates:
- cleaned telemetry parquet
- processed telemetry parquet
- braking event CSV
- summary JSON
- speed and RPM plots

## Example Use Case
This project demonstrates how vehicle time-series signals can be processed in a structured pipeline similar to real automotive or motorsport data workflows.

## Future Improvements
- OpenF1 API ingestion
- SQLite storage layer
- anomaly detection
- lap/session comparison
- dashboard visualization