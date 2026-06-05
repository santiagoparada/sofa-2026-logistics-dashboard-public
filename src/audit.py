from __future__ import annotations

import pandas as pd


def data_quality_audit(frame: pd.DataFrame) -> dict[str, object]:
    required_columns = list(frame.columns)
    blank_counts = {
        column: int(frame[column].isna().sum() + (frame[column].astype(str).str.strip() == "").sum())
        for column in required_columns
    }
    return {
        "records": int(len(frame)),
        "columns": required_columns,
        "blank_counts": blank_counts,
        "has_urgent_workflow": bool((frame["Urgent"].astype(str) == "Yes").any()),
        "has_verification_workflow": bool((frame["Verified"].astype(str) == "Yes").any()),
        "public_data_source": "local synthetic CSV",
    }
