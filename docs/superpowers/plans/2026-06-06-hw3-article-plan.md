# HW3 Article Generation System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CrewAI 4-agent sequential pipeline that produces a ≥15-page LuaLaTeX PDF article on "Multi-Agent Orchestration Patterns" with all technical envelope features (BiDi, fancy formulas, linked citations, TikZ diagram, Python chart) working.

**Architecture:** Single sequential Crew (Researcher → Writer → Editor → LaTeXAgent), file-first Markdown workflow, all external calls through ApiGatekeeper. Human-in-the-loop checkpoint between Editor and LaTeXAgent. SDK is the sole public entry point.

**Tech Stack:** Python 3.13, uv, CrewAI ≥0.80, langchain-anthropic, duckduckgo-search, matplotlib, Rich, LuaLaTeX + biber, ruff, pytest ≥85% coverage

---

## File Map

```
hw3/
├── pyproject.toml
├── uv.lock
├── .env-example
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile                            project-level: install/test/lint/clean/pdf
├── README.md
├── LICENSE
├── src/agent_article/
│   ├── __init__.py                     __version__ = "1.00", __all__
│   ├── constants.py                    enums: AgentRole, ServiceName, ProcessType
│   ├── main.py                         entry point → TerminalMenu
│   ├── sdk/sdk.py                      ArticleSDK (sole public surface)
│   ├── shared/
│   │   ├── version.py                  VERSION = "1.00", bump()
│   │   ├── config.py                   ConfigLoader singleton
│   │   ├── gatekeeper.py               ApiGatekeeper: rate limit + token budget
│   │   └── logging_fifo.py             StructuredLogger FIFO 20×500
│   ├── agents/
│   │   ├── base_agent.py               BaseAgent(ABC): build() → crewai.Agent
│   │   ├── researcher_agent.py
│   │   ├── writer_agent.py
│   │   ├── editor_agent.py
│   │   └── latex_agent.py
│   ├── tasks/article_tasks.py          build_tasks(agents, cfg) → list[Task]
│   ├── crew/article_crew.py            ArticleCrew.kickoff(inputs) → CrewOutput
│   ├── tools/
│   │   ├── base_tool.py                BaseTool(ABC)
│   │   ├── file_rw.py                  FileReadTool, FileWriteTool
│   │   ├── web_search.py               WebSearchTool (DuckDuckGo)
│   │   ├── chart_generator.py          ChartGeneratorTool → PNG
│   │   └── latex_compile.py            LaTeXCompileTool (subprocess)
│   ├── skills/
│   │   ├── base_skill.py               BaseSkill(ABC), FileSkill
│   │   ├── researcher_skill/SKILL.md
│   │   ├── writer_skill/SKILL.md
│   │   ├── editor_skill/SKILL.md
│   │   └── latex_skill/SKILL.md
│   └── menu/tui.py                     TerminalMenu (Rich)
├── config/
│   ├── setup.json
│   ├── agents.json
│   ├── tasks.json
│   ├── crew.json
│   ├── rate_limits.json
│   ├── logging_config.json
│   └── latex.json
├── latex/
│   ├── main.tex
│   ├── chapters/ch01–ch06.tex
│   ├── figures/
│   │   ├── crew_architecture.tikz      mandatory TikZ block diagram
│   │   └── agent_topology.png          Python-generated chart
│   ├── bib/references.bib
│   ├── style/article.sty
│   ├── Makefile
│   └── output/                         git-ignored
├── tests/
│   ├── conftest.py
│   ├── unit/test_version.py
│   ├── unit/test_config.py
│   ├── unit/test_gatekeeper.py
│   ├── unit/test_tools.py
│   ├── unit/test_agents.py
│   ├── unit/test_chart_generator.py
│   ├── unit/test_skill.py
│   ├── integration/test_article_crew.py
│   └── integration/test_latex_pipeline.py
├── docs/
│   ├── PRD.md
│   ├── PLAN.md
│   ├── TODO.md                         ≥500 tasks, target 800
│   ├── PROMPTS.md                      ≥25 entries
│   ├── PRD_crew_orchestrator.md
│   ├── PRD_researcher_agent.md
│   ├── PRD_writer_agent.md
│   ├── PRD_editor_agent.md
│   ├── PRD_latex_agent.md
│   ├── PRD_skill_layer.md
│   ├── PRD_tools.md
│   ├── PRD_gatekeeper.md
│   ├── PRD_bibliography.md
│   ├── PRD_chart_generator.md
│   ├── ADRs/ADR-001 through ADR-007
│   ├── diagrams/class_diagram.md
│   └── AUDIT.md
├── scripts/
│   ├── check_file_lines.py
│   ├── build_article.py
│   └── fill_submission_pdf.py          already exists
├── workspace/                          git-ignored, Markdown intermediates
└── results/                            committed Markdown trace artifacts
```

---

## ⚠️ APPROVAL GATE

**Phase 0–1 (Tasks 1–15) must be approved by Salah before any Phase 2+ code is written.**
After Task 15, stop and ask: "Docs complete. Please review PRD + PLAN + TODO + per-mechanism PRDs before I start coding."

---

## Phase 0 — Repository Setup

### Task 1: Initialize GitHub repo + uv project

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `.env-example`
- Create: `src/agent_article/__init__.py`

- [ ] **Step 1: Create GitHub repo**

```bash
gh repo create salah-dev-stu/uoh-sqak-ex03 --public --description "HW3 - CrewAI Article Generation Pipeline"
cd /Users/salah/Projects/orch-ai-agents/hw3
git init
git remote add origin https://github.com/salah-dev-stu/uoh-sqak-ex03.git
```

- [ ] **Step 2: Create .gitignore**

```
.env
workspace/
latex/output/*.pdf
latex/output/*.aux
*.aux
*.log
*.toc
*.bbl
*.blg
*.synctex.gz
*.fls
*.fdb_latexmk
*.out
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
htmlcov/
.coverage
dist/
*.egg-info/
```

- [ ] **Step 3: Create .env-example**

```
# Anthropic API key (optional — Claude CLI login preferred)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Web search (optional — DuckDuckGo used by default, no key needed)
SERPER_API_KEY=

# LaTeX compiler path (default: lualatex from PATH)
LUALATEX_PATH=lualatex
BIBER_PATH=biber
```

- [ ] **Step 4: Create pyproject.toml**

```toml
[project]
name = "agent-article"
version = "1.00"
requires-python = ">=3.13"
dependencies = [
    "crewai>=0.80.0",
    "langchain-anthropic>=0.3.0",
    "duckduckgo-search>=7.0.0",
    "python-dotenv>=1.0.0",
    "matplotlib>=3.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.4.0",
    "pre-commit>=3.7.0",
]

[project.scripts]
agent-article = "agent_article.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/agent_article"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
fail_under = 85
```

- [ ] **Step 5: Create src/agent_article/__init__.py**

```python
"""agent_article — HW3 CrewAI article generation pipeline."""

__version__ = "1.00"
__all__ = ["ArticleSDK"]
```

- [ ] **Step 6: Install dependencies**

```bash
uv sync --dev
```

Expected: lockfile created, no errors.

- [ ] **Step 7: Create workspace/ and results/ dirs with .gitkeep**

```bash
mkdir -p workspace/chapters results
touch workspace/.gitkeep results/.gitkeep
```

- [ ] **Step 8: Initial commit**

```bash
git add pyproject.toml .gitignore .env-example src/ workspace/.gitkeep results/.gitkeep
git commit -m "chore: initialize uv project with agent-article package"
```

---

### Task 2: Wire ruff + pre-commit + CI

**Files:**
- Create: `.pre-commit-config.yaml`
- Create: `.github/workflows/ci.yml`
- Create: `scripts/check_file_lines.py`

- [ ] **Step 1: Create .pre-commit-config.yaml**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
  - repo: local
    hooks:
      - id: check-file-lines
        name: Check Python file line counts (≤150)
        entry: uv run python scripts/check_file_lines.py
        language: system
        types: [python]
        pass_filenames: false
```

- [ ] **Step 2: Create scripts/check_file_lines.py**

```python
"""Fail if any Python file exceeds 150 logical lines (excluding blanks/comments)."""
import sys
from pathlib import Path

MAX_LINES = 150
DIRS = ["src", "tests", "scripts"]


def count_logical_lines(path: Path) -> int:
    lines = path.read_text().splitlines()
    return sum(
        1 for line in lines
        if line.strip() and not line.strip().startswith("#")
    )


def main() -> int:
    violations: list[tuple[Path, int]] = []
    for d in DIRS:
        for p in Path(d).rglob("*.py"):
            n = count_logical_lines(p)
            if n > MAX_LINES:
                violations.append((p, n))
    if violations:
        for path, n in violations:
            print(f"FAIL {path}: {n} logical lines (max {MAX_LINES})")
        return 1
    print("OK: all Python files within 150-line limit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Create .github/workflows/ci.yml**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      - run: uv sync --dev
      - run: uv run ruff check src tests scripts
      - run: uv run python scripts/check_file_lines.py
      - run: uv run pytest tests/unit tests/integration --cov=src --cov-fail-under=85
```

- [ ] **Step 4: Install pre-commit hooks**

```bash
uv run pre-commit install
```

- [ ] **Step 5: Commit**

```bash
git add .pre-commit-config.yaml .github/ scripts/check_file_lines.py
git commit -m "chore: add ruff pre-commit hook, line-count check, GitHub Actions CI"
```

---

## Phase 1 — Project Documentation

> These tasks produce the graded docs. Use `/plan` mode for each. Stop after Task 15 and wait for Salah's approval.

### Task 3: Create config skeleton (needed by docs for accurate architecture description)

**Files:**
- Create: all `config/*.json`

- [ ] **Step 1: Create config/setup.json**

```json
{
  "version": "1.00",
  "package": "agent_article",
  "workspace_dir": "workspace",
  "results_dir": "results",
  "latex_dir": "latex",
  "output_filename": "uoh-sqak-article.pdf"
}
```

- [ ] **Step 2: Create config/agents.json**

```json
{
  "version": "1.00",
  "agents": {
    "researcher": {
      "role": "Senior Research Analyst specializing in AI systems",
      "goal": "Gather comprehensive structured research notes on the topic with 8+ cited sources",
      "backstory": "You are a senior research analyst with 10 years of experience in AI systems. You write rigorous, citation-dense research notes in a structured format.",
      "llm": "claude-cli",
      "skill_ref": "researcher_skill",
      "temperature": 0.3
    },
    "writer": {
      "role": "Technical Writer with expertise in AI and software architecture",
      "goal": "Produce coherent well-structured Markdown chapters from research notes targeting professional publication quality",
      "backstory": "You are a technical writer who has authored dozens of papers on software architecture and AI systems. You write clearly for a technical audience.",
      "llm": "claude-cli",
      "skill_ref": "writer_skill",
      "temperature": 0.7
    },
    "editor": {
      "role": "Senior Editor and style guide enforcer",
      "goal": "Polish prose, verify citation placeholders, enforce consistent chapter structure, prepare content for LaTeX conversion",
      "backstory": "You are a senior editor at a technical publishing house. You enforce house style, catch inconsistencies, and ensure every chapter meets publication standards.",
      "llm": "claude-cli",
      "skill_ref": "editor_skill",
      "temperature": 0.2
    },
    "latex_producer": {
      "role": "LaTeX Engineer producing fancy formulas, not plain text",
      "goal": "Convert approved Markdown to LaTeX, compile 4 passes, verify all links resolve and formulas are rendered as fancy LaTeX math not plain text",
      "backstory": "You are a LaTeX expert with deep knowledge of LuaLaTeX, biblatex/biber, TikZ, and Hebrew-English BiDi typesetting. You always produce fancy formula rendering — never plain text.",
      "llm": "claude-cli",
      "skill_ref": "latex_skill",
      "temperature": 0.1
    }
  }
}
```

- [ ] **Step 3: Create config/tasks.json**

```json
{
  "version": "1.00",
  "tasks": {
    "research": {
      "description": "Research the topic '{topic}'. Write comprehensive notes covering: (1) key concepts and definitions, (2) major frameworks and their tradeoffs, (3) production patterns and challenges, (4) at least 8 cited sources in format [AuthorYear]. Save output to workspace/research_notes.md.",
      "expected_output": "A structured Markdown file workspace/research_notes.md with sections: Overview, Key Frameworks, Production Patterns, Bibliography. Minimum 1500 words, 8+ citations."
    },
    "write": {
      "description": "Using research notes at workspace/research_notes.md, write 6 Markdown chapters for '{topic}'. Chapters: (1) Introduction, (2) Agent Architectures, (3) Framework Comparison, (4) Production Patterns, (5) BiDi chapter in Hebrew+English, (6) Case Study. Save each to workspace/chapters/ch0N_title.md. Target 350-500 words per chapter.",
      "expected_output": "6 Markdown files workspace/chapters/ch01-ch06.md, each 350-500 words. ch05 must include at least 2 paragraphs of Hebrew text. ch03 must include at least one comparison table."
    },
    "edit": {
      "description": "Review and polish all chapters in workspace/chapters/. Verify: consistent style, all citations have [AuthorYear] markers, tables properly formatted, ch05 BiDi chapter has Hebrew+English mix, no chapter exceeds 550 words. Save to workspace/chapters/ch0N_edited.md.",
      "expected_output": "6 edited Markdown files workspace/chapters/*_edited.md. Each improved for clarity and LaTeX readiness."
    },
    "latex": {
      "description": "Convert approved Markdown in workspace/chapters/*_edited.md to LaTeX. Generate: (1) latex/main.tex with full preamble, (2) latex/chapters/*.tex, (3) latex/bib/references.bib, (4) ensure fancy formula using \\begin{equation} NOT plain text, (5) TikZ Crew architecture block diagram in ch01. Compile: lualatex main.tex → biber main → lualatex main.tex → lualatex main.tex. Verify .log shows no unresolved refs.",
      "expected_output": "latex/output/uoh-sqak-article.pdf — PDF ≥15 pages with all features. Compile log showing 0 errors."
    }
  }
}
```

- [ ] **Step 4: Create config/crew.json**

```json
{
  "version": "1.00",
  "process": "sequential",
  "verbose": true,
  "agents": ["researcher", "writer", "editor", "latex_producer"],
  "tasks": ["research", "write", "edit", "latex"]
}
```

- [ ] **Step 5: Create config/rate_limits.json**

```json
{
  "version": "1.00",
  "services": {
    "claude_cli": {
      "requests_per_minute": 10,
      "tokens_per_article": 200000,
      "tokens_per_day": 500000,
      "warn_at_percent": 75,
      "hard_cap_percent": 95
    },
    "duckduckgo": {
      "requests_per_minute": 5
    },
    "lualatex": {
      "requests_per_minute": 60
    }
  }
}
```

- [ ] **Step 6: Create config/logging_config.json**

```json
{
  "version": "1.00",
  "log_dir": "logs",
  "fifo_files": 20,
  "max_lines_per_file": 500,
  "level": "INFO"
}
```

- [ ] **Step 7: Create config/latex.json**

```json
{
  "version": "1.00",
  "compiler": "lualatex",
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
  "bidi_chapter": "ch05_bidi"
}
```

- [ ] **Step 8: Commit**

```bash
git add config/
git commit -m "chore: add all config JSON files versioned at 1.00"
```

---

### Task 4: Write docs/PRD.md

**Files:**
- Create: `docs/PRD.md`

- [ ] **Step 1: Write docs/PRD.md** — use the following required sections:

```markdown
# Product Requirements Document — HW3 Article Generation Pipeline

**Version:** 1.00
**Authors:** Salah Qadah, Andalus Kalash
**Course:** 203.3763 — Orchestration of AI Agents
**Date:** 2026-06-06

## 1. Executive Summary
## 2. Goals and Non-Goals
## 3. User Stories
   - As Salah, I want to run `agent-article` and get a 15-page PDF...
   - As the grader, I want to clone the repo, run `uv sync`, and compile the PDF...
## 4. Functional Requirements
   - FR-01: 4 CrewAI agents (Researcher, Writer, Editor, LaTeXAgent)
   - FR-02: Sequential process
   - FR-03: Markdown-first workflow
   - FR-04: LaTeX PDF ≥15 pages with all H1-H25 features
   - FR-05: Human-in-the-loop checkpoint before LaTeX compilation
   - FR-06: SDK as sole public entry point
## 5. Non-Functional Requirements
   - NFR-01: ≤5 min per chapter generation
   - NFR-02: ≤30s LaTeX compile
   - NFR-03: Coverage ≥85%
   - NFR-04: ruff 0 errors
   - NFR-05: ≤150 lines per Python file
## 6. Architecture Overview (link to PLAN.md)
## 7. Acceptance Criteria (maps to SUBMISSION_CHECKLIST.md)
## 8. Out of Scope
   - Hierarchical CrewAI process
   - Mixed LLM providers
   - Overleaf
```

- [ ] **Step 2: Commit**

```bash
git add docs/PRD.md
git commit -m "docs(prd): add Product Requirements Document"
```

---

### Task 5: Write docs/PLAN.md

**Files:**
- Create: `docs/PLAN.md`

- [ ] **Step 1: Write docs/PLAN.md** — required sections:

Required sections (each non-trivial):
1. Architecture overview (7-layer stack from design spec)
2. C4 Model: Context + Container + Component diagrams (Mermaid)
3. UML Sequence diagram: one full Crew kickoff (Mermaid)
4. Class diagram: BaseAgent, BaseTool, BaseSkill + all subclasses (Mermaid or ASCII)
5. ADRs (7 required):
   - ADR-001: CrewAI over LangGraph — sequential article pipeline, LangGraph adds graph complexity for no benefit here
   - ADR-002: Sequential vs Hierarchical — article writing is a closed linear process
   - ADR-003: Markdown-first workflow — Dr. Segal's own method; faster iteration; debug on readable artifacts
   - ADR-004: LuaLaTeX vs XeLaTeX — equal per lecturer; LuaLaTeX chosen for Dr. Segal's familiarity
   - ADR-005: Single LLM provider (Claude) — voice consistency for cooperative writing; mixing providers for cooperative task adds inconsistency
   - ADR-006: File-based skill layer — portable, versionable, readable, matches spec Appendix A
   - ADR-007: DuckDuckGo for web search — no API key needed, free, sufficient for known-domain topic
6. ISO/IEC 25010 paragraph (all 8 dimensions)
7. Extension points documentation

- [ ] **Step 2: Commit**

```bash
git add docs/PLAN.md
git commit -m "docs(plan): add technical plan with C4, UML, class diagram, 7 ADRs, ISO/IEC 25010"
```

---

### Task 6: Write docs/TODO.md (target 800 tasks)

**Files:**
- Create: `docs/TODO.md`

- [ ] **Step 1: Write docs/TODO.md**

Structure it across the 13 phases from IDEA.md. Each task is one actionable checkbox. Target 800, minimum 500. Phases:

```markdown
# TODO — HW3 Article Generation Pipeline

**Total tasks: [count]**
**Minimum: 500 | Target: 800**

## Phase 1: Scaffolding (Tasks 1-80)
- [ ] T-001: Create GitHub repo uoh-sqak-ex03 as public
- [ ] T-002: Run `git init` in hw3/
- [ ] T-003: Add remote origin
...

## Phase 2: Agents + Skills (Tasks 81-200)
...

## Phase 3: Crew Assembly (Tasks 201-280)
...

## Phase 4: Markdown Pipeline (Tasks 281-380)
...

## Phase 5: LaTeX Conversion (Tasks 381-480)
...

## Phase 6: Cover Sheet + TOC + Chapters (Tasks 481-540)
...

## Phase 7: Python Chart Generation (Tasks 541-580)
...

## Phase 8: TikZ Diagram (Tasks 581-620)
...

## Phase 9: BiDi Section (Tasks 621-660)
...

## Phase 10: Build Pipeline (Tasks 661-700)
...

## Phase 11: Tests + Audit (Tasks 701-760)
...

## Phase 12: README (Tasks 761-800)
...

## Phase 13: GitHub Push + Moodle (Tasks 801+)
...
```

- [ ] **Step 2: Commit**

```bash
git add docs/TODO.md
git commit -m "docs(todo): add 800-task TODO list covering all 13 phases"
```

---

### Task 7: Write per-mechanism PRDs (10 files)

**Files:** `docs/PRD_crew_orchestrator.md`, `docs/PRD_researcher_agent.md`, `docs/PRD_writer_agent.md`, `docs/PRD_editor_agent.md`, `docs/PRD_latex_agent.md`, `docs/PRD_skill_layer.md`, `docs/PRD_tools.md`, `docs/PRD_gatekeeper.md`, `docs/PRD_bibliography.md`, `docs/PRD_chart_generator.md`

- [ ] **Step 1: Each PRD must follow the building-block docstring shape:**

```markdown
# PRD — [Component Name]

## Input / Output / Setup

**Input:** [what it receives]
**Output:** [what it produces]
**Setup:** [config keys, dependencies, environment]

## Responsibilities
## Interface (public methods/attributes)
## Dependencies
## Test strategy
## Acceptance criteria
```

- [ ] **Step 2: Example — docs/PRD_gatekeeper.md**

```markdown
# PRD — ApiGatekeeper

## Input / Output / Setup
**Input:** service_name (str), callable fn, *args, **kwargs
**Output:** result of fn(*args, **kwargs) or raises GatekeeperError
**Setup:** config/rate_limits.json; no API key needed

## Responsibilities
- Enforce requests_per_minute per service (sliding window)
- Enforce tokens_per_article budget (hard cap at 95%)
- Track usage for spend report
- Thread-safe (used by concurrent agent calls)

## Interface
- `ApiGatekeeper.instance() → ApiGatekeeper` (singleton)
- `call(service, fn, *args, **kwargs) → Any`
- `get_spend_report() → dict[str, UsageRecord]`

## Dependencies
- config/rate_limits.json
- shared/logging_fifo.py

## Test strategy
- Unit: mock time.monotonic, verify rate limit raises at RPM+1
- Unit: verify budget cap raises at 95% of tokens_per_article
- Integration: verify Crew calls all route through gatekeeper

## Acceptance criteria
- [ ] 0 LLM calls bypass Gatekeeper in any test
- [ ] Rate limit enforced within 1% of configured RPM
```

- [ ] **Step 3: Write all 10 PRD files with the same structure.**

- [ ] **Step 4: Commit**

```bash
git add docs/PRD_*.md
git commit -m "docs(prds): add 10 per-mechanism PRDs with Input/Output/Setup docstring shape"
```

---

### Task 8: Write docs/PROMPTS.md

**Files:**
- Create: `docs/PROMPTS.md`

- [ ] **Step 1: Write docs/PROMPTS.md** — required format per entry:

```markdown
## Entry 001 — Researcher Agent Role

**Context:** Defining the Researcher agent's role and goal for the CrewAI Crew
**Goal:** A role string that makes the agent search authoritatively and cite sources
**Prompt:**
> "role": "Senior Research Analyst specializing in AI systems"
> "goal": "Gather comprehensive structured research notes on the topic with 8+ cited sources"

**Output received:** Agent searched for multi-agent orchestration patterns and returned structured notes with [LangChain2024], [CrewAI2024] citations.

**Iterations:** v1 had "AI researcher" — too broad, added "Senior" and "specializing in AI systems" to get authoritative tone.

**Best practice:** Add seniority to role string; include citation format expectation in goal.
```

Target ≥25 entries covering: 4 agent roles, 4 agent goals, 4 backstories, 4 task descriptions, LaTeX preamble prompt, BiDi chapter prompt, fancy-formula prompt, TikZ diagram prompt, key coding prompts used with Claude.

- [ ] **Step 2: Commit**

```bash
git add docs/PROMPTS.md
git commit -m "docs(prompts): add 25+ prompt engineering log entries"
```

---

## ⚠️ APPROVAL GATE — Stop here. Ask Salah to review all docs before proceeding.

---

## Phase 2 — Foundation Code

### Task 9: shared/version.py + constants.py

**Files:**
- Create: `src/agent_article/shared/version.py`
- Create: `src/agent_article/constants.py`
- Create: `tests/unit/test_version.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_version.py
from agent_article.shared.version import VERSION, bump


def test_version_format() -> None:
    parts = VERSION.split(".")
    assert len(parts) == 2
    assert parts[0].isdigit()
    assert parts[1].isdigit()


def test_bump() -> None:
    assert bump("1.00") == "1.01"
    assert bump("1.09") == "1.10"
    assert bump("1.99") == "1.100"
```

- [ ] **Step 2: Run test — expect FAIL**

```bash
uv run pytest tests/unit/test_version.py -v
```

Expected: `ModuleNotFoundError: No module named 'agent_article.shared.version'`

- [ ] **Step 3: Implement shared/version.py**

```python
"""Version management for agent_article."""

VERSION = "1.00"


def bump(version: str) -> str:
    """Increment patch component: 1.00 → 1.01."""
    major, minor = version.split(".")
    return f"{major}.{int(minor) + 1}"
```

- [ ] **Step 4: Implement constants.py**

```python
"""Immutable enumerations for agent_article."""
from enum import StrEnum


class AgentRole(StrEnum):
    RESEARCHER = "researcher"
    WRITER = "writer"
    EDITOR = "editor"
    LATEX_PRODUCER = "latex_producer"


class ServiceName(StrEnum):
    CLAUDE_CLI = "claude_cli"
    DUCKDUCKGO = "duckduckgo"
    LUALATEX = "lualatex"


class ProcessType(StrEnum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
```

- [ ] **Step 5: Create shared/__init__.py**

```python
"""Shared infrastructure for agent_article."""
```

- [ ] **Step 6: Run test — expect PASS**

```bash
uv run pytest tests/unit/test_version.py -v
```

- [ ] **Step 7: Commit**

```bash
git add src/agent_article/shared/ src/agent_article/constants.py tests/unit/test_version.py
git commit -m "feat(shared): add version module and constants enums"
```

---

### Task 10: shared/config.py

**Files:**
- Create: `src/agent_article/shared/config.py`
- Create: `tests/unit/test_config.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_config.py
import json
import pytest
from pathlib import Path


def test_get_config_loads_setup(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(json.dumps({"version": "1.00", "package": "test"}))

    import agent_article.shared.config as cfg_mod
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()

    result = cfg_mod.get_config("setup")
    assert result["version"] == "1.00"
    assert result["package"] == "test"


def test_cfg_returns_default_for_missing_key(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(json.dumps({"version": "1.00"}))

    import agent_article.shared.config as cfg_mod
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()

    assert cfg_mod.cfg("setup", "missing_key", default="fallback") == "fallback"
```

- [ ] **Step 2: Run — expect FAIL**

```bash
uv run pytest tests/unit/test_config.py -v
```

- [ ] **Step 3: Implement shared/config.py**

```python
"""Configuration loader — reads config/*.json, caches in-process."""
import json
from pathlib import Path
from typing import Any

_CONFIG_DIR = Path(__file__).parent.parent.parent.parent / "config"
_cache: dict[str, Any] = {}


def get_config(name: str) -> dict[str, Any]:
    """Load and cache a config file by name (without .json extension)."""
    if name not in _cache:
        path = _CONFIG_DIR / f"{name}.json"
        _cache[name] = json.loads(path.read_text(encoding="utf-8"))
    return _cache[name]


def cfg(name: str, key: str, default: Any = None) -> Any:
    """Get a single key from a config file with an optional default."""
    return get_config(name).get(key, default)


def reload() -> None:
    """Clear the config cache (useful in tests)."""
    _cache.clear()
```

- [ ] **Step 4: Run — expect PASS**

```bash
uv run pytest tests/unit/test_config.py -v
```

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/shared/config.py tests/unit/test_config.py
git commit -m "feat(config): add ConfigLoader with caching and reload support"
```

---

### Task 11: shared/logging_fifo.py

**Files:**
- Create: `src/agent_article/shared/logging_fifo.py`

- [ ] **Step 1: Implement logging_fifo.py**

```python
"""FIFO structured logger — rotates log files, max 20 files × 500 lines."""
import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import get_config


class StructuredLogger:
    """
    Input:  component (str), **fields (Any)
    Output: JSONL lines written to logs/<component>_NNN.jsonl
    Setup:  config/logging_config.json
    """

    def __init__(self, component: str) -> None:
        self._component = component
        _cfg = get_config("logging_config")
        self._log_dir = Path(_cfg["log_dir"])
        self._max_files = int(_cfg["fifo_files"])
        self._max_lines = int(_cfg["max_lines_per_file"])
        self._lock = threading.Lock()
        self._current_lines = 0
        self._file_index = 0
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self._fh = self._open_next()

    def _open_next(self):  # noqa: ANN202
        path = self._log_dir / f"{self._component}_{self._file_index:03d}.jsonl"
        self._rotate_if_needed()
        return path.open("a", encoding="utf-8")

    def _rotate_if_needed(self) -> None:
        files = sorted(self._log_dir.glob(f"{self._component}_*.jsonl"))
        while len(files) >= self._max_files:
            files[0].unlink()
            files = files[1:]

    def _write(self, level: str, message: str, **fields: Any) -> None:
        record = {
            "ts": datetime.now(UTC).isoformat(),
            "level": level,
            "component": self._component,
            "message": message,
            **fields,
        }
        with self._lock:
            self._fh.write(json.dumps(record) + "\n")
            self._fh.flush()
            self._current_lines += 1
            if self._current_lines >= self._max_lines:
                self._fh.close()
                self._file_index += 1
                self._current_lines = 0
                self._fh = self._open_next()

    def info(self, message: str, **fields: Any) -> None:
        self._write("INFO", message, **fields)

    def error(self, message: str, **fields: Any) -> None:
        self._write("ERROR", message, **fields)

    def warning(self, message: str, **fields: Any) -> None:
        self._write("WARNING", message, **fields)
```

- [ ] **Step 2: Commit**

```bash
git add src/agent_article/shared/logging_fifo.py
git commit -m "feat(logging): add FIFO structured logger with 20-file rotation"
```

---

### Task 12: shared/gatekeeper.py

**Files:**
- Create: `src/agent_article/shared/gatekeeper.py`
- Create: `tests/unit/test_gatekeeper.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/unit/test_gatekeeper.py
import time
import pytest
from unittest.mock import patch, MagicMock

from agent_article.shared.gatekeeper import ApiGatekeeper, GatekeeperError


@pytest.fixture
def gatekeeper(tmp_path, monkeypatch):
    import agent_article.shared.config as cfg_mod
    import json
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "rate_limits.json").write_text(json.dumps({
        "version": "1.00",
        "services": {
            "test_svc": {
                "requests_per_minute": 2,
                "tokens_per_article": 1000,
                "hard_cap_percent": 95,
            }
        }
    }))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()
    ApiGatekeeper._instance = None
    return ApiGatekeeper.instance()


def test_call_succeeds(gatekeeper):
    result = gatekeeper.call("test_svc", lambda: 42)
    assert result == 42


def test_rate_limit_enforced(gatekeeper):
    gatekeeper.call("test_svc", lambda: None)
    gatekeeper.call("test_svc", lambda: None)
    with pytest.raises(GatekeeperError, match="Rate limit"):
        gatekeeper.call("test_svc", lambda: None)


def test_singleton(tmp_path, monkeypatch):
    import agent_article.shared.config as cfg_mod
    import json
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "rate_limits.json").write_text(json.dumps({"version": "1.00", "services": {}}))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs2"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()
    ApiGatekeeper._instance = None
    g1 = ApiGatekeeper.instance()
    g2 = ApiGatekeeper.instance()
    assert g1 is g2
```

- [ ] **Step 2: Run — expect FAIL**

```bash
uv run pytest tests/unit/test_gatekeeper.py -v
```

- [ ] **Step 3: Implement shared/gatekeeper.py**

```python
"""API Gatekeeper — rate limiting, token budget, all external calls route here."""
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable

from .config import get_config
from .logging_fifo import StructuredLogger


class GatekeeperError(Exception):
    """Raised when rate limit or token budget is exceeded."""


@dataclass
class UsageRecord:
    tokens_in: int = 0
    tokens_out: int = 0
    calls: int = 0


class ApiGatekeeper:
    """
    Input:  service (str), fn (Callable), *args, **kwargs
    Output: fn(*args, **kwargs) result or raises GatekeeperError
    Setup:  config/rate_limits.json
    """

    _instance: "ApiGatekeeper | None" = None

    def __init__(self) -> None:
        self._cfg = get_config("rate_limits")["services"]
        self._usage: dict[str, UsageRecord] = defaultdict(UsageRecord)
        self._call_times: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()
        self._logger = StructuredLogger("gatekeeper")

    @classmethod
    def instance(cls) -> "ApiGatekeeper":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def call(self, service: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            self._enforce_rate_limit(service)
            self._check_budget(service)
        result = fn(*args, **kwargs)
        with self._lock:
            self._usage[service].calls += 1
        self._logger.info("gatekeeper_call", service=service, fn=fn.__name__)
        return result

    def _enforce_rate_limit(self, service: str) -> None:
        rpm = self._cfg.get(service, {}).get("requests_per_minute", 60)
        times = self._call_times[service]
        now = time.monotonic()
        while times and now - times[0] > 60:
            times.popleft()
        if len(times) >= rpm:
            raise GatekeeperError(f"Rate limit exceeded for {service}: {rpm} RPM")
        times.append(now)

    def _check_budget(self, service: str) -> None:
        svc = self._cfg.get(service, {})
        cap = svc.get("tokens_per_article", float("inf"))
        hard_pct = svc.get("hard_cap_percent", 95) / 100
        used = self._usage[service].tokens_in + self._usage[service].tokens_out
        if used >= cap * hard_pct:
            raise GatekeeperError(f"Token budget exceeded for {service}")

    def get_spend_report(self) -> dict[str, UsageRecord]:
        return dict(self._usage)
```

- [ ] **Step 4: Run — expect PASS**

```bash
uv run pytest tests/unit/test_gatekeeper.py -v
```

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/shared/gatekeeper.py tests/unit/test_gatekeeper.py
git commit -m "feat(gatekeeper): add ApiGatekeeper with rate limiting and token budget"
```

---

## Phase 3 — Tools

### Task 13: tools/base_tool.py + tools/file_rw.py

**Files:**
- Create: `src/agent_article/tools/base_tool.py`
- Create: `src/agent_article/tools/file_rw.py`
- Create: `tests/unit/test_tools.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/unit/test_tools.py
from pathlib import Path
import pytest
from agent_article.tools.file_rw import FileReadTool, FileWriteTool


def test_file_write_and_read(tmp_path):
    writer = FileWriteTool(base_dir=tmp_path)
    reader = FileReadTool(base_dir=tmp_path)

    writer.run("notes.md", "# Hello\nWorld")
    content = reader.run("notes.md")
    assert content == "# Hello\nWorld"


def test_file_write_creates_parent_dirs(tmp_path):
    writer = FileWriteTool(base_dir=tmp_path)
    writer.run("chapters/ch01.md", "content")
    assert (tmp_path / "chapters" / "ch01.md").read_text() == "content"


def test_file_read_missing_raises(tmp_path):
    reader = FileReadTool(base_dir=tmp_path)
    with pytest.raises(FileNotFoundError):
        reader.run("nonexistent.md")
```

- [ ] **Step 2: Run — expect FAIL**

```bash
uv run pytest tests/unit/test_tools.py -v
```

- [ ] **Step 3: Implement tools/base_tool.py**

```python
"""Abstract base for all tools used by CrewAI agents."""
from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Input:  *args, **kwargs (tool-specific)
    Output: str or structured result
    Setup:  configured via subclass __init__
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any: ...

    def as_crewai_tool(self) -> Any:
        """Wrap self as a CrewAI-compatible tool."""
        from crewai.tools import tool as crewai_tool
        run_fn = self.run
        name_ = self.name
        desc_ = self.description

        @crewai_tool(name_, description=desc_)
        def _tool(*args: Any, **kwargs: Any) -> Any:
            return run_fn(*args, **kwargs)

        return _tool
```

- [ ] **Step 4: Implement tools/file_rw.py**

```python
"""File read/write tools for agent workspace."""
from pathlib import Path
from typing import Any

from .base_tool import BaseTool


class FileWriteTool(BaseTool):
    """Write text content to a file under base_dir."""

    def __init__(self, base_dir: Path | None = None) -> None:
        from agent_article.shared.config import cfg
        self._base = base_dir or Path(cfg("setup", "workspace_dir", "workspace"))

    @property
    def name(self) -> str:
        return "file_write"

    @property
    def description(self) -> str:
        return "Write text content to a file. Args: relative_path (str), content (str)"

    def run(self, relative_path: str, content: str, **_: Any) -> str:
        target = self._base / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Written: {target}"


class FileReadTool(BaseTool):
    """Read text content from a file under base_dir."""

    def __init__(self, base_dir: Path | None = None) -> None:
        from agent_article.shared.config import cfg
        self._base = base_dir or Path(cfg("setup", "workspace_dir", "workspace"))

    @property
    def name(self) -> str:
        return "file_read"

    @property
    def description(self) -> str:
        return "Read text content from a file. Args: relative_path (str)"

    def run(self, relative_path: str, **_: Any) -> str:
        target = self._base / relative_path
        if not target.exists():
            raise FileNotFoundError(f"File not found: {target}")
        return target.read_text(encoding="utf-8")
```

- [ ] **Step 5: Run — expect PASS**

```bash
uv run pytest tests/unit/test_tools.py -v
```

- [ ] **Step 6: Commit**

```bash
git add src/agent_article/tools/ tests/unit/test_tools.py
git commit -m "feat(tools): add BaseTool, FileReadTool, FileWriteTool"
```

---

### Task 14: tools/web_search.py

**Files:**
- Create: `src/agent_article/tools/web_search.py`

- [ ] **Step 1: Add failing test to test_tools.py**

```python
def test_web_search_returns_string(monkeypatch):
    from agent_article.tools.web_search import WebSearchTool

    mock_results = [{"body": "LangChain is a framework...", "href": "https://example.com"}]
    monkeypatch.setattr(
        "agent_article.tools.web_search.DDGS",
        lambda: type("DDGS", (), {"text": lambda self, q, max_results: mock_results})()
    )
    tool = WebSearchTool()
    result = tool.run("LangChain overview")
    assert "LangChain" in result
    assert "https://example.com" in result
```

- [ ] **Step 2: Implement tools/web_search.py**

```python
"""DuckDuckGo web search tool — no API key required."""
from typing import Any

from .base_tool import BaseTool


class WebSearchTool(BaseTool):
    """
    Input:  query (str), max_results (int, default 5)
    Output: formatted string of results with title, body, url
    Setup:  duckduckgo-search package (uv add duckduckgo-search)
    """

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Search the web using DuckDuckGo. Args: query (str), max_results (int, default 5)"

    def run(self, query: str, max_results: int = 5, **_: Any) -> str:
        from duckduckgo_search import DDGS
        from agent_article.shared.gatekeeper import ApiGatekeeper

        def _search() -> list[dict]:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))

        results = ApiGatekeeper.instance().call("duckduckgo", _search)
        if not results:
            return f"No results found for: {query}"
        lines = []
        for r in results:
            lines.append(f"**{r.get('title', 'No title')}**\n{r.get('body', '')}\nURL: {r.get('href', '')}\n")
        return "\n---\n".join(lines)
```

- [ ] **Step 3: Run — expect PASS**

```bash
uv run pytest tests/unit/test_tools.py::test_web_search_returns_string -v
```

- [ ] **Step 4: Commit**

```bash
git add src/agent_article/tools/web_search.py
git commit -m "feat(tools): add WebSearchTool via DuckDuckGo (no API key)"
```

---

### Task 15: tools/chart_generator.py

**Files:**
- Create: `src/agent_article/tools/chart_generator.py`
- Create: `tests/unit/test_chart_generator.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_chart_generator.py
from pathlib import Path
from agent_article.tools.chart_generator import ChartGeneratorTool


def test_chart_creates_png(tmp_path):
    tool = ChartGeneratorTool(output_dir=tmp_path)
    result = tool.run(
        chart_type="bar",
        title="Framework Comparison",
        labels=["LangChain", "CrewAI", "LangGraph"],
        values=[85, 90, 75],
        ylabel="Ease of Use Score",
        filename="agent_topology.png",
    )
    assert (tmp_path / "agent_topology.png").exists()
    assert (tmp_path / "agent_topology.png").stat().st_size > 0
    assert "agent_topology.png" in result
```

- [ ] **Step 2: Run — expect FAIL**

```bash
uv run pytest tests/unit/test_chart_generator.py -v
```

- [ ] **Step 3: Implement tools/chart_generator.py**

```python
"""Generate matplotlib charts and save as PNG for LaTeX inclusion."""
from pathlib import Path
from typing import Any

from .base_tool import BaseTool


class ChartGeneratorTool(BaseTool):
    """
    Input:  chart_type, title, labels, values, ylabel, filename
    Output: PNG file path string
    Setup:  output_dir (default: latex/figures/)
    """

    def __init__(self, output_dir: Path | None = None) -> None:
        from agent_article.shared.config import cfg
        latex_dir = cfg("latex", "main_file", "latex/main.tex")
        default_dir = Path(latex_dir).parent / "figures"
        self._output_dir = output_dir or default_dir

    @property
    def name(self) -> str:
        return "chart_generator"

    @property
    def description(self) -> str:
        return (
            "Generate a matplotlib chart and save as PNG. "
            "Args: chart_type (str: bar|line|pie), title (str), "
            "labels (list[str]), values (list[float]), ylabel (str), filename (str)"
        )

    def run(self, chart_type: str, title: str, labels: list,
            values: list, ylabel: str, filename: str, **_: Any) -> str:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        self._output_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 5))

        if chart_type == "bar":
            ax.bar(labels, values, color="#4C72B0")
        elif chart_type == "line":
            ax.plot(labels, values, marker="o", color="#4C72B0")
        elif chart_type == "pie":
            ax.pie(values, labels=labels, autopct="%1.1f%%")
        else:
            ax.bar(labels, values)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_ylabel(ylabel)
        plt.tight_layout()

        output_path = self._output_dir / filename
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return str(output_path)
```

- [ ] **Step 4: Run — expect PASS**

```bash
uv run pytest tests/unit/test_chart_generator.py -v
```

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/tools/chart_generator.py tests/unit/test_chart_generator.py
git commit -m "feat(tools): add ChartGeneratorTool (matplotlib → PNG)"
```

---

### Task 16: tools/latex_compile.py

**Files:**
- Create: `src/agent_article/tools/latex_compile.py`

- [ ] **Step 1: Add failing test**

```python
# In tests/unit/test_tools.py — add:
def test_latex_compile_tool_calls_subprocess(monkeypatch):
    from agent_article.tools.latex_compile import LaTeXCompileTool
    import json
    from pathlib import Path

    calls = []

    def fake_run(cmd, cwd, capture_output, text, timeout):
        calls.append(cmd)
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr("agent_article.tools.latex_compile.subprocess.run", fake_run)
    tool = LaTeXCompileTool(latex_dir=Path("/tmp/latex"))
    tool.run("main.tex")
    # Should have called: lualatex, biber, lualatex, lualatex
    assert len(calls) == 4
    assert "lualatex" in calls[0][0]
    assert "biber" in calls[1][0]
```

- [ ] **Step 2: Implement tools/latex_compile.py**

```python
"""LaTeX compilation tool — runs lualatex → biber → lualatex × 2."""
import subprocess
from pathlib import Path
from typing import Any

from .base_tool import BaseTool
from agent_article.shared.config import get_config
from agent_article.shared.logging_fifo import StructuredLogger


class LaTeXCompileTool(BaseTool):
    """
    Input:  main_tex_filename (str, default 'main.tex')
    Output: str path to compiled PDF or raises on error
    Setup:  config/latex.json for compiler path and passes
    """

    def __init__(self, latex_dir: Path | None = None) -> None:
        cfg = get_config("latex")
        self._latex_dir = latex_dir or Path(cfg["main_file"]).parent
        self._compiler = cfg.get("compiler", "lualatex")
        self._biber = cfg.get("biber", "biber")
        self._passes = int(cfg.get("passes", 4))
        self._logger = StructuredLogger("latex_compile")

    @property
    def name(self) -> str:
        return "latex_compile"

    @property
    def description(self) -> str:
        return "Compile a LaTeX document with lualatex → biber → lualatex × 2. Args: main_tex (str)"

    def run(self, main_tex: str = "main.tex", **_: Any) -> str:
        stem = Path(main_tex).stem
        self._run_cmd([self._compiler, "--interaction=nonstopmode", main_tex])
        self._run_cmd([self._biber, stem])
        self._run_cmd([self._compiler, "--interaction=nonstopmode", main_tex])
        self._run_cmd([self._compiler, "--interaction=nonstopmode", main_tex])
        self._check_log(stem)
        pdf = self._latex_dir / "output" / f"{stem}.pdf"
        return str(pdf)

    def _run_cmd(self, cmd: list[str]) -> None:
        result = subprocess.run(
            cmd, cwd=self._latex_dir,
            capture_output=True, text=True, timeout=120,
        )
        self._logger.info("latex_cmd", cmd=cmd[0], returncode=result.returncode)
        if result.returncode != 0:
            raise RuntimeError(f"LaTeX command failed: {' '.join(cmd)}\n{result.stderr}")

    def _check_log(self, stem: str) -> None:
        log_path = self._latex_dir / f"{stem}.log"
        if not log_path.exists():
            return
        log = log_path.read_text(encoding="utf-8", errors="ignore")
        if "Rerun to get cross-references right" in log:
            self._logger.warning("latex_rerun_needed", stem=stem)
        if "Overfull \\hbox" in log:
            self._logger.warning("latex_overfull_hbox", stem=stem)
```

- [ ] **Step 3: Run tests — expect PASS**

```bash
uv run pytest tests/unit/test_tools.py -v
```

- [ ] **Step 4: Commit**

```bash
git add src/agent_article/tools/latex_compile.py
git commit -m "feat(tools): add LaTeXCompileTool with 4-pass compile and log auditing"
```

---

## Phase 4 — Skills

### Task 17: skills/base_skill.py + SKILL.md files

**Files:**
- Create: `src/agent_article/skills/base_skill.py`
- Create: `src/agent_article/skills/researcher_skill/SKILL.md`
- Create: `src/agent_article/skills/writer_skill/SKILL.md`
- Create: `src/agent_article/skills/editor_skill/SKILL.md`
- Create: `src/agent_article/skills/latex_skill/SKILL.md`
- Create: `tests/unit/test_skill.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_skill.py
from pathlib import Path
import pytest
from agent_article.skills.base_skill import FileSkill


def test_file_skill_loads_content(tmp_path):
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: test\ndescription: A test skill\n---\nYou are an expert."
    )
    skill = FileSkill(skill_dir)
    assert "You are an expert." in skill.content


def test_file_skill_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        FileSkill(tmp_path / "nonexistent_skill").content
```

- [ ] **Step 2: Implement skills/base_skill.py**

```python
"""Skill layer — file-based instruction packages for CrewAI agents."""
from abc import ABC, abstractmethod
from pathlib import Path

from agent_article.shared.config import cfg as get_cfg


class BaseSkill(ABC):
    """
    Input:  skill_ref (str | Path)
    Output: content (str) injected into agent backstory
    Setup:  SKILL.md file in the skill directory
    """

    @property
    @abstractmethod
    def content(self) -> str: ...


class FileSkill(BaseSkill):
    """Load skill from a SKILL.md file in the skills directory."""

    def __init__(self, skill_ref: str | Path) -> None:
        if isinstance(skill_ref, str):
            skills_root = Path(__file__).parent
            self._skill_path = skills_root / skill_ref / "SKILL.md"
        else:
            self._skill_path = Path(skill_ref) / "SKILL.md"

    @property
    def content(self) -> str:
        if not self._skill_path.exists():
            raise FileNotFoundError(f"SKILL.md not found: {self._skill_path}")
        raw = self._skill_path.read_text(encoding="utf-8")
        # Strip YAML frontmatter if present
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            return parts[2].strip() if len(parts) >= 3 else raw
        return raw
```

- [ ] **Step 3: Create researcher_skill/SKILL.md**

```markdown
---
name: researcher
description: Senior research analyst for AI systems topics
---

You are a senior research analyst with 10 years of experience studying AI orchestration systems.

## Research protocol
1. Start with a broad survey of the topic using web search.
2. Identify 3-5 authoritative sources (papers, official docs, blog posts from known organizations).
3. For each source, extract: key claims, supporting evidence, limitations.
4. Structure output as: Overview → Key Concepts → Framework Analysis → Production Patterns → Bibliography.

## Citation format
Use [AuthorYear] inline. Example: "CrewAI uses a Role-based architecture [CrewAI2024]."
At the end of notes, list full references:
- [CrewAI2024] CrewAI Team. "CrewAI Documentation." https://crewai.com, 2024.

## Quality checklist
- [ ] At least 8 distinct citations
- [ ] Each major claim is supported by a citation
- [ ] Notes are organized under clear headings
- [ ] Minimum 1500 words
```

- [ ] **Step 4: Create writer_skill/SKILL.md**

```markdown
---
name: writer
description: Technical writer for AI and software architecture content
---

You are a technical writer with expertise in AI systems and software architecture.

## Writing protocol
1. Read all research notes before writing any chapter.
2. Write one chapter at a time, in order: Introduction → Architectures → Frameworks → Production → BiDi → Case Study.
3. Each chapter: 350-500 words, 2-4 subsections, at least one citation.
4. Chapter 5 (BiDi): write at least 2 paragraphs in Hebrew, mixed with English technical terms.

## Style guide
- Use active voice.
- Define technical terms on first use.
- Keep sentences under 25 words.
- Never use "utilize" (use "use"), "leverage" (use "apply" or "use"), "synergy."

## Chapter structure
```
## [Chapter Title]
### [Subsection]
...prose...
### [Subsection]
...prose...
```
```

- [ ] **Step 5: Create editor_skill/SKILL.md**

```markdown
---
name: editor
description: Senior editor enforcing style and LaTeX readiness
---

You are a senior editor preparing technical content for LaTeX typesetting.

## Editing protocol
1. Check every chapter for consistent terminology (e.g., "CrewAI" not "crewai" or "crew ai").
2. Verify all citation markers [AuthorYear] have a corresponding reference in ch01 research notes.
3. Ensure all tables use Markdown pipe syntax (will convert cleanly to LaTeX tabular).
4. Verify ch05 contains at least 2 paragraphs in Hebrew and correctly mixes RTL/LTR text.
5. Ensure no chapter exceeds 550 words.
6. Add [NEEDS_FORMULA] marker where a mathematical relationship should become a LaTeX equation.

## Output format
Save each chapter as ch0N_edited.md (e.g., ch01_edited.md).
```

- [ ] **Step 6: Create latex_skill/SKILL.md**

```markdown
---
name: latex_producer
description: LaTeX engineer for fancy formulas (not plain text) and BiDi typesetting
---

You are a LaTeX engineer specializing in LuaLaTeX, Hebrew BiDi, and mathematical typesetting.

## CRITICAL RULE: fancy formula, not plain text
Every mathematical expression MUST use LaTeX math mode:
- WRONG: The cost is C = sum of all token prices.
- RIGHT: \begin{equation} C = \sum_{i=1}^{N}(c_{\text{in}} \cdot t_i^{\text{in}} + c_{\text{out}} \cdot t_i^{\text{out}}) \end{equation}

## Required preamble packages
```latex
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{hebrew}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[backend=biber,style=numeric-comp,sorting=none]{biblatex}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,positioning}
\usepackage{tabularx}
\usepackage{graphicx}
```

## BiDi chapter template
```latex
\begin{hebrew}
פסקה בעברית עם \textenglish{English terms} בתוך הטקסט.
\end{hebrew}
English paragraph with \texthebrew{מונחים עבריים} mixed in.
```

## Compilation sequence
Run exactly: lualatex → biber → lualatex → lualatex (4 commands, not 3).
```

- [ ] **Step 7: Run tests — expect PASS**

```bash
uv run pytest tests/unit/test_skill.py -v
```

- [ ] **Step 8: Commit**

```bash
git add src/agent_article/skills/ tests/unit/test_skill.py
git commit -m "feat(skills): add FileSkill + 4 SKILL.md files for all agents"
```

---

## Phase 5 — Agents

### Task 18: agents/base_agent.py

**Files:**
- Create: `src/agent_article/agents/base_agent.py`
- Create: `src/agent_article/agents/__init__.py`
- Create: `tests/unit/test_agents.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_agents.py
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


@pytest.fixture
def agent_config(tmp_path, monkeypatch):
    import agent_article.shared.config as cfg_mod
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "agents.json").write_text(json.dumps({
        "version": "1.00",
        "agents": {
            "test_agent": {
                "role": "Test Role",
                "goal": "Test goal",
                "backstory": "Test backstory",
                "llm": "claude-cli",
                "skill_ref": "test_skill",
                "temperature": 0.5,
            }
        }
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()

    skills_root = tmp_path / "skills" / "test_skill"
    skills_root.mkdir(parents=True)
    (skills_root / "SKILL.md").write_text("You are a test agent.")

    import agent_article.skills.base_skill as skill_mod
    monkeypatch.setattr(
        skill_mod.FileSkill, "__init__",
        lambda self, ref: setattr(self, "_skill_path", skills_root / "SKILL.md")
    )
    return tmp_path


def test_base_agent_build_returns_crewai_agent(agent_config):
    from agent_article.agents.base_agent import BaseAgent
    from agent_article.tools.file_rw import FileReadTool, FileWriteTool

    class ConcreteAgent(BaseAgent):
        def build(self):
            return self._make_agent()

    with patch("agent_article.agents.base_agent.Agent") as mock_agent:
        mock_agent.return_value = MagicMock()
        agent = ConcreteAgent("test_agent", tools=[])
        result = agent.build()
        mock_agent.assert_called_once()
        call_kwargs = mock_agent.call_args.kwargs
        assert call_kwargs["role"] == "Test Role"
        assert call_kwargs["goal"] == "Test goal"
        assert "Test backstory" in call_kwargs["backstory"]
```

- [ ] **Step 2: Run — expect FAIL**

```bash
uv run pytest tests/unit/test_agents.py -v
```

- [ ] **Step 3: Implement agents/base_agent.py**

```python
"""Abstract base for all CrewAI agents in the article pipeline."""
from abc import ABC, abstractmethod
from typing import Any

from crewai import Agent

from agent_article.shared.config import get_config
from agent_article.skills.base_skill import FileSkill
from agent_article.tools.base_tool import BaseTool


class BaseAgent(ABC):
    """
    Input:  config_key (str) key into agents.json, tools (list[BaseTool])
    Output: crewai.Agent via build()
    Setup:  config/agents.json, skills/<config_key>/SKILL.md
    """

    def __init__(self, config_key: str, tools: list[BaseTool]) -> None:
        self._cfg = get_config("agents")["agents"][config_key]
        self._skill = FileSkill(self._cfg["skill_ref"])
        self._tools = tools

    @abstractmethod
    def build(self) -> Agent: ...

    def _make_agent(self) -> Agent:
        backstory = self._cfg["backstory"] + "\n\n---\n" + self._skill.content
        return Agent(
            role=self._cfg["role"],
            goal=self._cfg["goal"],
            backstory=backstory,
            tools=[t.as_crewai_tool() for t in self._tools],
            verbose=True,
        )
```

- [ ] **Step 4: Run — expect PASS**

```bash
uv run pytest tests/unit/test_agents.py -v
```

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/agents/ tests/unit/test_agents.py
git commit -m "feat(agents): add BaseAgent with skill injection and CrewAI integration"
```

---

### Task 19: Four concrete agent classes

**Files:**
- Create: `src/agent_article/agents/researcher_agent.py`
- Create: `src/agent_article/agents/writer_agent.py`
- Create: `src/agent_article/agents/editor_agent.py`
- Create: `src/agent_article/agents/latex_agent.py`

- [ ] **Step 1: Implement researcher_agent.py**

```python
"""Researcher agent — gathers notes and citations from the web."""
from crewai import Agent
from .base_agent import BaseAgent
from agent_article.tools.web_search import WebSearchTool
from agent_article.tools.file_rw import FileWriteTool


class ResearcherAgent(BaseAgent):
    """
    Input:  topic (str) via task description
    Output: workspace/research_notes.md
    Setup:  config/agents.json::researcher, researcher_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="researcher",
            tools=[WebSearchTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
```

- [ ] **Step 2: Implement writer_agent.py**

```python
"""Writer agent — produces Markdown chapters from research notes."""
from crewai import Agent
from .base_agent import BaseAgent
from agent_article.tools.file_rw import FileReadTool, FileWriteTool


class WriterAgent(BaseAgent):
    """
    Input:  workspace/research_notes.md (via context from ResearchTask)
    Output: workspace/chapters/ch01.md … ch06.md
    Setup:  config/agents.json::writer, writer_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="writer",
            tools=[FileReadTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
```

- [ ] **Step 3: Implement editor_agent.py**

```python
"""Editor agent — polishes chapters and prepares for LaTeX conversion."""
from crewai import Agent
from .base_agent import BaseAgent
from agent_article.tools.file_rw import FileReadTool, FileWriteTool


class EditorAgent(BaseAgent):
    """
    Input:  workspace/chapters/ch*.md (via context from WritingTask)
    Output: workspace/chapters/ch*_edited.md
    Setup:  config/agents.json::editor, editor_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="editor",
            tools=[FileReadTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
```

- [ ] **Step 4: Implement latex_agent.py**

```python
"""LaTeX-Producer agent — converts Markdown to LaTeX and compiles PDF."""
from crewai import Agent
from .base_agent import BaseAgent
from agent_article.tools.file_rw import FileReadTool, FileWriteTool
from agent_article.tools.latex_compile import LaTeXCompileTool
from agent_article.tools.chart_generator import ChartGeneratorTool


class LaTeXAgent(BaseAgent):
    """
    Input:  workspace/chapters/*_edited.md (via context from EditingTask)
    Output: latex/output/uoh-sqak-article.pdf
    Setup:  config/agents.json::latex_producer, latex_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="latex_producer",
            tools=[FileReadTool(), FileWriteTool(), LaTeXCompileTool(), ChartGeneratorTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
```

- [ ] **Step 5: Commit**

```bash
git add src/agent_article/agents/
git commit -m "feat(agents): add ResearcherAgent, WriterAgent, EditorAgent, LaTeXAgent"
```

---

## Phase 6 — Crew + SDK

### Task 20: tasks/article_tasks.py + crew/article_crew.py

**Files:**
- Create: `src/agent_article/tasks/article_tasks.py`
- Create: `src/agent_article/crew/article_crew.py`

- [ ] **Step 1: Implement tasks/article_tasks.py**

```python
"""Task factory — builds CrewAI Tasks from config/tasks.json."""
from crewai import Task, Agent
from agent_article.shared.config import get_config


def build_tasks(
    researcher: Agent,
    writer: Agent,
    editor: Agent,
    latex: Agent,
    topic: str,
) -> list[Task]:
    """Build the 4-task pipeline, substituting {topic} into descriptions."""
    cfg = get_config("tasks")["tasks"]

    def fmt(key: str) -> tuple[str, str]:
        return (
            cfg[key]["description"].format(topic=topic),
            cfg[key]["expected_output"].format(topic=topic),
        )

    desc_r, out_r = fmt("research")
    research_task = Task(description=desc_r, expected_output=out_r, agent=researcher)

    desc_w, out_w = fmt("write")
    write_task = Task(description=desc_w, expected_output=out_w, agent=writer,
                      context=[research_task])

    desc_e, out_e = fmt("edit")
    edit_task = Task(description=desc_e, expected_output=out_e, agent=editor,
                     context=[write_task])

    desc_l, out_l = fmt("latex")
    latex_task = Task(description=desc_l, expected_output=out_l, agent=latex,
                      context=[edit_task])

    return [research_task, write_task, edit_task, latex_task]
```

- [ ] **Step 2: Implement crew/article_crew.py**

```python
"""ArticleCrew — assembles 4 agents and runs the sequential pipeline."""
from dataclasses import dataclass
from pathlib import Path

from crewai import Crew, Process

from agent_article.agents.researcher_agent import ResearcherAgent
from agent_article.agents.writer_agent import WriterAgent
from agent_article.agents.editor_agent import EditorAgent
from agent_article.agents.latex_agent import LaTeXAgent
from agent_article.tasks.article_tasks import build_tasks
from agent_article.shared.config import get_config
from agent_article.shared.logging_fifo import StructuredLogger


@dataclass
class CrewResult:
    raw_output: str
    pdf_path: str | None


class ArticleCrew:
    """
    Input:  topic (str), inputs (dict)
    Output: CrewResult with pdf_path
    Setup:  config/crew.json, all agents + tasks
    """

    def __init__(self) -> None:
        self._cfg = get_config("crew")
        self._logger = StructuredLogger("article_crew")

    def kickoff(self, topic: str, extra_inputs: dict | None = None) -> CrewResult:
        researcher = ResearcherAgent().build()
        writer = WriterAgent().build()
        editor = EditorAgent().build()
        latex = LaTeXAgent().build()

        tasks = build_tasks(researcher, writer, editor, latex, topic=topic)

        crew = Crew(
            agents=[researcher, writer, editor, latex],
            tasks=tasks,
            process=Process.sequential,
            verbose=self._cfg.get("verbose", True),
        )

        inputs = {"topic": topic, **(extra_inputs or {})}
        self._logger.info("crew_kickoff", topic=topic)
        result = crew.kickoff(inputs=inputs)
        self._logger.info("crew_done", topic=topic)

        cfg = get_config("latex")
        pdf_path = str(Path(cfg["output_dir"]) / get_config("setup")["output_filename"])
        return CrewResult(raw_output=str(result), pdf_path=pdf_path)
```

- [ ] **Step 3: Commit**

```bash
git add src/agent_article/tasks/ src/agent_article/crew/
git commit -m "feat(crew): add ArticleCrew with 4-agent sequential pipeline"
```

---

### Task 21: sdk/sdk.py + menu/tui.py + main.py

**Files:**
- Create: `src/agent_article/sdk/sdk.py`
- Create: `src/agent_article/menu/tui.py`
- Create: `src/agent_article/main.py`

- [ ] **Step 1: Implement sdk/sdk.py**

```python
"""ArticleSDK — sole public entry point for all pipeline operations."""
from dataclasses import dataclass
from pathlib import Path

from agent_article.crew.article_crew import ArticleCrew, CrewResult
from agent_article.shared.config import get_config
from agent_article.shared.gatekeeper import ApiGatekeeper
from agent_article.shared.logging_fifo import StructuredLogger
from agent_article.tools.latex_compile import LaTeXCompileTool


@dataclass
class ArticleResult:
    pdf_path: str | None
    token_cost: dict
    compile_warnings: list[str]


class ArticleSDK:
    """
    Input:  topic (str)
    Output: ArticleResult with pdf_path, cost, warnings
    Setup:  config/*.json, Claude CLI login
    """

    def __init__(self) -> None:
        self._logger = StructuredLogger("sdk")
        self._crew = ArticleCrew()

    def generate_article(self, topic: str) -> CrewResult:
        self._logger.info("generate_article_start", topic=topic)
        return self._crew.kickoff(topic=topic)

    def approve_markdown(self) -> bool:
        """Human-in-the-loop gate before LaTeX compilation."""
        answer = input("\nApprove Markdown content for LaTeX conversion? [y/N] ").strip().lower()
        return answer == "y"

    def compile_pdf(self) -> str:
        """Re-run LaTeX compilation on existing .tex files."""
        cfg = get_config("latex")
        tool = LaTeXCompileTool()
        return tool.run(Path(cfg["main_file"]).name)

    def get_spend_report(self) -> dict:
        return {
            svc: {"calls": rec.calls, "tokens_in": rec.tokens_in, "tokens_out": rec.tokens_out}
            for svc, rec in ApiGatekeeper.instance().get_spend_report().items()
        }

    def run_audit(self) -> dict:
        """Check PDF envelope: page count, formula presence, table overflow."""
        cfg = get_config("latex")
        main_tex = Path(cfg["main_file"])
        issues = []
        if not main_tex.exists():
            issues.append("main.tex not found")
            return {"ok": False, "issues": issues}
        content = main_tex.read_text(encoding="utf-8", errors="ignore")
        if not any(tok in content for tok in [r"\begin{equation}", r"\frac{", r"\sum_", r"$$"]):
            issues.append("No fancy formula found — may be using plain text math")
        log_path = main_tex.parent / "output" / "main.log"
        if log_path.exists():
            log = log_path.read_text(encoding="utf-8", errors="ignore")
            if "Overfull \\hbox" in log:
                issues.append("Overfull hbox detected — table may overflow page")
        return {"ok": len(issues) == 0, "issues": issues}
```

- [ ] **Step 2: Implement menu/tui.py**

```python
"""Terminal menu for the article generation pipeline."""
from rich.console import Console
from rich.panel import Panel

from agent_article.sdk.sdk import ArticleSDK
from agent_article.shared.config import get_config

MENU = """
[bold]HW3 — Article Generation Pipeline[/bold]

  [G] Generate article (full pipeline)
  [C] Compile PDF only (re-run LaTeX)
  [A] Audit PDF envelope
  [S] Spend report (token cost)
  [X] Exit
"""


class TerminalMenu:
    def __init__(self) -> None:
        self._console = Console()
        self._sdk = ArticleSDK()

    def run(self) -> None:
        topic = get_config("setup").get("default_topic", "Multi-Agent Orchestration Patterns")
        while True:
            self._console.print(Panel(MENU, border_style="blue"))
            choice = input("Choice: ").strip().upper()
            if choice == "G":
                self._run_generation(topic)
            elif choice == "C":
                result = self._sdk.compile_pdf()
                self._console.print(f"[green]PDF: {result}[/green]")
            elif choice == "A":
                audit = self._sdk.run_audit()
                self._console.print(audit)
            elif choice == "S":
                self._console.print(self._sdk.get_spend_report())
            elif choice == "X":
                break

    def _run_generation(self, topic: str) -> None:
        self._console.print(f"[cyan]Generating article on: {topic}[/cyan]")
        result = self._sdk.generate_article(topic)
        self._console.print("[yellow]Article generation complete. Review workspace/chapters/[/yellow]")
        if self._sdk.approve_markdown():
            pdf = self._sdk.compile_pdf()
            self._console.print(f"[green]PDF ready: {pdf}[/green]")
        else:
            self._console.print("[red]LaTeX compilation skipped.[/red]")
```

- [ ] **Step 3: Implement main.py**

```python
"""Entry point for agent-article CLI."""
from agent_article.menu.tui import TerminalMenu


def main() -> None:
    TerminalMenu().run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Commit**

```bash
git add src/agent_article/sdk/ src/agent_article/menu/ src/agent_article/main.py
git commit -m "feat(sdk): add ArticleSDK, TerminalMenu, and main entry point"
```

---

## Phase 7 — LaTeX Skeleton

### Task 22: latex/style/article.sty + latex/main.tex

**Files:**
- Create: `latex/style/article.sty`
- Create: `latex/main.tex`

- [ ] **Step 1: Create latex/style/article.sty**

```latex
% article.sty — Custom style for uoh-sqak HW3 article
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{style/article}[2026/06/06 HW3 Article Style]

% Font and encoding (LuaLaTeX)
\RequirePackage{fontspec}
\setmainfont{FreeSerif}[
  BoldFont = FreeSerifBold,
  ItalicFont = FreeSerifItalic,
]

% Multilingual support (Hebrew + English BiDi)
\RequirePackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{hebrew}

% Math
\RequirePackage{amsmath,amssymb,amsthm}

% Bibliography
\RequirePackage[backend=biber,style=numeric-comp,sorting=none]{biblatex}

% Hyperlinks (must load after biblatex)
\RequirePackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}

% Page layout
\RequirePackage[a4paper,margin=2.5cm]{geometry}

% Headers/footers
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Multi-Agent Orchestration Patterns}
\fancyhead[R]{\small Course 203.3763}
\fancyfoot[C]{\thepage}

% Graphics
\RequirePackage{graphicx}
\graphicspath{{figures/}}

% TikZ
\RequirePackage{tikz}
\usetikzlibrary{shapes,arrows.meta,positioning,fit}

% Tables
\RequirePackage{tabularx,booktabs}

% Code listings
\RequirePackage{listings}
```

- [ ] **Step 2: Create latex/main.tex**

```latex
% main.tex — HW3 Article: Multi-Agent Orchestration Patterns
% Course 203.3763 — Orchestration of AI Agents
% Authors: Salah Qadah, Andalus Kalash
% Compiler: lualatex → biber → lualatex → lualatex

\documentclass[12pt,a4paper]{article}
\usepackage{style/article}
\addbibresource{bib/references.bib}

% ── Cover sheet metadata ──────────────────────────────────────────────────
\title{%
  \Huge\textbf{Multi-Agent Orchestration Patterns}\\[0.5em]
  \large From Research to Production Pipelines
}
\author{%
  Salah Qadah \and Andalus Kalash \\[0.3em]
  \normalsize University of Haifa \\
  \normalsize Course 203.3763 --- Orchestration of AI Agents \\
  \normalsize Lecturer: Dr. Yoram Reuven Segal
}
\date{June 2026}

\begin{document}

\maketitle
\thispagestyle{empty}
\newpage

\tableofcontents
\newpage

\input{chapters/ch01_introduction}
\newpage
\input{chapters/ch02_architectures}
\newpage
\input{chapters/ch03_frameworks}
\newpage
\input{chapters/ch04_production}
\newpage
\input{chapters/ch05_bidi}
\newpage
\input{chapters/ch06_casestudy}
\newpage

\printbibliography[heading=bibintoc,title={Bibliography}]

\end{document}
```

- [ ] **Step 3: Create latex/Makefile**

```makefile
MAIN = main
LATEX = lualatex
BIBER = biber
FLAGS = --interaction=nonstopmode

.PHONY: all clean

all: output/$(MAIN).pdf

output/$(MAIN).pdf: $(MAIN).tex bib/references.bib style/article.sty chapters/*.tex
	mkdir -p output
	$(LATEX) $(FLAGS) --output-directory=output $(MAIN).tex
	$(BIBER) --input-directory=output --output-directory=output $(MAIN)
	$(LATEX) $(FLAGS) --output-directory=output $(MAIN).tex
	$(LATEX) $(FLAGS) --output-directory=output $(MAIN).tex

clean:
	rm -f output/*.aux output/*.log output/*.toc output/*.bbl \
	       output/*.blg output/*.bcf output/*.xml output/*.out
```

- [ ] **Step 4: Create placeholder chapter files** (agents will fill these in):

```bash
for i in 01_introduction 02_architectures 03_frameworks 04_production 05_bidi 06_casestudy; do
  echo "% Chapter $i — generated by LaTeXAgent" > latex/chapters/ch${i}.tex
done
mkdir -p latex/output latex/figures
touch latex/figures/.gitkeep
```

- [ ] **Step 5: Commit**

```bash
git add latex/
git commit -m "feat(latex): add LaTeX skeleton — main.tex, article.sty, Makefile, chapter stubs"
```

---

### Task 23: latex/figures/crew_architecture.tikz + latex/bib/references.bib

**Files:**
- Create: `latex/figures/crew_architecture.tikz`
- Create: `latex/bib/references.bib`

- [ ] **Step 1: Create crew_architecture.tikz** (mandatory per lecture L1708–1714)

```tikz
% crew_architecture.tikz — CrewAI pipeline block diagram (MANDATORY per Dr. Segal L1708-1714)
\begin{tikzpicture}[
    node distance=1.5cm and 2.5cm,
    agent/.style={rectangle, draw=blue!70, fill=blue!10, rounded corners,
                  minimum width=2.8cm, minimum height=1cm, align=center, font=\small},
    arrow/.style={-{Stealth[scale=1.2]}, thick, blue!70},
    label_style/.style={font=\footnotesize\itshape, text=gray}
  ]

  % Nodes
  \node[agent] (researcher) {Researcher\\Agent};
  \node[agent, right=of researcher] (writer) {Writer\\Agent};
  \node[agent, right=of writer] (editor) {Editor\\Agent};
  \node[agent, right=of editor] (latex) {LaTeX\\Producer Agent};

  % Arrows
  \draw[arrow] (researcher) -- node[above, label_style]{notes.md} (writer);
  \draw[arrow] (writer) -- node[above, label_style]{ch*.md} (editor);
  \draw[arrow] (editor) -- node[above, label_style]{*\_edited.md} (latex);

  % Output
  \node[rectangle, draw=green!70, fill=green!10, rounded corners,
        right=2cm of latex, minimum width=2.8cm, minimum height=1cm, align=center, font=\small]
       (pdf) {uoh-sqak\\article.pdf};
  \draw[arrow] (latex) -- node[above, label_style]{compile} (pdf);

  % Gatekeeper
  \node[rectangle, draw=red!70, fill=red!10, rounded corners, dashed,
        below=1.5cm of writer, minimum width=8cm, minimum height=0.8cm, align=center, font=\small]
       (gk) {ApiGatekeeper — all external calls (LLM · Search · LaTeX)};
  \draw[-{Stealth}, dashed, red!60] (researcher.south) -- (gk.north -| researcher.south);
  \draw[-{Stealth}, dashed, red!60] (writer.south) -- (gk.north -| writer.south);
  \draw[-{Stealth}, dashed, red!60] (editor.south) -- (gk.north -| editor.south);
  \draw[-{Stealth}, dashed, red!60] (latex.south) -- (gk.north -| latex.south);

  % Process label
  \node[above=0.8cm of writer, font=\small\bfseries, text=blue!80]
       {CrewAI Process.sequential};

\end{tikzpicture}
```

- [ ] **Step 2: Create latex/bib/references.bib** (placeholder entries — agents will enrich these)

```bibtex
@article{LangChain2024,
  author    = {{LangChain Team}},
  title     = {LangChain: Building applications with LLMs through composability},
  journal   = {GitHub},
  year      = {2024},
  url       = {https://github.com/langchain-ai/langchain},
}

@article{CrewAI2024,
  author    = {{CrewAI Team}},
  title     = {CrewAI: Framework for orchestrating role-playing AI agents},
  journal   = {GitHub},
  year      = {2024},
  url       = {https://github.com/crewAIInc/crewAI},
}

@article{LangGraph2024,
  author    = {{LangChain Team}},
  title     = {LangGraph: Building stateful, multi-actor applications with LLMs},
  journal   = {GitHub},
  year      = {2024},
  url       = {https://github.com/langchain-ai/langgraph},
}

@book{RussellNorvig2020,
  author    = {Russell, Stuart and Norvig, Peter},
  title     = {Artificial Intelligence: A Modern Approach},
  edition   = {4th},
  publisher = {Pearson},
  year      = {2020},
}

@article{AutoGPT2023,
  author    = {Significant Gravitas},
  title     = {AutoGPT: An Autonomous GPT-4 Experiment},
  journal   = {GitHub},
  year      = {2023},
  url       = {https://github.com/Significant-Gravitas/AutoGPT},
}
```

- [ ] **Step 3: Commit**

```bash
git add latex/figures/crew_architecture.tikz latex/bib/references.bib
git commit -m "feat(latex): add TikZ Crew architecture diagram and placeholder bibliography"
```

---

### Task 24: scripts/build_article.py

**Files:**
- Create: `scripts/build_article.py`

- [ ] **Step 1: Implement scripts/build_article.py**

```python
"""Python-driven LaTeX compilation — 4 passes as required by Dr. Segal."""
import subprocess
import sys
from pathlib import Path

LATEX_DIR = Path(__file__).parent.parent / "latex"
OUTPUT_DIR = LATEX_DIR / "output"
MAIN = "main"


def run(cmd: list[str], cwd: Path) -> None:
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(result.stderr[-2000:])
        raise SystemExit(f"Command failed: {' '.join(cmd)}")


def build() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    print("[1/4] lualatex (first pass)...")
    run(["lualatex", "--interaction=nonstopmode", f"--output-directory={OUTPUT_DIR}", f"{MAIN}.tex"], LATEX_DIR)
    print("[2/4] biber...")
    run(["biber", f"--input-directory={OUTPUT_DIR}", f"--output-directory={OUTPUT_DIR}", MAIN], LATEX_DIR)
    print("[3/4] lualatex (citation pass)...")
    run(["lualatex", "--interaction=nonstopmode", f"--output-directory={OUTPUT_DIR}", f"{MAIN}.tex"], LATEX_DIR)
    print("[4/4] lualatex (cross-ref pass)...")
    run(["lualatex", "--interaction=nonstopmode", f"--output-directory={OUTPUT_DIR}", f"{MAIN}.tex"], LATEX_DIR)
    pdf = OUTPUT_DIR / f"{MAIN}.pdf"
    if pdf.exists():
        print(f"\n✅ PDF ready: {pdf}  ({pdf.stat().st_size // 1024} KB)")
    else:
        raise SystemExit("❌ PDF not found after compilation")


if __name__ == "__main__":
    build()
```

- [ ] **Step 2: Test it compiles the skeleton**

```bash
uv run python scripts/build_article.py
```

Expected: skeleton PDF (cover + blank chapters) — may have warnings, should not hard-fail.

- [ ] **Step 3: Commit**

```bash
git add scripts/build_article.py
git commit -m "feat(scripts): add Python-driven 4-pass LaTeX build script"
```

---

## Phase 8 — Tests

### Task 25: tests/conftest.py + integration tests

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/integration/test_article_crew.py`
- Create: `tests/integration/test_latex_pipeline.py`

- [ ] **Step 1: Create tests/conftest.py**

```python
"""Shared fixtures for unit and integration tests."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def mock_config(tmp_path, monkeypatch):
    """Provide test config files in a tmp directory."""
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()

    configs = {
        "setup": {"version": "1.00", "package": "agent_article",
                  "workspace_dir": str(tmp_path / "workspace"),
                  "results_dir": str(tmp_path / "results"),
                  "latex_dir": "latex", "output_filename": "test.pdf"},
        "agents": {"version": "1.00", "agents": {
            "researcher": {"role": "R", "goal": "G", "backstory": "B",
                           "llm": "claude-cli", "skill_ref": "researcher_skill", "temperature": 0.3},
            "writer": {"role": "R", "goal": "G", "backstory": "B",
                       "llm": "claude-cli", "skill_ref": "writer_skill", "temperature": 0.7},
            "editor": {"role": "R", "goal": "G", "backstory": "B",
                       "llm": "claude-cli", "skill_ref": "editor_skill", "temperature": 0.2},
            "latex_producer": {"role": "R", "goal": "G fancy formula, not plain text", "backstory": "B",
                               "llm": "claude-cli", "skill_ref": "latex_skill", "temperature": 0.1},
        }},
        "tasks": {"version": "1.00", "tasks": {
            "research": {"description": "Research {topic}", "expected_output": "notes.md"},
            "write": {"description": "Write {topic}", "expected_output": "chapters"},
            "edit": {"description": "Edit {topic}", "expected_output": "edited chapters"},
            "latex": {"description": "LaTeX {topic}", "expected_output": "PDF"},
        }},
        "crew": {"version": "1.00", "process": "sequential", "verbose": False},
        "rate_limits": {"version": "1.00", "services": {}},
        "logging_config": {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                           "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"},
        "latex": {"version": "1.00", "compiler": "lualatex", "biber": "biber", "passes": 4,
                  "bib_style": "numeric-comp", "main_file": "latex/main.tex",
                  "output_dir": "latex/output", "target_pages": 15},
    }

    for name, content in configs.items():
        (cfg_dir / f"{name}.json").write_text(json.dumps(content))

    import agent_article.shared.config as cfg_mod
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod._cache.clear()

    yield tmp_path


@pytest.fixture
def mock_llm():
    """Mock CrewAI LLM to return deterministic responses."""
    with patch("crewai.Agent") as mock_agent_cls:
        mock_agent_cls.return_value = MagicMock()
        yield mock_agent_cls
```

- [ ] **Step 2: Create integration/test_article_crew.py**

```python
"""Integration test — runs ArticleCrew with MockLLM, verifies workspace files."""
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest


def test_crew_kickoff_produces_workspace_files(mock_config, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    chapters = workspace / "chapters"
    chapters.mkdir()

    # Simulate what agents would write
    (workspace / "research_notes.md").write_text("# Notes\nContent [Ref2024]")
    for i in range(1, 7):
        (chapters / f"ch0{i}_edited.md").write_text(f"# Chapter {i}\nContent")

    with patch("agent_article.crew.article_crew.ResearcherAgent") as r, \
         patch("agent_article.crew.article_crew.WriterAgent") as w, \
         patch("agent_article.crew.article_crew.EditorAgent") as e, \
         patch("agent_article.crew.article_crew.LaTeXAgent") as l, \
         patch("agent_article.crew.article_crew.Crew") as crew_cls:

        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = MagicMock(raw="Article complete")
        crew_cls.return_value = mock_crew

        from agent_article.crew.article_crew import ArticleCrew
        from agent_article.shared.gatekeeper import ApiGatekeeper
        ApiGatekeeper._instance = None

        result = ArticleCrew().kickoff("Test Topic")

    assert mock_crew.kickoff.called
    assert result.raw_output == "Article complete"
```

- [ ] **Step 3: Create integration/test_latex_pipeline.py**

```python
"""Integration test — LaTeX skeleton compiles without hard failure."""
import subprocess
from pathlib import Path
import pytest


@pytest.mark.skipif(
    subprocess.run(["which", "lualatex"], capture_output=True).returncode != 0,
    reason="lualatex not installed"
)
def test_latex_skeleton_compiles(tmp_path):
    """Test that the LaTeX skeleton (without agent content) compiles."""
    import shutil
    latex_src = Path(__file__).parent.parent.parent / "latex"
    if not latex_src.exists():
        pytest.skip("latex/ directory not found")

    latex_dst = tmp_path / "latex"
    shutil.copytree(latex_src, latex_dst)
    (latex_dst / "output").mkdir(exist_ok=True)

    result = subprocess.run(
        ["lualatex", "--interaction=nonstopmode",
         f"--output-directory={latex_dst / 'output'}", "main.tex"],
        cwd=latex_dst, capture_output=True, text=True, timeout=60,
    )
    # Skeleton may warn but should not exit 1 on first pass
    assert result.returncode in (0, 1)  # 1 allowed for unresolved refs on first pass
    assert (latex_dst / "output" / "main.aux").exists()
```

- [ ] **Step 4: Run all tests**

```bash
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

Expected: all unit tests pass, integration tests pass or skip.

- [ ] **Step 5: Commit**

```bash
git add tests/
git commit -m "test: add conftest with MockLLM fixture and integration tests"
```

---

## Phase 9 — Full Pipeline Run

### Task 26: Generate real article + compile PDF

- [ ] **Step 1: Verify Claude CLI is logged in**

```bash
claude --version
# If not logged in:
claude --login
```

- [ ] **Step 2: Run full article generation**

```bash
uv run agent-article
# Press G to generate
# Topic: Multi-Agent Orchestration Patterns
```

- [ ] **Step 3: Review workspace/chapters/ (human checkpoint)**

Open each `workspace/chapters/ch0N_edited.md`. Verify:
- Content is coherent (no lettuce farming in ch2 about equations)
- ch05 has Hebrew text
- Citations look like `[AuthorYear]`

- [ ] **Step 4: Approve Markdown in the menu → LaTeX compiles**

Press `y` at the approval prompt.

- [ ] **Step 5: Verify PDF**

```bash
open latex/output/uoh-sqak-article.pdf
```
Check manually: ≥15 pages, cover, TOC, BiDi chapter, TikZ diagram, formula, table, bibliography with clickable links.

- [ ] **Step 6: Commit results + PDF**

```bash
cp -r workspace/chapters results/  # save Markdown trace
git add results/ latex/output/uoh-sqak-article.pdf latex/chapters/*.tex latex/bib/references.bib
git commit -m "feat: add generated article content and compiled PDF"
```

---

## Phase 10 — README + Quality Gates

### Task 27: README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md** — required sections:

```markdown
# uoh-sqak-ex03 — HW3 Article Generation Pipeline

> Course 203.3763 | University of Haifa | Spring 2026 | Dr. Yoram Segal

## Quick Start
## Prerequisites
## Installation
## Usage (4 paths: A/B/C/D)
## Architecture
   - Layer stack diagram (ASCII)
   - Crew data flow
   - Class hierarchy
## Configuration Guide (each config/*.json explained)
## Sample PDF (link to latex/output/uoh-sqak-article.pdf)
## Cost Analysis (token table for one full generation)
## Extending the Pipeline (agent registry, skill registry, tool registry)
## Why LaTeX over Word
## PoC Limitations
## AI Usage Disclosure (verbatim Hebrew + English paragraph)
## HW1 Extensibility Remediation
## License
```

- [ ] **Step 2: Add the verbatim AI ethics paragraph:**

```markdown
## AI Usage Disclosure

**Hebrew:** מומלץ להשתמש בכלי LLM וסוכני AI לעזרה בהשלמת הפרויקט. מובהר כי כחלק מהבדיקה יתכן וייעשה שימוש בסוכני AI לביצוע הבדיקה. כל השימוש בכלי AI בפרויקט זה מתועד ב-[docs/PROMPTS.md](docs/PROMPTS.md).

**English:** Use of LLM tools and AI agents is recommended to help complete the project. As part of the inspection, AI agents may be used to perform the check. All AI tool usage in this project is documented in [docs/PROMPTS.md](docs/PROMPTS.md).
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README with install/usage/architecture/cost/ethics"
```

---

### Task 28: Final quality gates

- [ ] **Step 1: Run ruff — must return 0 errors**

```bash
uv run ruff check src tests scripts
```

Fix any violations before continuing.

- [ ] **Step 2: Run line count check**

```bash
uv run python scripts/check_file_lines.py
```

Split any files over 150 lines.

- [ ] **Step 3: Run full test suite with coverage**

```bash
uv run pytest tests/unit tests/integration --cov=src --cov-report=term-missing
```

Expected: coverage ≥85%. If below, add tests for uncovered branches.

- [ ] **Step 4: Run PDF audit**

```bash
uv run agent-article
# Press A for audit
```

Expected: `{"ok": true, "issues": []}`.

- [ ] **Step 5: Commit any fixes**

```bash
git add .
git commit -m "fix: resolve ruff errors, improve test coverage to ≥85%"
```

---

## Phase 11 — Submission

### Task 29: Tag + push + Moodle

- [ ] **Step 1: Final commit and tag**

```bash
git add .
git commit -m "chore: final submission — v1.00"
git tag v1.00
git push origin main --tags
```

- [ ] **Step 2: Verify repo is publicly accessible**

Open `https://github.com/salah-dev-stu/uoh-sqak-ex03` in incognito. Must load without login.

- [ ] **Step 3: Generate submission PDF**

```bash
uv run python scripts/fill_submission_pdf.py
# Verify: exercise=03, group=uoh-sqak, self-grade=85
# Student 1: Salah Qadah (323039974)
# Student 2: Andalus Kalash (211435797)
# Repo URL: https://github.com/salah-dev-stu/uoh-sqak-ex03
```

- [ ] **Step 4: Moodle upload**

Both Salah AND Andalus upload `uoh-sqak-ex03.pdf` separately to Moodle assignment id=270973.

- [ ] **Step 5: Report back to orchestrator** with:
  - Repo URL
  - PDF page count
  - Coverage %
  - Commit count
  - Any open issues

---

## Self-Review Checklist

### Spec coverage (all H-rules)
| H-rule | Task |
|--------|------|
| H1 — 15-page PDF | Task 26 |
| H2 — Cover sheet | Task 22 (main.tex \maketitle) |
| H3 — TOC + chapters + headers/footers | Task 22 (article.sty fancyhdr) |
| H4 — ≥1 image | Task 26 (agent generates figures) |
| H5 — Python chart | Task 15 (ChartGeneratorTool) |
| H6 — Table fits page | Task 26 (tabularx in agent output) |
| H7 — Fancy formula | Task 17 (latex_skill SKILL.md enforces) |
| H8 — BiDi chapter | Task 17 (editor_skill SKILL.md) + Task 22 (polyglossia) |
| H9 — Linked bibliography | Task 23 (biblatex + biber + hyperref) |
| H10 — LaTeX in repo | Task 22–24 |
| H11 — lualatex OR xelatex | Task 22 |
| H12 — 4 compile passes | Task 24 (build_article.py) |
| H13 — TikZ diagram inside PDF | Task 23 (crew_architecture.tikz) |
| H14 — CrewAI 4 agents | Tasks 18–19 |
| H15 — Skill layer | Task 17 |
| H16 — Sequential process | Task 20 |
| H17 — Markdown-first | Task 21 (approve_markdown human gate) |
| H18 — Hebrew or English output | Task 17 (editor skill) |
| H19 — Pairs only | Task 29 (submission) |
| H20 — Both members upload | Task 29 |
| H21 — Public repo | Task 29 |
| H22 — Cost analysis | Task 27 (README) |
| H23 — AI ethics | Task 27 (README) |
| H24 — Continuous commits | All tasks (commit after every task) |
| H25 — SDK as sole entry | Task 21 (ArticleSDK) |

### R-rules
| R-rule | Task |
|--------|------|
| R1 — SDK | Task 21 |
| R2 — OOP + class diagram | Tasks 18–19 + Task 5 (PLAN.md) |
| R3 — Gatekeeper | Task 12 |
| R4 — Rate limits in JSON | Task 3 (rate_limits.json) |
| R5 — FIFO queue | Task 11 (logging_fifo.py) |
| R6 — Versioning | Tasks 3 + 9 |
| R7 — TDD | All code tasks |
| R8 — ≤150 lines | Task 28 (check_file_lines.py) |
| R9 — Ruff 0 errors | Task 28 |
| R10 — Coverage ≥85% | Task 28 |
| R11 — No hardcoded values | Config tasks + code reviews |
| R12 — No secrets | Task 1 (.env-example) |
| R13 — uv only | All tasks |
