from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from transformations import dashboard_summary, normalize_logistics_frame


def test_normalize_yes_no_and_dates():
    frame = pd.DataFrame(
        [
            {
                "Pavilion": " SOFA 2026 Pavilion A ",
                "Module": "Access Control",
                "Item": "Checkpoint",
                "Sub Item": "",
                "Requirement": "Check verification workflow status",
                "Technical Note": "",
                "Role Description": "Implementation tracker",
                "Implementation Level": "Verified",
                "Verified": "true",
                "Urgent": "0",
                "Last Updated": "2026-04-02 09:30:00",
                "Owner Team": "Operations Control",
                "Estimated Resolution Time": "8 hours",
                "Operational Status": "Complete",
            }
        ]
    )

    normalized = normalize_logistics_frame(frame)
    assert normalized.loc[0, "Pavilion"] == "SOFA 2026 Pavilion A"
    assert normalized.loc[0, "Verified"] == "Yes"
    assert normalized.loc[0, "Urgent"] == "No"
    assert normalized.loc[0, "Last Updated"] == "2026-04-02T09:30"


def test_dashboard_summary_counts_workflows():
    frame = pd.DataFrame(
        [
            {"Pavilion": "A", "Operational Status": "Complete", "Verified": "Yes", "Urgent": "No", "Owner Team": "Ops", "Implementation Level": "Verified", "Last Updated": ""},
            {"Pavilion": "A", "Operational Status": "At Risk", "Verified": "No", "Urgent": "Yes", "Owner Team": "Tech", "Implementation Level": "In Progress", "Last Updated": ""},
            {"Pavilion": "B", "Operational Status": "At Risk", "Verified": "No", "Urgent": "Yes", "Owner Team": "Ops", "Implementation Level": "Planned", "Last Updated": ""},
        ]
    )

    summary = dashboard_summary(frame)
    assert summary["total_records"] == 3
    assert summary["urgent_records"] == 2
    assert summary["verified_records"] == 1
    assert summary["owner_teams"] == 2
    assert summary["by_status"]["At Risk"] == 2
