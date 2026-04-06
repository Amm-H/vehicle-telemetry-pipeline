from pathlib import Path
from typing import Any

import pandas as pd
import requests

from src.config import OPENF1_BASE_URL


def load_raw_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")
    return pd.read_csv(path)


def save_raw_copy(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def fetch_openf1_sessions(year: int, country_name: str, session_name: str) -> pd.DataFrame:
    response = requests.get(
        f"{OPENF1_BASE_URL}/sessions",
        params={
            "year": year,
            "country_name": country_name,
            "session_name": session_name,
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError(
            f"No OpenF1 sessions found for year={year}, country_name={country_name}, "
            f"session_name={session_name}"
        )

    return pd.DataFrame(data)


def fetch_openf1_car_data(session_key: int, driver_number: int) -> pd.DataFrame:
    response = requests.get(
        f"{OPENF1_BASE_URL}/car_data",
        params={
            "session_key": session_key,
            "driver_number": driver_number,
        },
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError(
            f"No car_data rows returned for session_key={session_key}, "
            f"driver_number={driver_number}"
        )

    return pd.DataFrame(data)


def normalize_openf1_car_data(df: pd.DataFrame) -> pd.DataFrame:
    required = ["date", "speed", "rpm", "throttle", "brake", "n_gear"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"OpenF1 car_data missing columns: {missing}")

    normalized = df.copy()

    normalized = normalized.rename(
        columns={
            "date": "timestamp",
            "speed": "speed_kmh",
            "rpm": "engine_rpm",
            "throttle": "throttle_pct",
            "n_gear": "gear",
        }
    )

    normalized = normalized[
        ["timestamp", "speed_kmh", "engine_rpm", "throttle_pct", "brake", "gear"]
    ].copy()

    normalized["timestamp"] = pd.to_datetime(normalized["timestamp"], errors="coerce")
    normalized["speed_kmh"] = pd.to_numeric(normalized["speed_kmh"], errors="coerce")
    normalized["engine_rpm"] = pd.to_numeric(normalized["engine_rpm"], errors="coerce")
    normalized["throttle_pct"] = pd.to_numeric(normalized["throttle_pct"], errors="coerce")
    normalized["throttle_pct"] = normalized["throttle_pct"].clip(lower=0, upper=100)
    normalized["gear"] = pd.to_numeric(normalized["gear"], errors="coerce")

    # OpenF1 brake is documented as 100 when pressed and 0 when not pressed.
    normalized["brake"] = pd.to_numeric(normalized["brake"], errors="coerce").fillna(0)
    normalized["brake"] = (normalized["brake"] > 0).astype(int)

    return normalized


def ingest_openf1_telemetry(
    year: int,
    country_name: str,
    session_name: str,
    driver_number: int,
) -> pd.DataFrame:
    sessions_df = fetch_openf1_sessions(
        year=year,
        country_name=country_name,
        session_name=session_name,
    )

    # pick the first matching session
    session_key = int(sessions_df.iloc[0]["session_key"])

    raw_car_df = fetch_openf1_car_data(
        session_key=session_key,
        driver_number=driver_number,
    )

    return normalize_openf1_car_data(raw_car_df)