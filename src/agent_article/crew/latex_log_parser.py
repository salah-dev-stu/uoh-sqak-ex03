# src/agent_article/crew/latex_log_parser.py
"""Parse LuaLaTeX .log files into structured LatexError objects."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_UNDEFINED_CMD = re.compile(r"! Undefined control sequence")
_EXTRA_BRACE   = re.compile(r"! Too many \}'s")
_TRAILING_AMP  = re.compile(r"! (Misplaced \\noalign|Extra alignment tab)")
_LINE_REF      = re.compile(r"^l\.(\d+)")
_FILE_OPEN     = re.compile(r"\(\./?(chapters/[^\s)]+\.tex)")


@dataclass
class LatexError:
    file: str    # e.g. "chapters/ch04_production.tex"; "" if unknown
    line: int    # 0 if unknown
    message: str # raw "! ..." log line
    kind: str    # "undefined_cmd"|"extra_brace"|"trailing_amp"|"unknown"


def _classify(msg: str) -> str:
    if _UNDEFINED_CMD.search(msg):
        return "undefined_cmd"
    if _EXTRA_BRACE.search(msg):
        return "extra_brace"
    if _TRAILING_AMP.search(msg):
        return "trailing_amp"
    return "unknown"


def parse(log_path: Path) -> list[LatexError]:
    """Read a LuaLaTeX log file; return all fatal errors as LatexError objects.

    File attribution is best-effort and only tracks ``chapters/*.tex`` files.
    Errors in main.tex or package files may be attributed to the last opened
    chapter file or left as empty string.
    """
    if not log_path.exists():
        return []
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    errors: list[LatexError] = []
    current_file = ""
    for i, line in enumerate(lines):
        m = _FILE_OPEN.search(line)
        if m:
            current_file = m.group(1)
        elif line.strip() == ")":
            current_file = ""
        if not line.startswith("! "):
            continue
        err_line = 0
        for j in range(i + 1, min(i + 8, len(lines))):
            lm = _LINE_REF.match(lines[j])
            if lm:
                err_line = int(lm.group(1))
                break
        errors.append(LatexError(
            file=current_file, line=err_line, message=line, kind=_classify(line),
        ))
    return errors
