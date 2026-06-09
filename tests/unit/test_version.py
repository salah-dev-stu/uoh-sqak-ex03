"""Tests for shared/version.py."""
from agent_article.shared.version import VERSION, bump


def test_version_format() -> None:
    parts = VERSION.split(".")
    assert len(parts) == 2
    assert parts[0].isdigit()
    assert parts[1].isdigit()


def test_version_starts_at_1_00() -> None:
    assert VERSION == "1.06"


def test_bump_increments_patch() -> None:
    assert bump("1.00") == "1.01"


def test_bump_increments_past_9() -> None:
    assert bump("1.09") == "1.10"


def test_bump_preserves_major() -> None:
    assert bump("2.05").startswith("2.")


def test_bump_large_minor() -> None:
    assert bump("1.99") == "1.100"
