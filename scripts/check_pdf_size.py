"""Guard: refuse to commit a deliverable PDF under the minimum size threshold."""
import sys
from pathlib import Path

MIN_BYTES = 50_000
_ROOT = Path(__file__).parent.parent
DELIVERABLE = _ROOT / "latex" / "output" / "uoh-sqak-article.pdf"


def main() -> int:
    if not DELIVERABLE.exists():
        print(f"WARNING: {DELIVERABLE} not found — skipping size check")
        return 0
    size = DELIVERABLE.stat().st_size
    if size < MIN_BYTES:
        print(
            f"FAIL: {DELIVERABLE} is only {size} bytes "
            f"(minimum {MIN_BYTES}). "
            "This looks like a test stub — refusing to commit."
        )
        return 1
    print(f"OK: {DELIVERABLE} is {size:,} bytes (≥{MIN_BYTES:,}) ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
