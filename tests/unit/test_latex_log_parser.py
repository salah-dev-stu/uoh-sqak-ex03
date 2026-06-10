# tests/unit/test_latex_log_parser.py
"""Tests for crew/latex_log_parser.py — LatexError + parse()."""
from pathlib import Path


def test_parse_returns_empty_for_clean_log(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text("Normal compilation output\nno errors here", encoding="utf-8")
    assert parse(log) == []


def test_parse_returns_empty_for_missing_log(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    assert parse(tmp_path / "nonexistent.log") == []


def test_parse_undefined_cmd(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch04_production.tex\n"
        "! Undefined control sequence.\n"
        "l.114 A\\textslash B\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 1
    e = errors[0]
    assert e.kind == "undefined_cmd"
    assert e.line == 114
    assert "ch04_production.tex" in e.file


def test_parse_extra_brace(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch06_casestudy.tex\n"
        "! Too many }'s.\n"
        "l.17 }}\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 1
    assert errors[0].kind == "extra_brace"
    assert errors[0].line == 17


def test_parse_trailing_amp(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch02_architectures.tex\n"
        "! Extra alignment tab has been changed to \\cr.\n"
        "l.45 foo & bar &\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 1
    assert errors[0].kind == "trailing_amp"


def test_parse_misplaced_noalign(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch03_frameworks.tex\n"
        "! Misplaced \\noalign.\n"
        "l.22 \\hline\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 1
    assert errors[0].kind == "trailing_amp"


def test_parse_unknown_error(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch01_introduction.tex\n"
        "! Some completely new weird error.\n"
        "l.22 something\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 1
    assert errors[0].kind == "unknown"
    assert errors[0].line == 22


def test_parse_multiple_errors(tmp_path):
    from agent_article.crew.latex_log_parser import parse
    log = tmp_path / "main.log"
    log.write_text(
        "(./chapters/ch04_production.tex\n"
        "! Undefined control sequence.\n"
        "l.10 \\textslash\n"
        "! Too many }'s.\n"
        "l.20 }}\n",
        encoding="utf-8",
    )
    errors = parse(log)
    assert len(errors) == 2
    assert errors[0].kind == "undefined_cmd"
    assert errors[1].kind == "extra_brace"
