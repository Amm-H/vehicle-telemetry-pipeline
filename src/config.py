from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

RAW_INPUT_FILE = RAW_DIR / "sample_telemetry.csv"
RAW_ARCHIVE_FILE = RAW_DIR / "raw_telemetry_snapshot.csv"

CLEANED_OUTPUT_FILE = PROCESSED_DIR / "cleaned_telemetry.parquet"
PROCESSED_OUTPUT_FILE = PROCESSED_DIR / "telemetry_processed.parquet"

BRAKING_EVENTS_FILE = REPORTS_DIR / "braking_events.csv"
SUMMARY_FILE = REPORTS_DIR / "summary.json"
SPEED_PLOT_FILE = REPORTS_DIR / "speed_over_time.png"
RPM_PLOT_FILE = REPORTS_DIR / "rpm_over_time.png"

REQUIRED_COLUMNS = [
    "timestamp",
    "speed_kmh",
    "engine_rpm",
    "throttle_pct",
    "brake",
    "gear",
]

OPENF1_BASE_URL = "https://api.openf1.org/v1"
DEFAULT_SESSION_NAME = "Race"
DEFAULT_YEAR = 2023
DEFAULT_COUNTRY_NAME = "Belgium"
DEFAULT_DRIVER_NUMBER = 55