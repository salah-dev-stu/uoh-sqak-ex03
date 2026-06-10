# src/agent_article/crew/latex_patcher.py
"""Apply known-pattern regex fixes to .tex files in-place."""
from __future__ import annotations

import re
from pathlib import Path

from agent_article.crew.latex_log_parser import LatexError

_UNDEFINED_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\\textslash\b"), "/"),
    (re.compile(r"\\textplus\b"),  "+"),
    (re.compile(r"\\textminus\b"), "-"),
]
_TRAILING_AMP = re.compile(r"\s*&\s*(\\\\(?:\[\d*\.?\d*\w+\])?)")


def _fix_undefined_cmd(content: str) -> str:
    for pattern, replacement in _UNDEFINED_FIXES:
        content = pattern.sub(replacement, content)
    return content


def _fix_trailing_amp(content: str) -> str:
    return _TRAILING_AMP.sub(r" \1", content)


def _fix_extra_brace(content: str, line_no: int) -> str:
    if line_no < 1:
        return content
    file_lines = content.splitlines(keepends=True)
    idx = line_no - 1
    if 0 <= idx < len(file_lines):
        stripped = file_lines[idx].rstrip()
        if stripped.endswith("}"):
            file_lines[idx] = stripped[:-1] + "\n"
    return "".join(file_lines)


def apply(errors: list[LatexError], latex_dir: Path) -> int:
    """Apply fixes for known error kinds. Returns count of files modified."""
    by_file: dict[str, list[LatexError]] = {}
    for e in errors:
        if e.file:
            by_file.setdefault(e.file, []).append(e)
    modified = 0
    for rel_file, file_errors in by_file.items():
        tex_path = latex_dir / rel_file
        if not tex_path.exists():
            continue
        content = tex_path.read_text(encoding="utf-8")
        new_content = content
        for err in file_errors:
            if err.kind == "undefined_cmd":
                new_content = _fix_undefined_cmd(new_content)
            elif err.kind == "trailing_amp":
                new_content = _fix_trailing_amp(new_content)
            elif err.kind == "extra_brace":
                new_content = _fix_extra_brace(new_content, err.line)
        if new_content != content:
            tex_path.write_text(new_content, encoding="utf-8")
            modified += 1
    return modified
