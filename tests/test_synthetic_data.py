from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from synthetic_data import COLUMNS, generate_records


def test_generator_creates_expected_public_shape():
    records = generate_records(record_count=900)
    assert len(records) == 900
    assert set(records[0]) == set(COLUMNS)
    assert 800 <= len(records) <= 1000


def test_generator_preserves_structural_complexity():
    records = generate_records(record_count=920)
    pavilions = {record["Pavilion"] for record in records}
    modules = {record["Module"] for record in records if record["Module"]}
    urgent = {record["Urgent"] for record in records}
    verified = {record["Verified"] for record in records}
    levels = {record["Implementation Level"] for record in records}
    teams = {record["Owner Team"] for record in records}

    assert len(pavilions) >= 5
    assert len(modules) >= 6
    assert urgent == {"No", "Yes"}
    assert verified == {"No", "Yes"}
    assert len(levels) >= 4
    assert len(teams) >= 4
    assert any(record["Sub Item"] == "" for record in records)
