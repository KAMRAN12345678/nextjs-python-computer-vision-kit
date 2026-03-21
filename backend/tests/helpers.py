from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def fixture_path(name: str) -> Path:
    return FIXTURE_DIR / name


def fixture_bytes(name: str) -> bytes:
    return fixture_path(name).read_bytes()
