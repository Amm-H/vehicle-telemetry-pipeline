import pandas as pd


COLUMN_MAPPING = {
    "time": "timestamp",
    "speed": "speed_kmh",
    "rpm": "engine_rpm",
    "throttle": "throttle_pct",
}


def clean_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns=COLUMN_MAPPING)

    if "timestamp" not in df.columns:
        raise ValueError("Missing required timestamp column after normalization.")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    numeric_columns = ["speed_kmh", "engine_rpm", "throttle_pct", "gear"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "brake" in df.columns:
        df["brake"] = (
            df["brake"]
            .replace({True: 1, False: 0, "true": 1, "false": 0, "True": 1, "False": 0})
        )
        df["brake"] = pd.to_numeric(df["brake"], errors="coerce").fillna(0)

    df = df.drop_duplicates()
    df = df.dropna(subset=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    for col in ["speed_kmh", "engine_rpm", "throttle_pct", "gear"]:
        if col in df.columns:
            df[col] = df[col].interpolate(method="linear", limit_direction="both")

    if "speed_kmh" in df.columns:
        df["speed_kmh"] = df["speed_kmh"].clip(lower=0)

    if "engine_rpm" in df.columns:
        df["engine_rpm"] = df["engine_rpm"].clip(lower=0)

    if "throttle_pct" in df.columns:
        df["throttle_pct"] = df["throttle_pct"].clip(lower=0, upper=100)

    if "gear" in df.columns:
        df["gear"] = df["gear"].clip(lower=0)

    if "brake" in df.columns:
        df["brake"] = df["brake"].fillna(0)
        df["brake"] = (df["brake"] > 0).astype(int)

    return df