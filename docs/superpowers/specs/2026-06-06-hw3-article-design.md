# HW3 Article Generation System — Design Spec

**Date:** 2026-06-06
**Author:** Salah Qadah + Andalus Kalash (pair `uoh-sqak`)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa, Dr. Yoram Segal
**Deadline:** Friday 12 June 2026 23:59 Asia/Jerusalem (Moodle id=270973)
**Repo:** `https://github.com/salah-dev-stu/uoh-sqak-ex03` (public, created on Plan approval)

---

## 1. Project Summary

Build a **CrewAI multi-agent team** (4 agents, `Process.sequential`) that produces a **≥15-page LaTeX PDF article** on the topic **"Multi-Agent Orchestration Patterns"**. The article is the central graded artifact. Grading is "on the envelope" — links resolve, BiDi renders, formulas are fancy, tables fit, citations are clickable.

**Decisions locked:**

| Decision | Value |
|---|---|
| Article topic | Multi-Agent Orchestration Patterns |
| LLM provider | Claude CLI login (all agents, single provider) |
| Process type | `Process.sequential` |
| Workflow | Markdown-first → LaTeX conversion |
| Compiler | LuaLaTeX (XeLaTeX equally acceptable per lecturer) |
| Bibliography | `biblatex` + `biber` (NOT legacy bibtex) |
| Pair split | Salah implements; Andalus reviews + co-signs |
| Self-grade placeholder | 85 |
| Repo creation | After Plan approval, first commit = full scaffolding |

---

## 2. Architecture

### 2.1 Layer Stack

```
[Terminal Menu]         menu/tui.py                 letter-keyed TUI (A/G/R/X)
       ↓
[SDK]                   sdk/sdk.py                  sole public surface (R1)
       ↓
[ArticleCrew]           crew/article_crew.py        Process.sequential
       ↓
[Agents × 4]            agents/*.py                 each loads Skill from file
       ↓
[Tasks × 4]             tasks/article_tasks.py      descriptions from config/tasks.json
       ↓
[Tools × 5]             tools/*.py                  web_search, file_read, file_write,
                                                    latex_compile, chart_generator
       ↓
[Gatekeeper]            shared/gatekeeper.py        ALL external calls (R3)
       ↓
[Infrastructure]        Claude CLI / DuckDuckGo / lualatex subprocess
```

### 2.2 Data Flow

`workspace/` lives at the project root (`hw3/workspace/`) and is git-ignored (intermediate artifacts). Markdown trace files are committed separately to `results/` after approval.

```
1. User: menu → "G) Generate Article"
2. SDK.generate_article(topic="Multi-Agent Orchestration Patterns")
3. Researcher:       writes  workspace/research_notes.md
4. Writer:           reads notes → writes workspace/chapters/ch01.md … ch06.md
5. Editor:           reads chapters → rewrites workspace/chapters/ch0N_edited.md
                              ↑
             [HUMAN CHECKPOINT] SDK.approve_markdown() → "Approve Markdown? [y/N]"
                     copies approved .md to results/  (committed as trace evidence)
                     (positive AI economy — Human-in-the-Loop per lecture §7.3)
6. LaTeX-Producer:
        reads all ch*_edited.md
        generates latex/chapters/*.tex + latex/main.tex + latex/bib/references.bib
        calls: lualatex → biber → lualatex → lualatex  (4 passes, verifies .log)
7. Output: latex/output/uoh-sqak-article.pdf
8. SDK returns: ArticleResult(pdf_path, page_count, token_cost, compile_warnings)
```

**SDK public surface** (`sdk/sdk.py`):
```python
class ArticleSDK:
    def generate_article(self, topic: str) -> ArticleResult: ...
    def approve_markdown(self) -> bool: ...        # human-in-the-loop gate
    def compile_pdf(self) -> CompileResult: ...    # standalone re-compile
    def get_spend_report(self) -> SpendReport: ... # token cost table
    def run_audit(self) -> AuditResult: ...        # envelope checks (links, tables, formulas)
```

### 2.3 Post-Compile Audit (inside `LaTeXCompileTool`)

- Grep `.log` for `"Rerun to get cross-references right"` → trigger extra pass
- Grep `.log` for `"Overfull \hbox"` on tables → warn + re-prompt LaTeX-Producer
- Verify `$...$` / `\begin{equation}` / `\frac` / `\sum` in .tex — if none, re-prompt for "fancy formula, not plain text"

---

## 3. Agents, Skills, Tasks

### 3.1 Agent Definitions (loaded from `config/agents.json`)

| Agent | Role | Goal | Key Tools |
|---|---|---|---|
| **ResearcherAgent** | Senior research analyst specializing in AI systems | Gather structured notes on the topic with citations | `web_search`, `file_write` |
| **WriterAgent** | Technical writer with expertise in AI and software architecture | Produce coherent Markdown chapters from research notes | `file_read`, `file_write` |
| **EditorAgent** | Senior editor and style guide enforcer | Polish prose, verify citation placeholders, enforce chapter structure | `file_read`, `file_write` |
| **LaTeXAgent** | LaTeX engineer producing **fancy formulas, not plain text** | Convert approved Markdown to LaTeX, compile 4 passes, verify all links resolve | `file_read`, `latex_compile`, `chart_generator` |

LaTeXAgent prompt MUST include the verbatim phrase **"fancy formula, not plain text"** (per spec §13.2 and lecture L1742–1748).

### 3.2 Skill Layer (`src/agent_article/skills/`)

Each agent gets a `SKILL.md` + `references/` directory (per spec Appendix A):

```
skills/
├── researcher_skill/
│   ├── SKILL.md          YAML frontmatter + search strategy + citation format
│   └── references/       source quality checklist, example citations
├── writer_skill/
│   ├── SKILL.md          style guide, chapter structure template, tone
│   └── references/       section-length guide
├── editor_skill/
│   ├── SKILL.md          grammar checklist, BiDi chapter requirements, table-fit rules
│   └── references/
└── latex_skill/
    ├── SKILL.md          LaTeX preamble template, BiDi recipe, fancy-formula rule,
    │                     biblatex/biber usage, TikZ block-diagram template
    └── references/       amsmath cheatsheet, polyglossia setup
```

**Skill vs Tool distinction (Dr. Segal verbatim):**
- **Tool** = the screwdriver / drill: what the agent CAN DO.
- **Skill** = the onboarding packet: HOW the agent does it (checklists, style, procedures).

### 3.3 OOP Class Hierarchy (satisfies R2 + class diagram requirement)

```
BaseAgent(ABC)
├── ResearcherAgent
├── WriterAgent
├── EditorAgent
└── LaTeXAgent

BaseTool(ABC)
├── WebSearchTool
├── FileReadTool
├── FileWriteTool
├── LaTeXCompileTool
└── ChartGeneratorTool

BaseSkill(ABC)
└── FileSkill     reads SKILL.md from disk, returns content for agent backstory injection
```

### 3.4 Task Flow (`context=[prev_task]` chains output)

```
ResearchTask   → output: workspace/research_notes.md
WritingTask    → context=[ResearchTask],  output: workspace/chapters/ch*.md
EditingTask    → context=[WritingTask],   output: workspace/chapters/ch*_edited.md
                         ↑
              [HUMAN CHECKPOINT] SDK.approve_markdown()
LaTeXTask      → context=[EditingTask],   output: latex/output/uoh-sqak-article.pdf
```

Note: "LaTeX-Producer" is the conceptual agent role name (used in docs/config). `LaTeXAgent` is the Python class name.

---

## 4. LaTeX Pipeline + Article Structure

### 4.1 Compile Chain

```
lualatex main.tex   → first pass, builds .aux
biber main          → processes .bib → .bbl
lualatex main.tex   → injects citations
lualatex main.tex   → resolves ToC, cross-refs, hyperlinks
```

Wired in BOTH `latex/Makefile` (make-driven) AND `LaTeXCompileTool` (Python subprocess-driven).

### 4.2 Article Chapter Plan (≥15 pages total)

| Chapter | Title | Est. pages | Notes |
|---|---|---|---|
| Cover + ToC | — | 2 | TikZ-framed cover; fancyhdr headers/footers |
| Ch 1 | Introduction to Multi-Agent Orchestration | 2 | TikZ Crew block diagram (MANDATORY per L1708–1714) |
| Ch 2 | Agent Architectures & Topologies | 3 | Python-generated chart (framework comparison) |
| Ch 3 | LangChain, CrewAI & LangGraph Compared | 3 | Table (feature matrix, no overflow) |
| Ch 4 | Production Patterns: Gatekeeper, Rate Limits, Observability | 2 | Fancy math formula (token budget constraint) |
| Ch 5 | ביצור מסמכים עם סוכני AI (BiDi chapter) | 2 | Hebrew↔English mix, polyglossia/bidi package |
| Ch 6 | Case Study: This Article's Own Pipeline | 1 | OOP class diagram in TikZ (bonus "extra mile") |
| Bibliography | — | 1 | biblatex + biber, clickable citations |

**Total: ~16 pages** (safely above the 15-page floor).

### 4.3 LaTeX Repository Structure

```
latex/
├── main.tex
├── chapters/
│   ├── ch01_introduction.tex
│   ├── ch02_architectures.tex
│   ├── ch03_frameworks.tex
│   ├── ch04_production.tex
│   ├── ch05_bidi.tex               ← Hebrew↔English BiDi chapter
│   └── ch06_casestudy.tex
├── figures/
│   ├── crew_architecture.tikz      ← TikZ block diagram (MANDATORY)
│   ├── agent_topology.png          ← Python-generated matplotlib chart
│   └── cover_logo.png              ← image asset (H6)
├── bib/
│   └── references.bib
├── style/
│   └── article.sty                 ← fancyhdr, amsmath, biblatex, hyperref, polyglossia
├── Makefile
└── output/
    └── uoh-sqak-article.pdf        ← THE deliverable (committed)
```

### 4.4 Mandatory PDF Feature Verification

| Feature | Implementation | Grader check |
|---|---|---|
| Cover sheet | `\maketitle` with TikZ frame; topic + authors + date + 203.3763 + Dr. Yoram Segal | Visual |
| TOC | `\tableofcontents` | 4th compile pass |
| Headers/footers | `fancyhdr` | Every page |
| ≥1 image | `figures/cover_logo.png` | `\includegraphics` |
| Python chart | `tools/chart_generator.py` → `figures/agent_topology.png` | Script + PNG committed |
| ≥1 table (no overflow) | Framework comparison in ch03, `tabularx` | Visual |
| Fancy formula | Token-budget constraint in ch04: `\begin{equation}\sum_{i}...\end{equation}` | Visual |
| BiDi chapter | ch05, `polyglossia` + `\setotherlanguage{hebrew}` | Visual |
| Linked citations | `biblatex` + `\cite{}` + `hyperref` | Click test |
| TikZ block diagram | `crew_architecture.tikz` in ch01 | Visual |
| OOP class diagram | TikZ in ch06 (bonus) | Visual |

---

## 5. Testing Strategy

### 5.1 Test Tiers

```
tests/
├── unit/                          fast, fully mocked, no Claude calls
│   ├── test_gatekeeper.py         rate limit + token budget enforcement
│   ├── test_agents.py             config loading, skill injection
│   ├── test_tools.py              tool input/output contracts
│   ├── test_version.py            version string format
│   └── test_chart_generator.py    PNG output exists + non-zero bytes
├── integration/                   MockLLM, real lualatex
│   ├── test_article_crew.py       kickoff() → workspace/*.md files exist
│   └── test_latex_pipeline.py     .md → .tex + compile → PDF exists
└── conftest.py                    MockLLM fixture, tmp_workspace fixture
```

E2E (gated: `RUN_E2E=1`): real Claude CLI, real PDF, page-count check. Never in CI.

### 5.2 Quality Gates

| Gate | Tool | Trigger |
|---|---|---|
| Lint | `ruff check` (line-length=100, E/F/W/I/N/UP/B/C4/SIM) | pre-commit + CI |
| Coverage ≥85% | `pytest --cov` with `fail_under = 85` | CI |
| ≤150 lines/file | `scripts/check_file_lines.py` | pre-commit |
| No secrets | grep `sk-*` / `api_key=` | CI |
| LaTeX compiles | `make -C latex` | CI (MacTeX via brew) |

---

## 6. Configuration Architecture

All values in `config/*.json`, versioned at `"1.00"`. Zero hardcoded values in source.

```
config/
├── setup.json          version, package name, output paths
├── agents.json         per-agent: role, goal, backstory, llm, skill_ref, temperature
├── tasks.json          task descriptions + expected_output templates
├── crew.json           process type, verbose flag, agents+tasks list
├── rate_limits.json    RPM, tokens_per_article, daily cap, warn/hard thresholds
├── logging_config.json FIFO: 20 files × 500 lines
└── latex.json          compiler path, passes count, bib style, chapter list
```

---

## 7. Security + Versioning

- `.env` git-ignored; `.env-example` committed with placeholders
- `os.environ.get("ANTHROPIC_API_KEY")` only — never in source
- `.gitignore` includes `.env`, `*.aux`, `*.log`, `*.bbl`, `*.blg`, `*.toc`, `*.synctex.gz`
- `src/agent_article/shared/version.py` → `__version__ = "1.00"`; bump `+0.01` per change
- Every `config/*.json` carries `"version": "1.00"`

---

## 8. Extensibility (addressing HW1 weakness)

- **Agent registry**: add a new agent by dropping a file in `agents/` + registering in `config/agents.json`
- **Skill registry**: add a skill by dropping a directory in `skills/`
- **Tool registry**: subclass `BaseTool`, register in `config/tasks.json`
- **Lifecycle hooks**: `before_crew_kickoff`, `after_crew_kickoff`, `before_task`, `after_task`
- Document extension points in `docs/PLAN.md` AND `README.md`

---

## 9. Submission Checklist Snapshot

- [ ] `latex/output/uoh-sqak-article.pdf` committed and publicly accessible
- [ ] `uoh-sqak-ex03.pdf` (submission cover) generated via `scripts/fill_submission_pdf.py`
- [ ] Repo public at `https://github.com/salah-dev-stu/uoh-sqak-ex03`
- [ ] Both Salah and Andalus upload to Moodle id=270973 separately
- [ ] Self-grade field: 85

---

*Approved by Salah Qadah — 2026-06-06*
