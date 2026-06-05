from __future__ import annotations

import pandas as pd

from config import config
from synthetic_data import COLUMNS


def load_logistics_data() -> pd.DataFrame:
    if config.DATA_SOURCE != "local_csv":
        raise ValueError("The public version only supports DATA_SOURCE=local_csv.")

    path = config.data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Synthetic dataset not found at {path}. Run python src/synthetic_data.py."
        )

    frame = pd.read_csv(path)
    missing = [column for column in COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Synthetic dataset is missing columns: {missing}")
    return frame[COLUMNS].fillna("")
