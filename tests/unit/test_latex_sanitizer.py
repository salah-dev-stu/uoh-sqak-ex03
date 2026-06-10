"""Unit tests for latex_sanitizer module."""
from __future__ import annotations

import pytest

from agent_article.crew.latex_sanitizer import (
    fix_table_overflow,
    is_valid_latex_content,
    sanitize,
)


# ---------------------------------------------------------------------------
# is_valid_latex_content
# ---------------------------------------------------------------------------

class TestIsValidLatexContent:
    def test_chapter_command_is_valid(self):
        assert is_valid_latex_content(r"\chapter{Intro}")

    def test_comment_then_chapter_is_valid(self):
        content = "% preamble\n\\chapter{Intro}"
        assert is_valid_latex_content(content)

    def test_bibtex_entry_is_valid(self):
        assert is_valid_latex_content("@article{key, author={A}, year={2024}}")

    def test_blank_lines_then_command_is_valid(self):
        assert is_valid_latex_content("\n\n\\section{X}")

    def test_prose_after_comment_is_invalid(self):
        content = (
            "% Chapter 5\n"
            "% Permission was not yet granted.\n"
            "\n"
            "Please approve the Write permission so the file is saved."
        )
        assert not is_valid_latex_content(content)

    def test_only_comments_is_invalid(self):
        assert not is_valid_latex_content("% a\n% b\n% c")

    def test_empty_string_is_invalid(self):
        assert not is_valid_latex_content("")

    def test_only_whitespace_is_invalid(self):
        assert not is_valid_latex_content("   \n   ")

    def test_plain_prose_no_comment_is_invalid(self):
        assert not is_valid_latex_content("Here is my explanation of the chapter.")


# ---------------------------------------------------------------------------
# fix_table_overflow
# ---------------------------------------------------------------------------

class TestFixTableOverflow:
    def test_removes_trailing_ampersand_before_newline(self):
        row = r"A & B & C & D & \\"
        fixed = fix_table_overflow(row)
        assert fixed == r"A & B & C & D \\"

    def test_removes_trailing_ampersand_before_newline_with_skip(self):
        row = r"A & B & C & D & \\[8pt]"
        fixed = fix_table_overflow(row)
        assert fixed == r"A & B & C & D \\[8pt]"

    def test_removes_trailing_ampersand_with_various_skips(self):
        row = r"A & B & \\[2ex]"
        fixed = fix_table_overflow(row)
        assert fixed == r"A & B \\[2ex]"

    def test_no_change_when_no_overflow(self):
        row = r"A & B & C \\"
        assert fix_table_overflow(row) == row

    def test_multiple_rows(self):
        content = "A & B & C & \\\\[8pt]\nX & Y & Z \\\\"
        fixed = fix_table_overflow(content)
        assert "A & B & C \\\\" in fixed
        assert "A & B & C & \\\\" not in fixed
        assert "X & Y & Z \\\\" in fixed

    def test_idempotent(self):
        row = r"A & B & C & \\[8pt]"
        once = fix_table_overflow(row)
        twice = fix_table_overflow(once)
        assert once == twice


# ---------------------------------------------------------------------------
# sanitize
# ---------------------------------------------------------------------------

class TestSanitize:
    def test_valid_latex_passes_through(self):
        content = "\\chapter{X}\n\nSome text."
        assert sanitize(content) == content

    def test_empty_returns_empty(self):
        assert sanitize("") == ""

    def test_whitespace_only_returns_empty(self):
        assert sanitize("  \n  ") == ""

    def test_prose_after_comment_returns_empty(self):
        content = (
            "% Chapter 5\n"
            "\n"
            "Please approve the Write permission."
        )
        assert sanitize(content) == ""

    def test_applies_table_overflow_fix(self):
        content = "\\chapter{X}\n\nA & B & C & D & \\\\[8pt]\n"
        result = sanitize(content)
        assert "A & B & C & D \\\\" in result
        assert "A & B & C & D & \\\\" not in result

    def test_bibtex_passes_through(self):
        bib = "@misc{Key2024,\n  author={A},\n  year={2024}\n}"
        assert sanitize(bib) == bib

    def test_valid_with_comment_header_passes(self):
        content = "% auto-generated\n\\chapter{Frameworks}\n\nText."
        assert sanitize(content) == content
