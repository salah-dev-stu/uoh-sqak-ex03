"""Version management — starts at 1.00, bump adds 0.01 per change."""

VERSION = "1.06"


def bump(version: str) -> str:
    """Increment patch: '1.00' → '1.01', '1.09' → '1.10'."""
    major, minor = version.split(".")
    return f"{major}.{int(minor) + 1:02d}"
