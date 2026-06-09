# PRD: Fast Pipeline — Haiku + Parallel LaTeX Tasks

**Feature ID:** FP-01  
**Version:** 1.00  
**Date:** 2026-06-09  
**Author:** Salah Qadah / Andalus Kalash  
**Status:** Approved

---

## 1. Overview

### 1.1 Problem Statement

The current CrewAI pipeline (Researcher → Writer → Editor → 7 sequential LaTeX tasks) takes
60–80 minutes end-to-end using `claude -p` (Claude Sonnet via subscription). This makes
iterative development impractical and falls below the quality bar expected for a production
multi-agent system.

### 1.2 Goal

Reduce full pipeline execution time from ~70 minutes to **under 10 minutes** while maintaining
PDF quality and preserving all grading requirements (BiDi, equations, citations, 15+ pages).

### 1.3 Approved Approach

**Option C — Haiku + Parallel LaTeX tasks:**
- Switch `ClaudeCLILLM` to use `claude-haiku-4-5-20251001` as the default model (5–10× faster than Sonnet)
- Override `ch05_bidi` task to use Sonnet (complex BiDi rules require higher-quality model)
- Run the 7 LaTeX chapter tasks concurrently using Python `ThreadPoolExecutor`
- Keep Researcher → Writer → Editor sequential (they depend on each other)

---

## 2. Functional Requirements

| ID | Requirement |
|----|-------------|
| FP-FR-01 | `ClaudeCLILLM` must accept a `model` parameter per-instance; default to `claude-haiku-4-5-20251001` |
| FP-FR-02 | Each `Task` in `build_latex_tasks()` may specify a model override stored in `config/tasks.json` |
| FP-FR-03 | `latex_ch05` task MUST use `claude-sonnet-4-6` (BiDi rules are complex; haiku is insufficient) |
| FP-FR-04 | `ArticleCrew._build_crew()` must run the 7 LaTeX tasks in parallel via `ThreadPoolExecutor` — not via CrewAI `Process`, which enforces sequential execution |
| FP-FR-05 | Parallel execution must be transparent: logs show per-task start/complete with thread ID |
| FP-FR-06 | Each parallel LaTeX task writes its output to `output_file` independently; no shared state |
| FP-FR-07 | Post-parallel step: compile LaTeX (lualatex → biber → lualatex → lualatex) after all 7 tasks complete |
| FP-FR-08 | On task failure, the failed task logs its error and the pipeline continues; failed chapters fall back to the previous version in `latex/chapters/` |
| FP-FR-09 | Total wall-clock time for a full fresh run MUST be ≤ 10 minutes on macOS with Claude subscription |
| FP-FR-10 | `config/tasks.json` gains a `model` field per task; tasks without it inherit the crew default |
| FP-FR-11 | Agent prompts must encode output quality rules so Haiku produces clean LaTeX without manual patching: pure LaTeX output, correct `p{}` table columns, citation keys matching research notes |

---

## 3. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| FP-NFR-01 | Thread count capped at `min(7, cpu_count())` — no unbounded thread pools |
| FP-NFR-02 | Each thread's `claude -p` subprocess has its own timeout (default 300s for Haiku, 600s for Sonnet) |
| FP-NFR-03 | `ClaudeCLILLM` remains ≤ 150 lines (rule #7) — model override via config, not hardcoding |
| FP-NFR-04 | Parallel phase is covered by integration tests using mock `ClaudeCLILLM` |
| FP-NFR-05 | All existing tests continue to pass after the refactor |

---

## 4. Architecture

```
ArticleCrew.run()
├── Phase 1 — Sequential (CrewAI Process.sequential)
│   ├── ResearcherAgent  → workspace/research_notes.md      [Haiku, ~2 min]
│   ├── WriterAgent      → workspace/chapters/ch0N.md       [Haiku, ~2 min]
│   └── EditorAgent      → workspace/chapters/ch0N_edited.md [Haiku, ~1 min]
│
└── Phase 2 — Parallel (ThreadPoolExecutor, outside CrewAI)
    ├── Thread 1: latex_ch01 → latex/chapters/ch01_introduction.tex  [Haiku, ~1 min]
    ├── Thread 2: latex_ch02 → latex/chapters/ch02_architectures.tex  [Haiku, ~1 min]
    ├── Thread 3: latex_ch03 → latex/chapters/ch03_frameworks.tex     [Haiku, ~1 min]
    ├── Thread 4: latex_ch04 → latex/chapters/ch04_production.tex     [Haiku, ~1 min]
    ├── Thread 5: latex_ch05 → latex/chapters/ch05_bidi.tex           [Sonnet, ~2 min]
    ├── Thread 6: latex_ch06 → latex/chapters/ch06_casestudy.tex      [Haiku, ~1 min]
    └── Thread 7: latex_bib  → latex/bib/references.bib               [Haiku, ~1 min]
        (all 7 run simultaneously — wall-clock = slowest = ch05 ~2 min)

Post-parallel: lualatex → biber → lualatex → lualatex  [~1.5 min]

Total: ~5–7 min
```

---

## 5. Input / Output / Setup

```
Input:  topic: str (from TUI or CLI)
Output: latex/output/uoh-sqak-article.pdf — ≥15 pages, compiled
Setup:  claude CLI logged in (claude --login); lualatex installed
```

---

## 6. Agent Prompt Quality Rules (to encode in tasks.json / SKILL.md)

These rules prevent manual post-processing — agents must follow them automatically:

| Rule | Encoding location |
|------|-------------------|
| Output ONLY LaTeX — first char must be `%` or `\`, no trailing prose | All `latex_ch*` task descriptions |
| Tables: always use `p{Xcm}` column types, never bare `l` or `r` | All `latex_ch*` task descriptions |
| Citation keys: use EXACTLY the `[AuthorYear]` keys from `workspace/research_notes.md` | `latex_bib` + all `latex_ch*` task descriptions |
| `latex_bib` generates entries for every key used in chapters | `latex_bib` task description |
| No markdown fences, no explanation blocks after the LaTeX content | All `latex_ch*` task descriptions |

---

## 7. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| AC-1 | Full pipeline completes in ≤ 10 min on macOS with subscription | `time uv run python -m agent_article.main` |
| AC-2 | PDF ≥ 15 pages with all required elements (cover, TOC, equations, BiDi, bibliography) | Visual inspection + page count |
| AC-3 | No `[AuthorYear]` bold keys in PDF — all citations render as `[N]` | PDF inspection |
| AC-4 | No overfull \hbox warnings > 20pt in latex log | `grep Overfull latex/output/main.log` |
| AC-5 | `pytest --cov` ≥ 85% after refactor | CI output |
| AC-6 | Git log shows incremental commits for each implementation step | `git log --oneline` |
