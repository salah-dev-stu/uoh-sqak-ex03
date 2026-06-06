# PRD: Bibliography System

**Component**: `latex/bib/references.bib` + `src/agent_article/tools/bib_formatter.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

The Bibliography system manages the `.bib` file that backs all in-text citations, drives the
`biblatex + biber` compilation pass, and ensures every `\cite{AuthorYear}` link in the PDF
is clickable and jumps to the correct bibliography entry. It spans both the LaTeX project
(`latex/bib/references.bib`) and a Python utility that validates and formats `.bib` entries.
The `[AuthorYear]` convention (e.g. `[Segal2026]`) is used consistently by all agents.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `raw_sources` | `list[dict]` | Sources from `ResearcherAgent` (title, url, author, year) |
| **Input** `citation_markers` | `list[str]` | `[AuthorYear]` keys found in chapter Markdown files |
| **Input** `bib_path` | `Path` | `latex/bib/references.bib` — the master bibliography file |
| **Output** `references.bib` | `str` | Populated BibTeX file committed to `latex/bib/` |
| **Output** `bib_report.md` | `str` | Validation report: missing keys, duplicates, format issues |
| **Output** `\cite{…}` links | PDF | Clickable hyperlinks in compiled PDF (manual link test) |

---

## Functional Requirements

1. **FR-BB-01**: Use `biblatex` package (NOT legacy `bibtex`) in `latex/main.tex`. The
   preamble must include `\usepackage[backend=biber, style=authoryear, hyperref=true]{biblatex}`
   loaded from the LaTeX template configured in `config/latex.json`, not hardcoded.

2. **FR-BB-02**: Adopt the `AuthorYear` cite key convention (e.g. `Segal2026`, `Russell2021`).
   All agents use this format consistently. The `EditorAgent` validates every `[AuthorYear]`
   marker against `references.bib` before chapters reach `LaTeXAgent`.

3. **FR-BB-03**: Implement `BibEntryFormatter` in `src/agent_article/tools/bib_formatter.py`.
   It accepts source metadata (`author`, `title`, `year`, `url`, optional `journal`,
   `publisher`) and returns a well-formed BibTeX entry string. Entry type defaults to
   `@misc` for web sources and `@article` for journal sources.

4. **FR-BB-04**: Implement `BibValidator` that reads `references.bib` and verifies: no
   duplicate cite keys; all mandatory fields present per entry type; all `[AuthorYear]`
   markers in chapter files have a matching key. Report all violations in
   `workspace/bib_report.md`; do not silently skip any violation.

5. **FR-BB-05**: The compiled PDF must have clickable bibliography links. This requires the
   `hyperref` package loaded after `biblatex` in `main.tex`, and all four compile passes
   completed (`lualatex → biber → lualatex → lualatex`). `LaTeXAgent` must not skip the
   biber pass; a missing biber pass results in broken citation links.

6. **FR-BB-06**: `\printbibliography` must appear as the last element before `\end{document}`
   in `main.tex`. The bibliography section title is localised via
   `config/latex.json::bib_title` (English: `Bibliography`; Hebrew primary: `ביבליוגרפיה`).

7. **FR-BB-07**: Commit `references.bib` to `latex/bib/` and track it in git. Intermediate
   biber artefacts (`.bbl`, `.blg`) are listed in `.gitignore` and must not be committed.

---

## Non-Functional Requirements

- **NFR-BB-01 Completeness**: Every cited source must have a `.bib` entry; every entry must
  be cited at least once. Orphan entries are flagged as warnings by `BibValidator`.
- **NFR-BB-02 Format Portability**: The `.bib` file must be parseable by both `biber`
  (primary) and legacy `bibtex` (fallback); avoid `biblatex`-only field names in entries.
- **NFR-BB-03 Reproducibility**: Given the same source metadata, `BibEntryFormatter` produces
  byte-identical output; cite keys are derived deterministically from `AuthorYear`.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `latex.bib_style` | `config/latex.json` | biblatex style (default `"authoryear"`) |
| `latex.bib_title` | `config/latex.json` | Bibliography section title string |
| `latex.bib_path` | `config/latex.json` | Relative path from `latex/` to the `.bib` file |

No environment variables are used by the Bibliography system.

---

## Acceptance Criteria

- [ ] `BibEntryFormatter` produces a valid `@misc` entry from a minimal source dict.
- [ ] `BibValidator` reports a duplicate-key error when two entries share the same cite key.
- [ ] `BibValidator` reports a missing-key error when a `[AuthorYear]` marker has no entry.
- [ ] After a full 4-pass compile, clicking a `\cite{}` link in the PDF navigates to the
      bibliography entry (manual verification noted in CI docs).
- [ ] `references.bib` is present in `latex/bib/` and tracked by git (`git ls-files` lists it).
- [ ] `.bbl` and `.blg` are absent from git tracking (`.gitignore` verified by grep).
- [ ] `ruff check` returns 0 on `bib_formatter.py`; file has ≤ 150 logical lines.
