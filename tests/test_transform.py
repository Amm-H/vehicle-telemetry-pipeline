import pandas as pd
from src.transform import add_derived_features


def test_add_derived_features_creates_expected_columns():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2024-01-01 10:00:00", "2024-01-01 10:00:01", "2024-01-01 10:00:02"]
            ),
            "speed_kmh": [0, 36, 72],
            "engine_rpm": [1000, 2000, 3000],
            "throttle_pct": [10, 30, 60],
            "brake": [0, 0, 0],
            "gear": [1, 2, 3],
        }
    )

    transformed = add_derived_features(df)

    assert "delta_time_s" in transformed.columns
    assert "acceleration_mps2" in transformed.columns
    assert "rolling_speed_kmh" in transformed.columns
    assert "throttle_change_pct" in transformed.columns