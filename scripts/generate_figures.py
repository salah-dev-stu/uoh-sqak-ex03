#!/usr/bin/env python3
"""CLI wrapper: generate all article figures via the pipeline module."""
from __future__ import annotations

from agent_article.tools.figure_generators import generate_all


def main() -> None:
    for path in generate_all():
        print(f"Generated: {path}")


if __name__ == "__main__":
    main()
