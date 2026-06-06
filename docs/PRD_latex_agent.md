# PRD: LaTeXAgent

**Component**: `src/agent_article/agents/latex_agent.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`LaTeXAgent` is the fourth and final agent in the sequential pipeline. It converts the edited
Markdown chapters from `workspace/chapters_edited/` into a complete LaTeX project under
`latex/`, triggers `ChartGeneratorTool` to produce the Python-generated chart, assembles
`latex/main.tex`, and invokes `LaTeXCompileTool` to run the 4-pass build sequence
(`lualatex → biber → lualatex → lualatex`). The agent's task prompt must contain the
literal phrase **"fancy formula, not plain text"** (spec §13.2 mandate). It uses
`skills/latex_skill/SKILL.md` for LaTeX conventions, BiDi setup, and the biblatex pattern.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `chapters_edited_dir` | `Path` | `workspace/chapters_edited/` — edited Markdown |
| **Input** `edit_report_path` | `Path` | `workspace/edit_report.md` — formula + citation flags |
| **Input** `bib_path` | `Path` | `latex/bib/references.bib` |
| **Input** `skill_path` | `Path` | Path to `skills/latex_skill/SKILL.md` |
| **Input** `latex_config` | `dict` | Compiler settings loaded from `config/latex.json` |
| **Output** `main.tex` | `Path` | Assembled root LaTeX file at `latex/main.tex` |
| **Output** `chapters/*.tex` | `list[Path]` | One `.tex` file per chapter in `latex/chapters/` |
| **Output** `figures/chart.png` | `Path` | Python-generated chart saved to `latex/figures/` |
| **Output** `uoh-sqak-article.pdf` | `Path` | Final compiled PDF at `latex/output/` |

---

## Functional Requirements

1. **FR-LA-01**: Load `role`, `goal`, and `backstory` from `config/agents.json::agents.latex`;
   none of these strings may appear in source code. The `goal` field in config must contain
   the verbatim phrase **"fancy formula, not plain text"** so the agent inherits this
   requirement in its LLM context.

2. **FR-LA-02**: Convert each `chapter_N.md` to `chapter_N.tex` using Pandoc-style Markdown→LaTeX
   conversion logic (implemented in `src/agent_article/tools/latex_compiler.py`). Preserve
   citation keys in `\cite{AuthorYear}` form. Map `$$…$$` formula blocks to
   `\begin{equation}…\end{equation}` so amsmath renders them as display-mode equations.

3. **FR-LA-03**: Detect the BiDi chapter (via `<!-- BiDi chapter -->` comment in the Markdown
   source) and wrap it with `\begin{RTL}…\end{RTL}` (using the `bidi` package) or the
   `polyglossia` Hebrew environment, as configured in `config/latex.json::bidi_package`.

4. **FR-LA-04**: Invoke `ChartGeneratorTool` to run the Python chart script
   (`src/agent_article/tools/chart_generator.py`) and save the output PNG to
   `latex/figures/chart.png`. Insert a `\includegraphics{figures/chart}` reference in the
   appropriate chapter.

5. **FR-LA-05**: Assemble `latex/main.tex` with: cover sheet (`\maketitle`), ToC
   (`\tableofcontents`), `\input{chapters/chapter_N}` for each chapter, and
   `\printbibliography` at the end. Include `fancyhdr` for page headers/footers, and at least
   one `tikzpicture` block diagram of the CrewAI architecture (mandatory per spec L1708–1714).

6. **FR-LA-06**: Invoke `LaTeXCompileTool` via `ApiGatekeeper` to run the 4-pass build:
   `lualatex main.tex` → `biber main` → `lualatex main.tex` → `lualatex main.tex`.
   Capture stdout/stderr; raise `CompilationError` if any pass returns non-zero exit code.

7. **FR-LA-07**: Verify the output PDF page count is within the range specified by
   `config/latex.json::target_page_min` and `target_page_max` (default 14–17). Log a warning
   if out of range.

---

## Non-Functional Requirements

- **NFR-LA-01 Reproducibility**: Given the same Markdown input, the LaTeX output must be
  byte-identical (except for compile timestamps controlled by `\pdftrailerid{}`).
- **NFR-LA-02 Compile Speed**: The 4-pass compile must complete within 120 seconds on the
  target machine (macOS with TeXLive); enforced as a timeout in `LaTeXCompileTool`.
- **NFR-LA-03 Isolation**: The LaTeX compile runs in a subprocess; it must not have access to
  Python's in-process state, and its working directory is always `latex/`.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `agents.latex.role` | `config/agents.json` | CrewAI `role` string |
| `agents.latex.goal` | `config/agents.json` | Must contain "fancy formula, not plain text" |
| `agents.latex.backstory` | `config/agents.json` | CrewAI `backstory` string |
| `agents.latex.llm` | `config/agents.json` | LLM model key |
| `agents.latex.skill_ref` | `config/agents.json` | Relative path to `SKILL.md` |
| `latex.compiler` | `config/latex.json` | `"lualatex"` or `"xelatex"` |
| `latex.bidi_package` | `config/latex.json` | `"bidi"` or `"polyglossia"` |
| `latex.target_page_min` | `config/latex.json` | Integer; default 14 |
| `latex.target_page_max` | `config/latex.json` | Integer; default 17 |
| `latex.compile_timeout_seconds` | `config/latex.json` | Integer; default 120 |

---

## Acceptance Criteria

- [ ] `LaTeXCompileTool` is invoked exactly 4 times (lualatex × 3, biber × 1) in the correct
      order (verified by mock subprocess call recorder).
- [ ] Each `$$…$$` block in edited Markdown maps to `\begin{equation}…\end{equation}` in the
      output `.tex` (unit test with regex assertion).
- [ ] The BiDi chapter `.tex` contains an RTL-environment wrapper (`\begin{RTL}` or equivalent).
- [ ] `CompilationError` is raised when `LaTeXCompileTool` mock returns exit code 1.
- [ ] The agent's `goal` string (from `config/agents.json`) contains the phrase
      `"fancy formula, not plain text"` (string-presence test on config load).
- [ ] `ruff check` returns 0; file has ≤ 150 logical lines.
