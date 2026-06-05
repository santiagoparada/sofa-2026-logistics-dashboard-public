from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from src.audit import data_quality_audit
from src.config import BASE_DIR, config
from src.data_loader import load_logistics_data
from src.transformations import dashboard_summary, normalize_logistics_frame


PUBLIC_DIR = BASE_DIR / "public"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)

    @app.get("/")
    def index():
        return send_from_directory(PUBLIC_DIR, "index.html")

    @app.get("/<path:asset>")
    def public_asset(asset: str):
        asset_path = PUBLIC_DIR / asset
        if asset_path.exists() and asset_path.is_file():
            return send_from_directory(PUBLIC_DIR, asset)
        return send_from_directory(PUBLIC_DIR, "index.html")

    @app.get("/api/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "data_source": config.DATA_SOURCE,
                "dataset": str(config.SYNTHETIC_DATA_PATH),
            }
        )

    @app.get("/api/records")
    def records():
        frame = normalize_logistics_frame(load_logistics_data())
        return jsonify(frame.to_dict(orient="records"))

    @app.get("/api/summary")
    def summary():
        return jsonify(dashboard_summary(load_logistics_data()))

    @app.get("/api/audit")
    def audit():
        frame = normalize_logistics_frame(load_logistics_data())
        return jsonify(data_quality_audit(frame))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=config.PORT,
        debug=config.DEBUG_ENABLED,
    )
