# Post-Pipeline LaTeX Repair Loop — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After the CrewAI pipeline generates chapters, automatically compile, patch known LaTeX errors with regex, re-prompt the LLM for unknown errors, and retry up to 3 times before giving up.

**Architecture:** Three new files under `src/agent_article/crew/` (parser, patcher, repair agent) plus a `_compile_with_repair()` method in `article_crew.py` that replaces `_compile_pdf()`. Known-pattern fixes are free (no LLM call); agent re-prompt only fires from attempt 2 onwards for unrecognised errors.

**Tech Stack:** Python stdlib (`re`, `pathlib`, `dataclasses`), `pytest` + `unittest.mock`, existing `ClaudeCLILLM`, existing `LaTeXCompileTool`.

---

## File Map

| Action | Path |
|--------|------|
| Create | `src/agent_article/crew/latex_log_parser.py` |
| Create | `src/agent_article/crew/latex_patcher.py` |
| Create | `src/agent_article/crew/latex_repair_agent.py` |
| Modify | `src/agent_article/crew/article_crew.py` |
| Modify | `config/latex.json` |
| Create | `tests/unit/test_latex_log_parser.py` |
| Create | `tests/unit/test_latex_patcher.py` |
| Create | `tests/unit/test_latex_repair_agent.py` |
| Create | `tests/unit/test_article_crew_repair.py` |
| Modify | `tests/unit/test_crew.py` (update `_compile_pdf` → `_compile_with_repair`) |

---

## Task 1: `latex_log_parser.py` — LatexError dataclass + parse()

**Files:**
- Create: `tests/unit/test_latex_log_parser.py`
- Create: `src/agent_article/crew/latex_log_parser.py`

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run tests — verify they fail with ImportError**

```bash
uv run pytest tests/unit/test_latex_log_parser.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError: No module named 'agent_article.crew.latex_log_parser'`

- [ ] **Step 3: Implement `latex_log_parser.py`**

```python
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
    """Read a LuaLaTeX log file; return all fatal errors as LatexError objects."""
    if not log_path.exists():
        return []
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    errors: list[LatexError] = []
    current_file = ""
    for i, line in enumerate(lines):
        m = _FILE_OPEN.search(line)
        if m:
            current_file = m.group(1)
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
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
uv run pytest tests/unit/test_latex_log_parser.py -v
```

Expected: all 8 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/crew/latex_log_parser.py tests/unit/test_latex_log_parser.py
git commit -m "feat(crew): add latex_log_parser — parse LuaLaTeX log into LatexError list"
```

---

## Task 2: `latex_patcher.py` — known-pattern regex fixes

**Files:**
- Create: `tests/unit/test_latex_patcher.py`
- Create: `src/agent_article/crew/latex_patcher.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_latex_patcher.py
"""Tests for crew/latex_patcher.py — apply known-pattern fixes to .tex files."""
from pathlib import Path
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
    assert "1+ 2" == tex.read_text(encoding="utf-8")


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
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
uv run pytest tests/unit/test_latex_patcher.py -v 2>&1 | head -10
```

Expected: `ModuleNotFoundError: No module named 'agent_article.crew.latex_patcher'`

- [ ] **Step 3: Implement `latex_patcher.py`**

```python
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
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
uv run pytest tests/unit/test_latex_patcher.py -v
```

Expected: all 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/crew/latex_patcher.py tests/unit/test_latex_patcher.py
git commit -m "feat(crew): add latex_patcher — regex fixes for undefined_cmd, trailing_amp, extra_brace"
```

---

## Task 3: `latex_repair_agent.py` — LLM re-prompt for unknown errors

**Files:**
- Create: `tests/unit/test_latex_repair_agent.py`
- Create: `src/agent_article/crew/latex_repair_agent.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_latex_repair_agent.py
"""Tests for crew/latex_repair_agent.py — re-prompt ClaudeCLILLM for unknown errors."""
from unittest.mock import MagicMock, patch

from agent_article.crew.latex_log_parser import LatexError


def _unknown(file="chapters/ch01.tex", line=10):
    return LatexError(file=file, line=line,
                      message="! Some weird error.", kind="unknown")


def test_repair_calls_llm_and_writes_file(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    tex = chapters / "ch01.tex"
    tex.write_text("\\chapter{Hello}\nbroken content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.return_value = "\\chapter{Hello}\nfixed content"

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([_unknown()], tmp_path)

    assert mock_llm.call.called
    prompt = mock_llm.call.call_args[0][0]
    assert "! Some weird error." in prompt
    assert "broken content" in prompt
    assert tex.read_text(encoding="utf-8") == "\\chapter{Hello}\nfixed content"


def test_repair_skips_known_error_kinds(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    known = LatexError(file="chapters/ch04.tex", line=1,
                       message="! Undefined control sequence", kind="undefined_cmd")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([known], tmp_path)
    assert not mock_llm.call.called


def test_repair_skips_missing_file(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    err = LatexError(file="chapters/nonexistent.tex", line=1,
                     message="! error", kind="unknown")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([err], tmp_path)
    assert not mock_llm.call.called


def test_repair_skips_empty_file_field(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    err = LatexError(file="", line=0, message="! error", kind="unknown")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([err], tmp_path)
    assert not mock_llm.call.called


def test_repair_dedupes_per_file_one_llm_call(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    tex = chapters / "ch01.tex"
    tex.write_text("content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.return_value = "fixed"
    errors = [_unknown(), _unknown()]  # two errors, same file

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair(errors, tmp_path)

    assert mock_llm.call.call_count == 1


def test_repair_tolerates_llm_exception(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    (chapters / "ch01.tex").write_text("content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.side_effect = RuntimeError("LLM unavailable")

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([_unknown()], tmp_path)  # must not raise
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
uv run pytest tests/unit/test_latex_repair_agent.py -v 2>&1 | head -10
```

Expected: `ModuleNotFoundError: No module named 'agent_article.crew.latex_repair_agent'`

- [ ] **Step 3: Implement `latex_repair_agent.py`**

```python
# src/agent_article/crew/latex_repair_agent.py
"""Re-prompt ClaudeCLILLM with error context for unknown LaTeX compile errors."""
from __future__ import annotations

from pathlib import Path

from agent_article.crew.latex_log_parser import LatexError
from agent_article.shared.claude_cli_llm import ClaudeCLILLM
from agent_article.shared.logging_fifo import StructuredLogger

_log = StructuredLogger("latex_repair")

_PROMPT = """\
You are a LaTeX expert. The following file failed to compile with this error:

File: {file}
Line: {line}
Error: {message}

Here is the full file content:
{content}

Fix ONLY the error above. Return the complete corrected LaTeX file.
Do NOT add comments. Do NOT change any other content.\
"""


def repair(errors: list[LatexError], latex_dir: Path) -> None:
    """Re-prompt LLM for each unique file with unknown errors; overwrite file."""
    unknown = [e for e in errors if e.kind == "unknown" and e.file]
    if not unknown:
        return
    llm = ClaudeCLILLM()
    seen: set[str] = set()
    for err in unknown:
        if err.file in seen:
            continue
        seen.add(err.file)
        tex_path = latex_dir / err.file
        if not tex_path.exists():
            _log.warning(f"repair: file not found: {tex_path}")
            continue
        content = tex_path.read_text(encoding="utf-8")
        prompt = _PROMPT.format(
            file=err.file, line=err.line,
            message=err.message, content=content,
        )
        _log.info(f"repair: re-prompting for {err.file}: {err.message[:80]}")
        try:
            fixed = llm.call(prompt)
            if fixed.strip():
                tex_path.write_text(fixed.strip(), encoding="utf-8")
                _log.info(f"repair: wrote fix to {err.file}")
        except Exception as exc:
            _log.error(f"repair: LLM failed for {err.file}: {exc}")
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
uv run pytest tests/unit/test_latex_repair_agent.py -v
```

Expected: all 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/crew/latex_repair_agent.py tests/unit/test_latex_repair_agent.py
git commit -m "feat(crew): add latex_repair_agent — re-prompt LLM for unknown LaTeX errors"
```

---

## Task 4: `_compile_with_repair()` in `article_crew.py`

**Files:**
- Create: `tests/unit/test_article_crew_repair.py`
- Modify: `src/agent_article/crew/article_crew.py` (replace `_compile_pdf` with `_compile_with_repair`)
- Modify: `tests/unit/test_crew.py` (update mock target from `_compile_pdf` to `_compile_with_repair`)

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_article_crew_repair.py
"""Tests for ArticleCrew._compile_with_repair() — 3-attempt repair loop."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


def _mk_cfg(tmp_path):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    for name, data in [
        ("setup", {"version": "1.01", "workspace_dir": str(tmp_path / "ws"),
                   "output_filename": "test.pdf"}),
        ("latex", {"version": "1.00", "compiler": "lualatex", "biber": "biber",
                   "passes": 4, "main_file": "latex/main.tex",
                   "max_repair_attempts": 3}),
        ("rate_limits", {"version": "1.01", "services": {}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
        ("agents", {"version": "1.00", "agents": {}}),
        ("tasks", {"version": "1.03", "tasks": {}}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    cfg_mod._CONFIG_DIR = cfg_dir
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def setup_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def teardown_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def test_succeeds_on_first_attempt(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")

    mock_tool = MagicMock()
    mock_tool.run.return_value = fake_pdf

    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool):
        result = crew._compile_with_repair()

    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 1


def test_retries_after_known_error_and_succeeds(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")

    mock_tool = MagicMock()
    mock_tool.run.side_effect = [RuntimeError("fail1"), fake_pdf]

    fake_errors = [LatexError(
        file="chapters/ch04.tex", line=10,
        message="! Undefined control sequence.", kind="undefined_cmd",
    )]

    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=1) as mock_patch, \
         patch("agent_article.crew.latex_repair_agent.repair") as mock_repair:
        result = crew._compile_with_repair()

    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 2
    assert mock_patch.call_count == 1
    assert mock_repair.call_count == 0  # agent repair not called for known errors


def test_calls_agent_repair_on_attempt_2_unknown(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")

    mock_tool = MagicMock()
    mock_tool.run.side_effect = [RuntimeError("fail1"), RuntimeError("fail2"), fake_pdf]

    fake_errors = [LatexError(
        file="chapters/ch01.tex", line=5,
        message="! Weird unknown error.", kind="unknown",
    )]

    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=0), \
         patch("agent_article.crew.latex_repair_agent.repair") as mock_repair:
        result = crew._compile_with_repair()

    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 3
    assert mock_repair.call_count == 1  # fired on attempt 2


def test_returns_none_after_all_attempts_exhausted(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")

    mock_tool = MagicMock()
    mock_tool.run.side_effect = RuntimeError("always fail")

    fake_errors = [LatexError(
        file="chapters/ch01.tex", line=5,
        message="! Unknown.", kind="unknown",
    )]

    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=0), \
         patch("agent_article.crew.latex_repair_agent.repair"):
        result = crew._compile_with_repair()

    assert result is None
    assert mock_tool.run.call_count == 3


def test_stops_early_when_log_has_no_errors(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew
    crew = ArticleCrew("Test")

    mock_tool = MagicMock()
    mock_tool.run.side_effect = RuntimeError("fail with empty log")

    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse", return_value=[]):
        result = crew._compile_with_repair()

    assert result is None
    assert mock_tool.run.call_count == 1  # gave up after first fail with no log errors
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
uv run pytest tests/unit/test_article_crew_repair.py -v 2>&1 | head -15
```

Expected: tests collect but fail because `_compile_with_repair` doesn't exist yet (AttributeError)

- [ ] **Step 3: Replace `_compile_pdf` with `_compile_with_repair` in `article_crew.py`**

In `src/agent_article/crew/article_crew.py`:

Replace lines 78 and 101–111 (the call and the method). Final `article_crew.py` looks like:

```python
# src/agent_article/crew/article_crew.py
"""Article-writing CrewAI crew — sequential 3-agent phase + parallel LaTeX phase."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from crewai import Crew, Process

from agent_article.agents.editor_agent import EditorAgent
from agent_article.agents.researcher_agent import ResearcherAgent
from agent_article.agents.writer_agent import WriterAgent
from agent_article.crew.latex_runner import run_latex_phase_parallel
from agent_article.shared.config import cfg
from agent_article.shared.logging_fifo import StructuredLogger
from agent_article.tasks.article_tasks import (
    build_edit_task,
    build_latex_tasks,
    build_research_task,
    build_write_task,
)

_log = StructuredLogger("crew")


@dataclass
class CrewResult:
    """
    Input:  Crew kickoff result
    Output: pdf_path str, raw_output str
    Setup:  auto-populated by ArticleCrew.run()
    """

    pdf_path: str = ""
    raw_output: str = ""
    success: bool = False
    errors: list[str] = field(default_factory=list)


class ArticleCrew:
    """
    Input:  topic str
    Output: CrewResult with pdf_path
    Setup:  agents/tasks built lazily on run()
    """

    def __init__(self, topic: str) -> None:
        self._topic = topic
        self._workspace = Path(cfg("setup", "workspace_dir", "workspace"))
        self._workspace.mkdir(parents=True, exist_ok=True)

    def run(self) -> CrewResult:
        """Execute full pipeline: sequential 3-agent phase + parallel LaTeX phase."""
        _log.info(f"Starting crew run for topic={self._topic!r}")
        result = CrewResult()
        try:
            researcher = ResearcherAgent()
            writer = WriterAgent()
            editor = EditorAgent()

            t_research = build_research_task(researcher, self._topic)
            t_write = build_write_task(writer, self._topic, [t_research])
            t_edit = build_edit_task(editor, [t_write])

            seq_crew = Crew(
                agents=[researcher.build(), writer.build(), editor.build()],
                tasks=[t_research, t_write, t_edit],
                process=Process.sequential,
                verbose=True,
                respect_context_window=True,
            )
            output = seq_crew.kickoff()
            result.raw_output = str(output)

            latex_tasks = build_latex_tasks([t_edit])
            run_latex_phase_parallel(latex_tasks)
            self._generate_figures()

            compiled = self._compile_with_repair()
            output_filename = cfg("setup", "output_filename", "uoh-sqak-article.pdf")
            pdf_path = Path("latex/output") / output_filename
            if compiled:
                import shutil
                shutil.copy2(compiled, pdf_path)
                result.success = True
            result.pdf_path = str(pdf_path)
            _log.info(f"Crew run complete: pdf_path={result.pdf_path}")
        except Exception as exc:
            result.errors.append(str(exc))
            _log.error(f"Crew run failed: {exc}")
        return result

    def _generate_figures(self) -> None:
        """Generate all pipeline figures into latex/figures/ before compilation."""
        from agent_article.tools.figure_generators import generate_all
        try:
            paths = generate_all()
            _log.info(f"Generated {len(paths)} figures: {paths}")
        except Exception as exc:
            _log.error(f"Figure generation failed (non-fatal): {exc}")

    def _compile_with_repair(self) -> Path | None:
        """Compile LaTeX with up to max_repair_attempts; patch/re-prompt on failure."""
        from agent_article.crew.latex_log_parser import parse as parse_log
        from agent_article.crew.latex_patcher import apply as patch_errors
        from agent_article.crew.latex_repair_agent import repair as repair_errors
        from agent_article.tools.latex_compile import LaTeXCompileTool

        latex_dir = Path(cfg("latex", "main_file", "latex/main.tex")).parent
        max_attempts = cfg("latex", "max_repair_attempts", 3)
        log_path = latex_dir / "output" / "main.log"
        tool = LaTeXCompileTool()

        for attempt in range(1, max_attempts + 1):
            try:
                pdf = tool.run("main.tex")
                _log.info(f"LaTeX compile succeeded on attempt {attempt}: {pdf}")
                return Path(pdf)
            except Exception as exc:
                _log.warning(f"Compile attempt {attempt}/{max_attempts} failed: {exc}")
                if attempt == max_attempts:
                    break
                errors = parse_log(log_path)
                if not errors:
                    _log.error("No parseable errors in log; giving up")
                    break
                known = [e for e in errors if e.kind != "unknown"]
                if known:
                    n = patch_errors(known, latex_dir)
                    _log.info(f"Patched {n} file(s) with {len(known)} known fix(es)")
                if attempt >= 2:
                    unknown_errs = [e for e in errors if e.kind == "unknown"]
                    if unknown_errs:
                        repair_errors(unknown_errs, latex_dir)

        _log.error(f"Repair exhausted after {max_attempts} attempts")
        return None
```

- [ ] **Step 4: Update `test_crew.py` — rename `_compile_pdf` → `_compile_with_repair`**

In `tests/unit/test_crew.py`, change line 75:

```python
# Before:
patch.object(crew, "_compile_pdf", return_value=fake_pdf):
# After:
patch.object(crew, "_compile_with_repair", return_value=fake_pdf):
```

- [ ] **Step 5: Run all affected tests — verify they pass**

```bash
uv run pytest tests/unit/test_article_crew_repair.py tests/unit/test_crew.py -v
```

Expected: all tests PASS

- [ ] **Step 6: Run full suite to check no regressions**

```bash
uv run pytest tests/unit/ -v 2>&1 | tail -20
```

Expected: all tests PASS (no failures)

- [ ] **Step 7: Commit**

```bash
git add src/agent_article/crew/article_crew.py \
        tests/unit/test_article_crew_repair.py \
        tests/unit/test_crew.py
git commit -m "feat(crew): replace _compile_pdf with _compile_with_repair — 3-attempt hybrid repair loop"
```

---

## Task 5: Config + TODO additions

**Files:**
- Modify: `config/latex.json`
- Modify: `docs/TODO.md`

- [ ] **Step 1: Add `max_repair_attempts` to `config/latex.json`**

Open `config/latex.json` and add `"max_repair_attempts": 3` after `"bidi_chapter"`:

```json
{
  "version": "1.01",
  "compiler": "/usr/local/texlive/2025/bin/universal-darwin/lualatex",
  "biber": "biber",
  "passes": 4,
  "bib_style": "numeric-comp",
  "chapter_list": [
    "ch01_introduction",
    "ch02_architectures",
    "ch03_frameworks",
    "ch04_production",
    "ch05_bidi",
    "ch06_casestudy"
  ],
  "output_dir": "latex/output",
  "main_file": "latex/main.tex",
  "target_pages": 15,
  "language": "english",
  "bidi_chapter": "ch05_bidi",
  "max_repair_attempts": 3
}
```

- [ ] **Step 2: Run the full test suite one final time**

```bash
uv run pytest tests/unit/ -v --tb=short 2>&1 | tail -30
```

Expected: all tests PASS

- [ ] **Step 3: Add tasks to `docs/TODO.md`**

Append the following block under a new section in `docs/TODO.md`:

```markdown
## Post-Pipeline LaTeX Repair Loop

- [x] Design post-pipeline compile-and-fix loop (brainstorming session 2026-06-10)
- [ ] Implement latex_log_parser.py — LatexError dataclass + parse()
- [ ] Implement latex_patcher.py — known-pattern regex fixes
- [ ] Implement latex_repair_agent.py — LLM re-prompt for unknown errors
- [ ] Replace _compile_pdf with _compile_with_repair in article_crew.py
- [ ] Add max_repair_attempts to config/latex.json
- [ ] Write test_latex_log_parser.py (8 tests)
- [ ] Write test_latex_patcher.py (9 tests)
- [ ] Write test_latex_repair_agent.py (6 tests)
- [ ] Write test_article_crew_repair.py (5 tests)
- [ ] Update test_crew.py mock target _compile_pdf → _compile_with_repair
- [ ] Verify full test suite passes after implementation
- [ ] Run end-to-end pipeline to confirm Success: True with repair loop active
```

- [ ] **Step 4: Commit everything**

```bash
git add config/latex.json docs/TODO.md
git commit -m "chore: add max_repair_attempts config + TODO tasks for repair loop"
```
