import pandas as pd
from src.config import REQUIRED_COLUMNS


def validate_telemetry(df: pd.DataFrame) -> None:
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df["timestamp"].isna().any():
        raise ValueError("Timestamp column contains invalid values.")

    if (df["speed_kmh"] < 0).any():
        raise ValueError("speed_kmh contains negative values.")

    if (df["engine_rpm"] < 0).any():
        raise ValueError("engine_rpm contains negative values.")

    if ((df["throttle_pct"] < 0) | (df["throttle_pct"] > 100)).any():
        raise ValueError("throttle_pct must be between 0 and 100.")

    if not df["brake"].isin([0, 1]).all():
        raise ValueError("brake column must contain only 0 or 1.")

    if df.empty:
        raise ValueError("Telemetry dataset is empty.")