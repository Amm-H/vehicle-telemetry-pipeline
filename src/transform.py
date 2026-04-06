import numpy as np
import pandas as pd


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["delta_time_s"] = df["timestamp"].diff().dt.total_seconds()
    df["delta_time_s"] = df["delta_time_s"].fillna(0)

    speed_mps = df["speed_kmh"] / 3.6
    delta_speed = speed_mps.diff().fillna(0)

    df["acceleration_mps2"] = np.where(
        df["delta_time_s"] > 0,
        delta_speed / df["delta_time_s"],
        0,
    )

    df["rolling_speed_kmh"] = df["speed_kmh"].rolling(window=5, min_periods=1).mean()
    df["throttle_change_pct"] = df["throttle_pct"].diff().fillna(0)

    df["is_hard_brake"] = ((df["brake"] == 1) & (df["acceleration_mps2"] < -3.0)).astype(int)
    df["is_hard_acceleration"] = (df["acceleration_mps2"] > 2.5).astype(int)

    return df