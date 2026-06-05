from __future__ import annotations

import pandas as pd


BOOLEAN_COLUMNS = ["Verified", "Urgent"]


def normalize_logistics_frame(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for column in normalized.columns:
        normalized[column] = normalized[column].fillna("").astype(str).str.strip()

    for column in BOOLEAN_COLUMNS:
        normalized[column] = normalized[column].map(normalize_yes_no)

    normalized["Last Updated"] = pd.to_datetime(
        normalized["Last Updated"], errors="coerce"
    ).dt.strftime("%Y-%m-%dT%H:%M")
    normalized["Last Updated"] = normalized["Last Updated"].fillna("")
    return normalized


def normalize_yes_no(value: str) -> str:
    clean = str(value).strip().lower()
    if clean in {"yes", "y", "true", "1", "si", "sí"}:
        return "Yes"
    return "No"


def dashboard_summary(frame: pd.DataFrame) -> dict[str, object]:
    normalized = normalize_logistics_frame(frame)
    return {
        "total_records": int(len(normalized)),
        "urgent_records": int((normalized["Urgent"] == "Yes").sum()),
        "verified_records": int((normalized["Verified"] == "Yes").sum()),
        "owner_teams": int(normalized["Owner Team"].nunique()),
        "by_status": count_column(normalized, "Operational Status"),
        "by_pavilion": count_column(normalized, "Pavilion"),
        "by_implementation_level": count_column(normalized, "Implementation Level"),
    }


def count_column(frame: pd.DataFrame, column: str) -> dict[str, int]:
    counts = frame[column].replace("", "Unassigned").value_counts().sort_index()
    return {str(key): int(value) for key, value in counts.items()}
