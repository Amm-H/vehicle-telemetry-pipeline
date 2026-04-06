import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def detect_braking_events(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    event_mask = (df["brake"] == 1) | (df["acceleration_mps2"] < -2.0)
    df["braking_event_flag"] = event_mask.astype(int)

    events = []
    in_event = False
    start_idx = None

    for idx, flag in enumerate(df["braking_event_flag"]):
        if flag == 1 and not in_event:
            in_event = True
            start_idx = idx
        elif flag == 0 and in_event:
            end_idx = idx - 1
            events.append(_build_event_record(df, start_idx, end_idx))
            in_event = False
            start_idx = None

    if in_event and start_idx is not None:
        events.append(_build_event_record(df, start_idx, len(df) - 1))

    return pd.DataFrame(events)


def _build_event_record(df: pd.DataFrame, start_idx: int, end_idx: int) -> dict:
    segment = df.iloc[start_idx : end_idx + 1]

    start_time = segment["timestamp"].iloc[0]
    end_time = segment["timestamp"].iloc[-1]
    duration = (end_time - start_time).total_seconds()

    return {
        "start_timestamp": start_time,
        "end_timestamp": end_time,
        "duration_s": duration,
        "max_speed_kmh": segment["speed_kmh"].max(),
        "min_acceleration_mps2": segment["acceleration_mps2"].min(),
        "avg_throttle_pct": segment["throttle_pct"].mean(),
    }


def build_summary(df: pd.DataFrame, events: pd.DataFrame) -> dict:
    return {
        "total_rows": int(len(df)),
        "avg_speed_kmh": float(df["speed_kmh"].mean()),
        "max_speed_kmh": float(df["speed_kmh"].max()),
        "avg_engine_rpm": float(df["engine_rpm"].mean()),
        "hard_braking_events": int(len(events)),
        "hard_acceleration_events": int(df["is_hard_acceleration"].sum()),
    }


def save_summary(summary: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def generate_plots(df: pd.DataFrame, speed_plot_path: Path, rpm_plot_path: Path) -> None:
    speed_plot_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["speed_kmh"])
    plt.title("Speed Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Speed (km/h)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(speed_plot_path)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["engine_rpm"])
    plt.title("Engine RPM Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("RPM")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(rpm_plot_path)
    plt.close()