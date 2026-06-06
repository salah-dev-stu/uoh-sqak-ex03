# Product Requirements Document — HW3 Article Generation Pipeline

> **Mission:** Create a CrewAI multi-agent pipeline that produces a ≥15-page LuaLaTeX PDF article on **Multi-Agent Orchestration Patterns**, covering all technical envelope requirements (BiDi, fancy formulas, linked citations, TikZ diagram, Python chart, table, image, bibliography).

**Version:** 1.00
**Authors:** Salah Qadah (323039974), Andalus Kalash (211435797)
**Pair ID:** uoh-sqak
**Course:** 203.3763 — Orchestration of AI Agents
**Institution:** University of Haifa, Spring 2026 (תשפ"ו)
**Lecturer:** Dr. Yoram Reuven Segal
**Deadline:** Friday, 12 June 2026, 23:59 Asia/Jerusalem
**Moodle Assignment:** id=270973
**Date:** 2026-06-06

---

## 1. Executive Summary

This product is a **Python CLI application** (`agent-article`) that orchestrates a **CrewAI sequential multi-agent team** of four specialized AI agents to collaboratively research, write, edit, and typeset a professional ≥15-page LaTeX article. The central graded deliverable is a PDF file `latex/output/uoh-sqak-article.pdf` that demonstrates correct typesetting of BiDi text (Hebrew+English), fancy mathematical formulas (not plain text), a TikZ block diagram, a Python-generated chart, a well-formatted table, linked bibliography citations, and proper page structure (cover, TOC, headers/footers, chapters).

---

## 2. Description Bullets

The following three bullets define the scope. **All other requirements derive from these.**

**A. Multi-Agent CrewAI Pipeline**
- 4 CrewAI agents in `Process.sequential` order: ResearcherAgent → WriterAgent → EditorAgent → LaTeXAgent
- Each agent has a distinct `role`, `goal`, `backstory` loaded from `config/agents.json`
- Each agent is augmented by a `SKILL.md` file (file-based expertise injection) from the `skills/` layer
- All external calls (LLM, web search, LaTeX subprocess) are routed through `ApiGatekeeper`
- The `ArticleSDK` class is the sole public entry point (R1)

**B. LaTeX Article Deliverable ≥15 Pages**
- Topic: **Multi-Agent Orchestration Patterns**
- Markdown-first workflow: agents produce `.md` files → LaTeXAgent converts to `.tex` and compiles
- Compiler: LuaLaTeX (4 passes: `lualatex → biber → lualatex → lualatex`)
- Bibliography: `biblatex` + `biber` (NOT legacy bibtex/natbib)
- Article structure: Cover Sheet → TOC → 6 Chapters → Bibliography

**C. Technical Envelope Features (All Mandatory)**
| Feature | Requirement |
|---|---|
| Cover sheet | Topic + Authors + Date + Course 203.3763 + Dr. Yoram Segal |
| Table of contents | Auto-generated via `\tableofcontents` |
| Headers/footers | `fancyhdr` on every page |
| ≥1 image | `\includegraphics` in any chapter |
| ≥1 Python chart | `ChartGeneratorTool` (matplotlib) → PNG → `\includegraphics` |
| ≥1 table (no overflow) | `tabularx` column type, no page overflow |
| ≥1 fancy formula | `\begin{equation}...\end{equation}` — NEVER plain text |
| BiDi chapter | Ch5 in Hebrew↔English mix using `polyglossia` |
| Linked citations | `biblatex` + `\cite{}` + `hyperref` — clickable in PDF viewer |
| TikZ block diagram | Crew architecture diagram in Ch1 — MANDATORY per lecture |

---

## 3. User Stories

### End User (Salah / Andalus)
- **US-01:** As a student, I want to run `uv run agent-article` and get a ≥15-page PDF in ≤20 minutes so I can submit my homework.
- **US-02:** As a developer, I want a letter-keyed TUI menu (G/C/A/S/X) so I can re-run partial steps without restarting from scratch.
- **US-03:** As a developer, I want a human-in-the-loop checkpoint to review Markdown before LaTeX compilation so I can catch content errors before a 4-pass compile.
- **US-04:** As a developer, I want a spend report showing token usage so I can stay within the daily LLM budget.

### Grader (Dr. Yoram Segal / automated grader)
- **US-05:** As a grader, I want to `git clone && uv sync && uv run agent-article` and have it work with no hand-holding.
- **US-06:** As a grader, I want to click citations in the PDF and have them jump to the bibliography section.
- **US-07:** As a grader, I want to see at least one mathematical formula that uses LaTeX math mode (not plain text arithmetic).
- **US-08:** As a grader, I want `uv run pytest tests/unit tests/integration --cov=src` to pass with coverage ≥85%.
- **US-09:** As a grader, I want the `ruff check` command to return 0 errors.
- **US-10:** As a grader, I want to see ≥50 meaningful commits in the git history showing incremental development.

---

## 4. Functional Requirements

### FR-01: Four CrewAI Agents
- `ResearcherAgent`: searches the web (DuckDuckGo, no API key), writes structured notes to `workspace/research_notes.md`
- `WriterAgent`: reads notes, writes 6 Markdown chapters to `workspace/chapters/ch01.md … ch06.md`
- `EditorAgent`: polishes all chapters, saves to `workspace/chapters/ch0N_edited.md`
- `LaTeXAgent`: converts edited Markdown to `.tex`, generates chart, compiles PDF — goal MUST include phrase "fancy formula, not plain text"

### FR-02: Sequential Process
- All four agents run in `Process.sequential` order
- Each task receives `context=[previous_task]` to chain outputs

### FR-03: Markdown-First Workflow
- Agents produce `.md` intermediate files in `workspace/`
- Human-in-the-loop checkpoint via `SDK.approve_markdown()` before LaTeX conversion
- Approved Markdown files copied to `results/` as trace evidence (committed to git)

### FR-04: LaTeX PDF ≥15 Pages
- Chapter list: Introduction (Ch1), Architectures (Ch2), Framework Comparison (Ch3), Production Patterns (Ch4), BiDi Chapter in Hebrew (Ch5), Case Study (Ch6)
- Cover sheet is pages 1-2; TOC is page 3; each chapter ≥2 pages; bibliography ≥1 page
- PDF file named `latex/output/uoh-sqak-article.pdf`

### FR-05: Human-in-the-Loop
- After `EditorAgent` finishes, pause and prompt: `"Approve Markdown content for LaTeX conversion? [y/N]"`
- If `n`: stop gracefully, log reason
- If `y`: proceed to `LaTeXAgent`

### FR-06: SDK as Sole Public Entry Point
- `ArticleSDK` is the ONLY way to invoke pipeline operations
- External code NEVER imports directly from `agents/`, `crew/`, or `tools/`
- Public methods: `generate_article()`, `approve_markdown()`, `compile_pdf()`, `get_spend_report()`, `run_audit()`

### FR-07: Gatekeeper for All External Calls
- All Claude CLI calls, DuckDuckGo calls, and subprocess (lualatex/biber) calls route through `ApiGatekeeper`
- `ApiGatekeeper` enforces: requests per minute, tokens per article, daily token cap
- All limits configurable in `config/rate_limits.json` — zero hardcoded values

### FR-08: Terminal Menu
- Letter-keyed TUI: `G` = Generate, `C` = Compile only, `A` = Audit, `S` = Spend report, `X` = Exit
- Built with `rich` library
- Entry via `uv run agent-article` (configured in `pyproject.toml` `[project.scripts]`)

### FR-09: Structured Logging (FIFO Queue)
- All components log to JSONL files in `logs/` directory
- Max 20 files × 500 lines per file (FIFO: oldest file deleted when limit reached)
- Each log entry: timestamp (UTC), level, component, message, key-value fields

### FR-10: LaTeX Technical Features
- TikZ Crew architecture diagram in Ch1 (MANDATORY)
- `polyglossia` for BiDi Hebrew↔English in Ch5
- `biblatex` + `biber` bibliography (not legacy bibtex)
- `hyperref` for clickable links and citations
- `fancyhdr` for headers/footers
- `tabularx` for non-overflowing tables
- `amsmath` for fancy formula rendering

### FR-11: Python-Generated Chart
- `ChartGeneratorTool` uses `matplotlib` to generate a bar/line chart
- Chart saved as `latex/figures/agent_topology.png` (PNG, 150 DPI)
- Chart included in article via `\includegraphics`

### FR-12: Version Management
- Version starts at `"1.00"`
- `bump(version)` increments patch: `"1.00" → "1.01"`
- Version stored in: `src/agent_article/shared/version.py` AND all `config/*.json`

### FR-13: Skill Layer
- Each agent has a corresponding `SKILL.md` in `src/agent_article/skills/<name>_skill/`
- `FileSkill` reads `SKILL.md`, strips YAML frontmatter, injects content into agent backstory
- Skill files are version-controlled and human-readable

### FR-14: Configuration-Driven
- Zero hardcoded values in Python source
- All configurable items in `config/*.json`: agent parameters, task descriptions, rate limits, LaTeX compiler path, output filenames
- `ConfigLoader` singleton with in-process cache and `reload()` for tests

### FR-15: Secret Management
- Zero secrets in source code
- `.env-example` committed with placeholder values
- `.env` git-ignored
- API key read via `os.environ.get("ANTHROPIC_API_KEY")`

---

## 5. Non-Functional Requirements

### NFR-01: Performance
- Full pipeline (research + write + edit + compile) completes in ≤25 minutes
- LaTeX compilation completes in ≤60 seconds
- TUI responds in ≤100ms for menu interactions

### NFR-02: Code Quality
- `ruff check` returns 0 errors (line-length=100, py313, E/F/W/I/N/UP/B/C4/SIM, ignore E501)
- Every Python file ≤150 logical lines (excluding blanks/comments)
- OOP with `BaseAgent`, `BaseTool`, `BaseSkill` abstract base classes (no code duplication)
- Class diagram committed to `docs/diagrams/`

### NFR-03: Test Coverage
- `pytest --cov=src --cov-fail-under=85` passes
- Unit tests: no Claude CLI calls (MockLLM)
- Integration tests: real lualatex subprocess, real filesystem
- E2E tests: real Claude CLI, gated behind `RUN_E2E=1` env var

### NFR-04: Portability
- Grader can `git clone && uv sync && uv run agent-article` with no hand-holding
- Works on macOS (development) and Linux (CI/grader)
- `uv` is mandatory; no `pip`, `venv`, `virtualenv` allowed anywhere

### NFR-05: Git History
- ≥50 commits with meaningful messages on `main` branch
- Commits are incremental (one feature/fix per commit)
- No single large push at deadline

### NFR-06: Maintainability
- Extension points documented in `README.md` and `docs/PLAN.md`
- Agent registry: add agent by dropping file in `agents/` + registering in `config/agents.json`
- Skill registry: add skill by dropping directory in `skills/`
- Tool registry: subclass `BaseTool`, add to agent tool list

### NFR-07: Security
- No API keys in any committed file
- Pre-commit hook scans for `sk-ant` / `api_key =` patterns
- GitHub Actions CI runs the same scan

### NFR-08: Documentation
- `README.md` is a complete product manual: install, usage, architecture, cost, extend, contribute, license, AI ethics
- `docs/PROMPTS.md` with ≥25 entries (AI audit trail)
- 10 per-mechanism PRDs in `docs/`
- 7 ADRs in `docs/ADRs/`
- C4 model + UML sequence + class diagram in `docs/diagrams/`

---

## 6. Architecture Overview

See `docs/PLAN.md` for full C4 model, UML sequence diagram, and class diagram.

**Layer stack summary:**
```
[Terminal Menu]  →  [ArticleSDK]  →  [ArticleCrew]  →  [Agents × 4]
    →  [Tasks × 4]  →  [Tools × 5]  →  [ApiGatekeeper]
    →  [Claude CLI / DuckDuckGo / lualatex]
```

**Key design decisions:**
- CrewAI `Process.sequential` (not hierarchical) — closed pipeline, sequential article writing
- Markdown-first (not direct LaTeX) — agents produce human-readable intermediates
- Single LLM provider (Claude CLI login) — voice consistency across all agents
- LuaLaTeX (not XeLaTeX) — equal per lecturer; LuaLaTeX selected
- `biblatex` + `biber` — NOT legacy bibtex
- DuckDuckGo — free, no API key, sufficient for known-domain topic

---

## 7. Acceptance Criteria

### AC-01: PDF Quality
- [ ] PDF file exists at `latex/output/uoh-sqak-article.pdf`
- [ ] PDF has ≥15 pages when opened in a PDF viewer
- [ ] Cover sheet shows: topic, both authors, date, course 203.3763, Dr. Yoram Segal
- [ ] Table of contents on page 3 with correct page numbers
- [ ] Headers show course title on every non-cover page
- [ ] At least 1 `\includegraphics` image visible
- [ ] At least 1 Python-generated chart (PNG created by `chart_generator.py`) visible
- [ ] At least 1 table rendered without page overflow
- [ ] At least 1 mathematical formula in `\begin{equation}...\end{equation}` format
- [ ] Chapter 5 contains ≥2 paragraphs in Hebrew text with correct RTL rendering
- [ ] All `\cite{}` commands produce clickable hyperlinks jumping to bibliography
- [ ] TikZ block diagram of the Crew architecture visible in Ch1
- [ ] Bibliography section at the end with ≥5 entries

### AC-02: Code Quality
- [ ] `uv run ruff check src tests scripts` returns exit code 0
- [ ] `uv run python scripts/check_file_lines.py` returns "OK"
- [ ] `uv run pytest tests/unit tests/integration --cov=src --cov-fail-under=85` passes
- [ ] All `config/*.json` files carry `"version": "1.00"`
- [ ] No `import` statements bypass the SDK layer for external calls

### AC-03: Repository
- [ ] Repo is publicly accessible at `https://github.com/salah-dev-stu/uoh-sqak-ex03`
- [ ] ≥50 commits on `main` branch
- [ ] `uv.lock` is committed
- [ ] `.env` is NOT committed; `.env-example` IS committed
- [ ] `latex/output/uoh-sqak-article.pdf` is committed

### AC-04: Submission
- [ ] `uoh-sqak-ex03.pdf` generated via `scripts/fill_submission_pdf.py`
- [ ] Uploaded to Moodle id=270973 by Salah Qadah (ID 323039974)
- [ ] Uploaded to Moodle id=270973 by Andalus Kalash (ID 211435797)
- [ ] Self-grade: 85

---

## 8. Out of Scope

- Hierarchical CrewAI process (would add complexity without grading benefit)
- Mixed LLM providers per agent (voice inconsistency, extra API key management)
- Overleaf — Dr. Segal explicitly forbade it: "I insist" (Lecture 6, L1698)
- Web UI or REST API
- Real-time streaming output
- Article content accuracy (grading is "on the envelope" — structure, not correctness)
- Automatic Moodle upload (manual step required)
- Windows support (not tested; macOS + Linux only)

---

## 9. Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| crewai | ≥0.80.0 | Multi-agent framework |
| langchain-anthropic | ≥0.3.0 | Claude LLM integration |
| duckduckgo-search | ≥7.0.0 | Web search (no API key) |
| python-dotenv | ≥1.0.0 | .env loading |
| matplotlib | ≥3.9.0 | Python-generated charts |
| rich | ≥13.0.0 | Terminal menu |
| pytest | ≥8.0.0 | Testing |
| pytest-cov | ≥5.0.0 | Coverage reporting |
| ruff | ≥0.4.0 | Linting |
| pre-commit | ≥3.7.0 | Pre-commit hooks |
| lualatex | system | LaTeX compiler |
| biber | system | Bibliography processor |

---

*PRD Version 1.00 — Approved by Salah Qadah — 2026-06-06*
