from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


class Config:
    DATA_SOURCE = os.getenv("DATA_SOURCE", "local_csv")
    SYNTHETIC_DATA_PATH = Path(
        os.getenv("SYNTHETIC_DATA_PATH", "data/synthetic/logistics_demo.csv")
    )
    REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "60"))
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG_ENABLED = os.getenv("DEBUG_ENABLED", "false").lower() == "true"

    @classmethod
    def data_path(cls) -> Path:
        path = cls.SYNTHETIC_DATA_PATH
        if not path.is_absolute():
            return BASE_DIR / path
        return path


config = Config()
