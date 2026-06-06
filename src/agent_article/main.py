"""Entry point — delegates to TUI or direct CLI invocation."""
from __future__ import annotations
import sys


def main() -> int:
    """Main entry point — starts the terminal UI."""
    from agent_article.menu.tui import run_tui
    run_tui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
