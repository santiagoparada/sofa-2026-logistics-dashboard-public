# Architecture

The public SOFA 2026 logistics dashboard is intentionally isolated from production systems.

## Data Flow

1. `src/synthetic_data.py` generates a local synthetic dataset.
2. `src/data_loader.py` reads `data/synthetic/logistics_demo.csv`.
3. `src/transformations.py` normalizes records and computes summary metrics.
4. `src/audit.py` checks dataset quality and public-release safety signals.
5. `src/app.py` exposes a Flask API and serves the static dashboard from `public/`.

## Public Boundary

The application has no Google Sheets integration, no database connector, no credential loader, and no production deployment configuration. The only supported data source is the local synthetic CSV.
