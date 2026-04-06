import pandas as pd
import pytest
from src.validate import validate_telemetry


def test_validate_telemetry_passes_on_valid_data():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01 10:00:00"]),
            "speed_kmh": [120],
            "engine_rpm": [3500],
            "throttle_pct": [70],
            "brake": [0],
            "gear": [5],
        }
    )

    validate_telemetry(df)


def test_validate_telemetry_fails_on_negative_speed():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01 10:00:00"]),
            "speed_kmh": [-1],
            "engine_rpm": [3500],
            "throttle_pct": [70],
            "brake": [0],
            "gear": [5],
        }
    )

    with pytest.raises(ValueError):
        validate_telemetry(df)