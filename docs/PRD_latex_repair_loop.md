# PRD: Post-Pipeline LaTeX Compile-and-Fix Loop

**Feature ID:** RL-01  
**Version:** 1.00  
**Date:** 2026-06-10  
**Author:** Salah Qadah / Andalus Kalash  
**Status:** Approved

---

## 1. Overview

### 1.1 Problem Statement

After the CrewAI pipeline regenerates LaTeX chapter files, the LuaLaTeX compilation
step frequently fails because agents introduce known-bad patterns (`\textslash`,
`\textplus`, extra `}`, trailing `&` before `\\`) that are not caught until compile time.
Currently, every such failure requires manual inspection of `main.log` and hand-editing
the offending `.tex` file — an interrupt to the automated pipeline that breaks the
"run once, get PDF" contract.

### 1.2 Goal

Make the pipeline fully hands-free: after compilation fails, automatically detect the
error class, apply a free regex fix if the pattern is known, fall back to an LLM
re-prompt for novel errors, and retry — returning `Success: True` without human
intervention in all common failure cases.

### 1.3 Approved Approach

**Hybrid (RL-FR-05):**
- Attempt 1: compile → fail → parse log → apply known-pattern regex patches
- Attempt 2: compile → fail → parse log → patch known + re-prompt LLM for unknown
- Attempt 3: compile → fail → give up (return `None`, log exhausted)
- Attempt N (any): compile → success → return `Path(pdf)` immediately

---

## 2. Functional Requirements

| ID | Requirement |
|----|-------------|
| RL-FR-01 | `latex_log_parser.parse(log_path)` reads `main.log` and returns `list[LatexError]`; each error has `file`, `line`, `message`, `kind` |
| RL-FR-02 | `kind` is classified as `"undefined_cmd"`, `"extra_brace"`, `"trailing_amp"`, or `"unknown"` |
| RL-FR-03 | `latex_patcher.apply(errors, latex_dir)` applies in-place regex fixes for known kinds; returns count of modified files |
| RL-FR-04 | Known fixes: `\textslash`→`/`, `\textplus`→`+`, `\textminus`→`-` (undefined_cmd); strip trailing `&` before `\\` (trailing_amp); remove extra `}` at reported line (extra_brace) |
| RL-FR-05 | `ArticleCrew._compile_with_repair()` replaces `_compile_pdf()`; runs hybrid 3-attempt loop |
| RL-FR-06 | Agent re-prompt (`latex_repair_agent.repair()`) fires only from attempt 2 onwards, only for `kind == "unknown"` errors with a non-empty `file` field |
| RL-FR-07 | Re-prompt sends full file content + error message to `ClaudeCLILLM`; writes response back to `.tex` file |
| RL-FR-08 | If the log has no parseable errors after a compile failure, the loop breaks immediately (no pointless retries) |
| RL-FR-09 | Max retry count is read from `config/latex.json` key `max_repair_attempts`; default 3 if absent |
| RL-FR-10 | LLM re-prompt exceptions are caught and logged; the loop continues to the next attempt |

---

## 3. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| RL-NFR-01 | Three new files under `src/agent_article/crew/`, each ≤ 150 lines |
| RL-NFR-02 | No new external dependencies — stdlib only (`re`, `pathlib`, `dataclasses`) plus existing `ClaudeCLILLM` |
| RL-NFR-03 | Known-pattern fixes cost zero tokens (pure regex, no LLM call) |
| RL-NFR-04 | Agent re-prompt is bounded: one LLM call per unique file per repair round |
| RL-NFR-05 | All new code covered by unit tests using `unittest.mock` — no real LLM calls in tests |

---

## 4. Architecture

```
ArticleCrew.run()
└── _compile_with_repair()            ← replaces _compile_pdf()
    │
    ├── attempt 1
    │   ├── LaTeXCompileTool.run()   → success → return Path(pdf)
    │   └── fail
    │       ├── latex_log_parser.parse(main.log)  → list[LatexError]
    │       ├── latex_patcher.apply(known, latex_dir)   ← regex, free
    │       └── unknown errors → carried to attempt 2
    │
    ├── attempt 2
    │   ├── LaTeXCompileTool.run()   → success → return Path(pdf)
    │   └── fail
    │       ├── latex_log_parser.parse(main.log)
    │       ├── latex_patcher.apply(known, latex_dir)
    │       └── latex_repair_agent.repair(unknown, latex_dir)  ← LLM call
    │
    └── attempt 3
        ├── LaTeXCompileTool.run()   → success → return Path(pdf)
        └── fail → log "repair exhausted" → return None
```

**New modules:**

| Module | Responsibility |
|--------|----------------|
| `src/agent_article/crew/latex_log_parser.py` | Parse `main.log` → `list[LatexError]` |
| `src/agent_article/crew/latex_patcher.py` | Apply regex fixes for known error kinds |
| `src/agent_article/crew/latex_repair_agent.py` | Re-prompt `ClaudeCLILLM` for unknown errors |

---

## 5. Input / Output / Setup

```
Input:  LaTeX project at latex/ (chapters already written by pipeline agents)
Output: Path to compiled PDF, or None if all attempts fail
Setup:  lualatex + biber installed; claude CLI logged in (for agent re-prompt path)
```

---

## 6. Known-Pattern Table

| kind | Log trigger | Fix |
|------|-------------|-----|
| `undefined_cmd` | `! Undefined control sequence` + `\textslash` | `\textslash` → `/` |
| `undefined_cmd` | `! Undefined control sequence` + `\textplus` | `\textplus` → `+` |
| `undefined_cmd` | `! Undefined control sequence` + `\textminus` | `\textminus` → `-` |
| `extra_brace` | `! Too many }'s` | Remove trailing `}` at reported line |
| `trailing_amp` | `! Misplaced \noalign` or `! Extra alignment tab` | Strip `& \\` in table rows |

---

## 7. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | Pipeline produces `Success: True` when only known-pattern errors are present | Run pipeline; check result |
| AC-2 | `_compile_with_repair` retries exactly 3 times on repeated failures before returning `None` | `test_returns_none_after_all_attempts_exhausted` |
| AC-3 | Agent re-prompt is NOT called on attempt 1 | `test_retries_after_known_error_and_succeeds` |
| AC-4 | Agent re-prompt IS called on attempt 2 for unknown errors | `test_calls_agent_repair_on_attempt_2_unknown` |
| AC-5 | Loop exits early when log has no parseable errors | `test_stops_early_when_log_has_no_errors` |
| AC-6 | `pytest tests/unit/test_latex_log_parser.py tests/unit/test_latex_patcher.py tests/unit/test_latex_repair_agent.py tests/unit/test_article_crew_repair.py` — 24 tests pass | CI |
| AC-7 | `ruff check src/agent_article/crew/latex_log_parser.py latex_patcher.py latex_repair_agent.py` — clean | CI |
