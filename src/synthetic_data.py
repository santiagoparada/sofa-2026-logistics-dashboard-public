from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "synthetic" / "logistics_demo.csv"
RECORD_COUNT = 920

COLUMNS = [
    "Pavilion",
    "Module",
    "Item",
    "Sub Item",
    "Requirement",
    "Technical Note",
    "Role Description",
    "Implementation Level",
    "Verified",
    "Urgent",
    "Last Updated",
    "Owner Team",
    "Estimated Resolution Time",
    "Operational Status",
]

PAVILIONS = [
    "SOFA 2026 Pavilion A - Immersive Experiences",
    "SOFA 2026 Pavilion B - Artist Alley",
    "SOFA 2026 Pavilion C - Esports Arena",
    "SOFA 2026 Pavilion D - Maker Lab",
    "SOFA 2026 Pavilion E - Retail Corridor",
    "SOFA 2026 Pavilion F - Food Court",
    "SOFA 2026 Pavilion G - Auditorium",
]

MODULES = [
    "Access Control",
    "Electrical Layout",
    "Furniture Deployment",
    "Signal Routing",
    "Safety Inspection",
    "Queue Management",
    "Branding Installation",
    "Inventory Handoff",
]

ITEMS = [
    "Floor plan validation",
    "Power drop mapping",
    "Table and chair setup",
    "Directional signage",
    "Cable protection",
    "Emergency corridor clearance",
    "Credential checkpoint",
    "Operational briefing",
    "Stand readiness",
    "Equipment reception",
]

SUB_ITEMS = [
    "",
    "",
    "Zone marker",
    "Back wall",
    "Main aisle",
    "Secondary aisle",
    "Storage corner",
    "Control point",
    "Public-facing desk",
]

REQUIREMENTS = [
    "Confirm implementation tracking milestone",
    "Validate logistics dashboard record consistency",
    "Resolve urgent requirement before pavilion handoff",
    "Document operational audit evidence",
    "Check verification workflow status",
    "Align role description with owner team",
    "Update technical note for field team",
    "Review sparse hierarchy assignment",
]

TECHNICAL_NOTES = [
    "Simulated note: pending site confirmation with operations lead.",
    "Simulated note: dependency requires module-level review.",
    "Simulated note: verification can proceed after handoff evidence.",
    "Simulated note: field observation added for audit traceability.",
    "Simulated note: no production source connected in this public dataset.",
]

ROLES = [
    "Pavilion coordinator",
    "Implementation tracker",
    "Verification reviewer",
    "Operational audit analyst",
    "Logistics support team",
    "Field operations lead",
]

LEVELS = ["Not Started", "Planned", "In Progress", "Implemented", "Verified"]
TEAMS = [
    "Operations Control",
    "Infrastructure",
    "Exhibitor Services",
    "Safety Review",
    "Technical Production",
    "Venue Logistics",
]
STATUSES = ["On Track", "At Risk", "Blocked", "Pending Verification", "Complete"]


def weighted_choice(values: list[str], weights: list[int]) -> str:
    return random.choices(values, weights=weights, k=1)[0]


def build_record(index: int, start_date: datetime) -> dict[str, str]:
    pavilion = PAVILIONS[index % len(PAVILIONS)]
    module = MODULES[(index // 7 + random.randint(0, 2)) % len(MODULES)]
    item = ITEMS[(index // 3 + random.randint(0, 4)) % len(ITEMS)]
    level = weighted_choice(LEVELS, [10, 18, 28, 26, 18])
    verified = "Yes" if level == "Verified" or random.random() < 0.18 else "No"
    urgent = "Yes" if random.random() < 0.22 else "No"
    status = weighted_choice(STATUSES, [34, 20, 9, 19, 18])

    if urgent == "Yes" and status == "Complete":
        status = "At Risk"
    if verified == "Yes":
        status = "Complete"

    updated = start_date + timedelta(
        days=random.randint(0, 75),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

    return {
        "Pavilion": pavilion,
        "Module": module if random.random() > 0.04 else "",
        "Item": item,
        "Sub Item": random.choice(SUB_ITEMS),
        "Requirement": random.choice(REQUIREMENTS),
        "Technical Note": random.choice(TECHNICAL_NOTES),
        "Role Description": random.choice(ROLES),
        "Implementation Level": level,
        "Verified": verified,
        "Urgent": urgent,
        "Last Updated": updated.isoformat(timespec="minutes"),
        "Owner Team": random.choice(TEAMS),
        "Estimated Resolution Time": f"{random.randint(2, 72)} hours",
        "Operational Status": status,
    }


def generate_records(record_count: int = RECORD_COUNT, seed: int = 2026) -> list[dict[str, str]]:
    random.seed(seed)
    start_date = datetime(2026, 4, 1, 8, 0)
    return [build_record(index, start_date) for index in range(record_count)]


def write_csv(path: Path = OUTPUT_PATH, record_count: int = RECORD_COUNT) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = generate_records(record_count=record_count)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(records)
    return path


if __name__ == "__main__":
    output = write_csv()
    print(f"Wrote synthetic SOFA 2026 logistics data to {output}")
