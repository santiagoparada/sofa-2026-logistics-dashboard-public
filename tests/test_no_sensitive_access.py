from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}
ALLOWED_FILENAMES = {".env.example"}
TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".ipynb",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".toml",
    ".yml",
    ".yaml",
}


def public_files():
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def test_no_real_environment_files_are_committed():
    env_files = [
        path
        for path in ROOT.rglob(".env*")
        if path.name not in ALLOWED_FILENAMES and not any(part in IGNORED_DIRS for part in path.parts)
    ]
    assert env_files == []


def test_no_sensitive_access_patterns_are_committed():
    key = "private" + "_" + "key"
    account_email = "client" + "_" + "email"
    patterns = {
        "google_sheet_id_like": re.compile(
            r"\b(?=[0-9A-Za-z_-]{44,}\b)(?=[0-9A-Za-z_-]*\d)(?=[0-9A-Za-z_-]*[A-Z])[0-9A-Za-z_-]+\b"
        ),
        "google_drive_export_url": re.compile(r"https?://(?:docs|drive)\.google\.com/[^\s\"']+", re.I),
        "service_account_json": re.compile(r'"type"\s*:\s*"service_account"', re.I),
        "private_key": re.compile(key, re.I),
        "client_email": re.compile(account_email, re.I),
        "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "phone_number": re.compile(r"\b(?:\+\d{1,3}[\s.-]?)?(?:\d{3}[\s.-]?){2}\d{4}\b"),
        "render_url": re.compile(r"https?://[a-z0-9.-]*render\.com[^\s\"']*", re.I),
        "credential_variable": re.compile(r"(?:SECRET|TOKEN|PASSWORD|CREDENTIAL|API_KEY)\s*=", re.I),
    }

    allowed_terms = ("TRRNGR", "Click on Design S.A.S.", "SOFA 2026")
    violations = []

    for path in public_files():
        if path.name == "test_no_sensitive_access.py":
            continue
        text = read_text(path)
        for term in allowed_terms:
            text = text.replace(term, "")
        for name, pattern in patterns.items():
            for match in pattern.finditer(text):
                violations.append(f"{path.relative_to(ROOT)} matched {name}: {match.group(0)[:80]}")

    assert violations == []
