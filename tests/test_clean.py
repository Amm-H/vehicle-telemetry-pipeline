import pandas as pd
from src.clean import clean_telemetry


def test_clean_telemetry_parses_timestamp_and_removes_duplicates():
    df = pd.DataFrame(
        {
            "timestamp": ["2024-01-01 10:00:00", "2024-01-01 10:00:00"],
            "speed_kmh": [100, 100],
            "engine_rpm": [3000, 3000],
            "throttle_pct": [50, 50],
            "brake": [0, 0],
            "gear": [4, 4],
        }
    )

    cleaned = clean_telemetry(df)

    assert len(cleaned) == 1
    assert pd.api.types.is_datetime64_any_dtype(cleaned["timestamp"])