"""Post-processing sanitizer for agent-generated LaTeX/BibTeX output."""
from __future__ import annotations

import re


def is_valid_latex_content(content: str) -> bool:
    """
    Return True iff the first non-comment, non-blank line is a LaTeX or BibTeX command.

    Rejects "prose disguised as LaTeX" where an agent wraps an explanation in
    % comments then writes plain English below — clean_latex accepts the % as a
    valid start but the body is not compilable.
    """
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        return stripped.startswith("\\") or stripped.startswith("@")
    return False  # only blanks/comments — nothing real


def fix_table_overflow(content: str) -> str:
    """Remove a spurious trailing & before \\\\ in table rows.

    Agents sometimes emit one extra column: "a & b & c & d & \\\\[8pt]"
    in a 4-column table (which needs only 3 &s).  Strip the last lone & \\\\
    so LaTeX doesn't reject the row.
    """
    return re.sub(r"\s*&\s*(\\\\(?:\[\d*\.?\d*\w+\])?)", r" \1", content)


def sanitize(content: str) -> str:
    """Apply all auto-fixes; return fixed content or '' if fundamentally invalid.

    Pipeline: fix_table_overflow → validate with is_valid_latex_content.
    Returning '' signals the caller to retry the LLM invocation.
    """
    if not content.strip():
        return ""
    content = fix_table_overflow(content)
    if not is_valid_latex_content(content):
        return ""
    return content
