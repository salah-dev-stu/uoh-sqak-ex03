# Post-Pipeline LaTeX Compile-and-Fix Loop — Design Spec

**Date:** 2026-06-10  
**Status:** Approved  
**Approach:** Hybrid — known-pattern regex patch first, agent re-prompt fallback for unknowns

---

## Goal

After the CrewAI pipeline generates all `.tex` chapters, automatically compile the LaTeX project, detect errors, apply cheap regex patches for known error patterns, and fall back to an agent re-prompt for unrecognised errors. Retry up to 3 times. Return `Success: True` if any attempt succeeds; `Success: False` only if all 3 attempts fail.

---

## Architecture

Three new files under `src/agent_article/crew/`, all ≤ 150 lines:

| File | Responsibility |
|---|---|
| `latex_log_parser.py` | Reads `latex/output/main.log`, returns `list[LatexError]` |
| `latex_patcher.py` | Applies regex substitutions for known error kinds to `.tex` files in-place |
| `latex_repair_agent.py` | Re-prompts `ClaudeCLILLM` with error context for unknown errors; writes corrected file |

One method modified in `src/agent_article/crew/article_crew.py`:

- `_compile_pdf()` → replaced by `_compile_with_repair()` which orchestrates the 3-attempt loop

Config key `latex.max_repair_attempts` (default `3`) lives in `config/setup.json`.

---

## Data Structures

```python
@dataclass
class LatexError:
    file: str    # relative path, e.g. "chapters/ch04_production.tex"; "" if unknown
    line: int    # 0 if unknown
    message: str # raw log line
    kind: str    # "undefined_cmd" | "extra_brace" | "trailing_amp" | "unknown"
```

---

## Data Flow

```
_compile_with_repair(max_attempts=3)
  │
  ├─ attempt 1
  │   ├─ LaTeXCompileTool.run("main.tex")  → SUCCESS → return Path(pdf)
  │   └─ FAIL
  │       ├─ parse main.log → list[LatexError]
  │       ├─ known kinds → latex_patcher.apply(errors, latex_dir)
  │       └─ unknown kinds → carried to attempt 2
  │
  ├─ attempt 2
  │   ├─ LaTeXCompileTool.run("main.tex")  → SUCCESS → return Path(pdf)
  │   └─ FAIL
  │       ├─ parse main.log → list[LatexError]
  │       ├─ known kinds → patch
  │       └─ unknown kinds → latex_repair_agent.repair(errors, latex_dir)
  │
  └─ attempt 3
      ├─ LaTeXCompileTool.run("main.tex")  → SUCCESS → return Path(pdf)
      └─ FAIL → log "repair exhausted after 3 attempts" → return None
```

---

## Known-Pattern Table (`latex_patcher.py`)

| kind | Log signal | Fix applied |
|---|---|---|
| `undefined_cmd` | `Undefined control sequence.*\\textslash` | `\textslash` → `/` |
| `undefined_cmd` | `Undefined control sequence.*\\textplus` | `\textplus` → `+` |
| `undefined_cmd` | `Undefined control sequence.*\\textminus` | `\textminus` → `-` |
| `extra_brace` | `Too many }'s` | Remove extra `}` at reported line |
| `trailing_amp` | `Misplaced \\noalign\|Extra alignment tab` | Strip trailing `&` before `\\` in table rows |

The table is a list of dicts in `latex_patcher.py` (not in a separate config file — these are code-level invariants, not operator settings).

---

## Log Parser (`latex_log_parser.py`)

Reads the log file line-by-line. Key patterns:

- `! Undefined control sequence.` followed by `l.NNN` → `undefined_cmd`, extract line and file from context
- `! Too many }'s.` → `extra_brace`
- `! Misplaced \noalign` or `! Extra alignment tab` → `trailing_amp`
- Any other `! ` line → `unknown`

File attribution: scan backwards from the `!` line for the most recent `(chapters/chXX_...)` open-paren entry in the log.

---

## Repair Agent Prompt (`latex_repair_agent.py`)

```
You are a LaTeX expert. The following file failed to compile with this error:

File: {file}
Line: {line}
Error: {message}

Here is the full file content:
{content}

Fix ONLY the error above. Return the complete corrected LaTeX file.
Do NOT add comments. Do NOT change any other content.
```

- Uses `ClaudeCLILLM` (same subprocess-based LLM already used by the crew).
- If the file path is empty or the file does not exist, skip the agent call and log a warning.
- Writes the LLM response directly back to the `.tex` file (no intermediate temp file).

---

## `article_crew.py` changes

Replace the `_compile_pdf()` call site (currently lines 101–111) with a call to `_compile_with_repair()`. The new method:

1. Reads `max_attempts` from `self._cfg` (falls back to `3`).
2. Runs the loop described in Data Flow.
3. Returns `Path | None` (same contract as the old `_compile_pdf`).

The old `_compile_pdf()` method is removed.

---

## Config

Add to `config/setup.json`:
```json
"latex": {
  "max_repair_attempts": 3
}
```

---

## Testing

| Test file | What it covers |
|---|---|
| `tests/unit/test_latex_log_parser.py` | Feed synthetic log strings; assert correct `LatexError` list (kind, file, line) |
| `tests/unit/test_latex_patcher.py` | Feed `.tex` strings with known-bad patterns; assert corrected output string |
| `tests/unit/test_latex_repair_agent.py` | Mock `ClaudeCLILLM`; assert prompt contains error message + file content; assert file written |
| `tests/unit/test_article_crew_repair.py` | Mock `LaTeXCompileTool` to fail twice then succeed; assert loop runs exactly 3 `run()` calls; assert return value is a `Path` |

All tests use `pytest` with `unittest.mock`. No real LLM calls in unit tests.

---

## Constraints

- All new files ≤ 150 lines (no comments/blanks counted).
- No hardcoded paths — `latex_dir` passed as parameter; `max_repair_attempts` from config.
- No new external dependencies — uses only stdlib (`re`, `pathlib`, `dataclasses`) and existing project code.
- `ClaudeCLILLM` is already available; no new LLM client needed.
