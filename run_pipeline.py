from src.analyze import build_summary, detect_braking_events, generate_plots, save_summary
from src.clean import clean_telemetry
from src.config import (
    BRAKING_EVENTS_FILE,
    CLEANED_OUTPUT_FILE,
    DEFAULT_DRIVER_NUMBER,
    DEFAULT_COUNTRY_NAME,
    DEFAULT_SESSION_NAME,
    DEFAULT_YEAR,
    PROCESSED_OUTPUT_FILE,
    RAW_ARCHIVE_FILE,
    RAW_INPUT_FILE,
    REPORTS_DIR,
    SPEED_PLOT_FILE,
    RPM_PLOT_FILE,
    PROCESSED_DIR,
    RAW_DIR,
)
from src.ingest import (
    ingest_openf1_telemetry,
    load_raw_data,
    save_raw_copy,
)
from src.transform import add_derived_features
from src.utils import ensure_directories
from src.validate import validate_telemetry


def main() -> None:
    ensure_directories([RAW_DIR, PROCESSED_DIR, REPORTS_DIR])

    try:
        raw_df = ingest_openf1_telemetry(
            year=DEFAULT_YEAR,
            country_name=DEFAULT_COUNTRY_NAME,
            session_name=DEFAULT_SESSION_NAME,
            driver_number=DEFAULT_DRIVER_NUMBER,
        )
        raw_df.to_csv(RAW_INPUT_FILE, index=False)
        print("Fetched telemetry from OpenF1 API.")
    except Exception as exc:
        print(f"OpenF1 ingestion failed, falling back to local CSV. Reason: {exc}")
        raw_df = load_raw_data(RAW_INPUT_FILE)

    save_raw_copy(raw_df, RAW_ARCHIVE_FILE)

    cleaned_df = clean_telemetry(raw_df)
    validate_telemetry(cleaned_df)
    cleaned_df.to_parquet(CLEANED_OUTPUT_FILE, index=False)

    processed_df = add_derived_features(cleaned_df)
    processed_df.to_parquet(PROCESSED_OUTPUT_FILE, index=False)

    events_df = detect_braking_events(processed_df)
    events_df.to_csv(BRAKING_EVENTS_FILE, index=False)

    summary = build_summary(processed_df, events_df)
    save_summary(summary, REPORTS_DIR / "summary.json")

    generate_plots(processed_df, SPEED_PLOT_FILE, RPM_PLOT_FILE)

    print("Pipeline completed successfully.")
    print(f"Processed data saved to: {PROCESSED_OUTPUT_FILE}")
    print(f"Braking events saved to: {BRAKING_EVENTS_FILE}")


if __name__ == "__main__":
    main()