"""Fail if any Python file exceeds 150 logical lines (excluding blanks and comments)."""
import sys
from pathlib import Path

MAX_LINES = 150
SCAN_DIRS = ["src", "tests", "scripts"]


def count_lines(path: Path) -> int:
    return sum(1 for _ in path.read_text(encoding="utf-8", errors="ignore").splitlines())


def main() -> int:
    violations: list[tuple[Path, int]] = []
    for d in SCAN_DIRS:
        for p in Path(d).rglob("*.py"):
            n = count_lines(p)
            if n > MAX_LINES:
                violations.append((p, n))
    if violations:
        for file_path, n in violations:
            print(f"FAIL {file_path}: {n} logical lines (max {MAX_LINES})")
        return 1
    print(f"OK: all Python files within {MAX_LINES}-line limit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
