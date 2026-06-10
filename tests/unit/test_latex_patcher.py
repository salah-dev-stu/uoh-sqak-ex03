# tests/unit/test_latex_patcher.py
"""Tests for crew/latex_patcher.py — apply known-pattern fixes to .tex files."""
from agent_article.crew.latex_log_parser import LatexError


def _err(kind, file="chapters/ch04.tex", line=1):
    return LatexError(file=file, line=line, message="! error", kind=kind)


def _write(tmp_path, filename, content):
    p = tmp_path / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def test_fixes_textslash(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch04.tex", "A\\textslash B testing")
    apply([_err("undefined_cmd")], tmp_path)
    assert tex.read_text(encoding="utf-8") == "A/ B testing"


def test_fixes_textplus(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch04.tex", "1\\textplus 2")
    apply([_err("undefined_cmd")], tmp_path)
    assert "\\textplus" not in tex.read_text(encoding="utf-8")
    assert tex.read_text(encoding="utf-8") == "1+ 2"


def test_fixes_textminus(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch04.tex", "a \\textminus b")
    apply([_err("undefined_cmd")], tmp_path)
    assert "\\textminus" not in tex.read_text(encoding="utf-8")


def test_fixes_trailing_amp(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch04.tex", "a & b & c & \\\\[4pt]\n")
    apply([_err("trailing_amp")], tmp_path)
    content = tex.read_text(encoding="utf-8")
    assert "& \\\\" not in content
    assert "\\\\" in content


def test_fixes_extra_brace_at_line(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch06.tex",
                 "line1\n\\texttt{foo}}\nline3\n")
    err = LatexError(file="chapters/ch06.tex", line=2,
                     message="! Too many }'s", kind="extra_brace")
    apply([err], tmp_path)
    lines = tex.read_text(encoding="utf-8").splitlines()
    assert lines[1] == "\\texttt{foo}"


def test_unknown_kind_not_touched(tmp_path):
    from agent_article.crew.latex_patcher import apply
    original = "some weird content"
    tex = _write(tmp_path, "chapters/ch01.tex", original)
    apply([_err("unknown", file="chapters/ch01.tex")], tmp_path)
    assert tex.read_text(encoding="utf-8") == original


def test_skip_missing_file(tmp_path):
    from agent_article.crew.latex_patcher import apply
    count = apply([_err("undefined_cmd", file="chapters/missing.tex")], tmp_path)
    assert count == 0


def test_returns_count_of_modified_files(tmp_path):
    from agent_article.crew.latex_patcher import apply
    _write(tmp_path, "chapters/ch04.tex", "\\textslash")
    count = apply([_err("undefined_cmd")], tmp_path)
    assert count == 1


def test_deduplicates_multiple_errors_same_file(tmp_path):
    from agent_article.crew.latex_patcher import apply
    tex = _write(tmp_path, "chapters/ch04.tex", "\\textslash and \\textplus")
    errors = [_err("undefined_cmd"), _err("undefined_cmd")]
    apply(errors, tmp_path)
    content = tex.read_text(encoding="utf-8")
    assert "\\textslash" not in content
    assert "\\textplus" not in content
