# Technical Plan — HW3 Article Generation Pipeline

**Version:** 1.00
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa
**Date:** 2026-06-06

---

## 1. Architecture Overview

### 1.1 Seven-Layer Stack

```
┌─────────────────────────────────────────────┐
│  Layer 7: Terminal Menu (menu/tui.py)        │  Rich TUI, letter-keyed
├─────────────────────────────────────────────┤
│  Layer 6: SDK (sdk/sdk.py)                   │  Sole public surface (R1)
├─────────────────────────────────────────────┤
│  Layer 5: ArticleCrew (crew/article_crew.py) │  Process.sequential
├─────────────────────────────────────────────┤
│  Layer 4: Agents × 4 (agents/*.py)           │  Skill-augmented
│           + Tasks × 4 (tasks/article_tasks)  │
├─────────────────────────────────────────────┤
│  Layer 3: Tools × 5 (tools/*.py)             │  WebSearch, FileRW,
│                                              │  LaTeXCompile, ChartGen
├─────────────────────────────────────────────┤
│  Layer 2: ApiGatekeeper (shared/gatekeeper)  │  ALL external calls (R3)
├─────────────────────────────────────────────┤
│  Layer 1: Infrastructure                     │  Claude CLI / DuckDuckGo
│                                              │  / lualatex subprocess
└─────────────────────────────────────────────┘
```

### 1.2 Data Flow

```
User: menu → "G) Generate Article"
          ↓
SDK.generate_article(topic)
          ↓
ResearcherAgent → workspace/research_notes.md      (LLM + DuckDuckGo)
          ↓
WriterAgent     → workspace/chapters/ch01-06.md    (LLM + FileRW)
          ↓
EditorAgent     → workspace/chapters/ch*_edited.md (LLM + FileRW)
          ↓
    [HUMAN CHECKPOINT] SDK.approve_markdown() → "Approve? [y/N]"
          ↓ y
LaTeXAgent → latex/chapters/*.tex                  (LLM + FileRW)
           → latex/bib/references.bib
           → latex/figures/agent_topology.png       (ChartGenerator)
           → lualatex → biber → lualatex → lualatex (LaTeXCompile)
          ↓
latex/output/uoh-sqak-article.pdf
          ↓
SDK returns ArticleResult(pdf_path, token_cost, warnings)
```

---

## 2. C4 Model

### 2.1 Context Diagram

```
┌──────────────────────────────────────────────────┐
│                  System Context                   │
│                                                   │
│  [Student/Grader]                                 │
│       │ runs `uv run agent-article`               │
│       ▼                                           │
│  [agent-article CLI]  ──── [Claude CLI] ────────► │
│       │                         (LLM provider)    │
│       │               ──── [DuckDuckGo] ─────────►│
│       │                         (web search)      │
│       └──────────────── [lualatex/biber] ─────────│
│                              (PDF compiler)       │
└──────────────────────────────────────────────────┘
```

### 2.2 Container Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  agent-article package (src/agent_article/)                 │
│                                                             │
│  ┌──────────────┐   ┌───────────────┐   ┌───────────────┐  │
│  │  Terminal UI  │   │  ArticleSDK   │   │  ArticleCrew  │  │
│  │  (menu/tui)  │──▶│  (sdk/sdk.py) │──▶│  (crew/)      │  │
│  └──────────────┘   └───────────────┘   └───────────────┘  │
│                                                ▼            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agents (ResearcherAgent, WriterAgent, EditorAgent,  │   │
│  │           LaTeXAgent) each with SKILL.md             │   │
│  └──────────────────────────────────────────────────────┘   │
│                               ▼                             │
│  ┌───────────┐  ┌──────────┐  ┌────────────┐  ┌─────────┐  │
│  │WebSearch  │  │ FileRW   │  │LaTeXCompile│  │ChartGen │  │
│  │Tool       │  │Tool      │  │Tool        │  │Tool     │  │
│  └───────────┘  └──────────┘  └────────────┘  └─────────┘  │
│                               ▼                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ApiGatekeeper — all external calls route here      │    │
│  └─────────────────────────────────────────────────────┘    │
│                               ▼                             │
│  Claude CLI | DuckDuckGo | lualatex subprocess               │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Component Diagram (agents module)

```
agents/
├── base_agent.py         BaseAgent(ABC)
│                         - config_key: str
│                         - skill: FileSkill
│                         - tools: list[BaseTool]
│                         + build() → crewai.Agent  [abstract]
│                         # _make_agent() → crewai.Agent
├── researcher_agent.py   ResearcherAgent(BaseAgent)
├── writer_agent.py       WriterAgent(BaseAgent)
├── editor_agent.py       EditorAgent(BaseAgent)
└── latex_agent.py        LaTeXAgent(BaseAgent)
```

---

## 3. UML Sequence Diagram — Full Crew Kickoff

```
User      TUI       SDK         ArticleCrew  Researcher  Writer  Editor  LaTeX
 │         │         │               │            │          │       │       │
 │ presses G│         │               │            │          │       │       │
 │─────────▶│         │               │            │          │       │       │
 │         │generate_│               │            │          │       │       │
 │         │article()│               │            │          │       │       │
 │         │────────▶│               │            │          │       │       │
 │         │         │kickoff(topic) │            │          │       │       │
 │         │         │──────────────▶│            │          │       │       │
 │         │         │               │run(research│          │       │       │
 │         │         │               │task)       │          │       │       │
 │         │         │               │───────────▶│          │       │       │
 │         │         │               │            │search+write       │       │
 │         │         │               │            │────────────────▶  │       │
 │         │         │               │            │ workspace/        │       │
 │         │         │               │            │ research_notes.md │       │
 │         │         │               │◀───────────│          │       │       │
 │         │         │               │run(write   │          │       │       │
 │         │         │               │task)       │          │       │       │
 │         │         │               │──────────────────────▶│       │       │
 │         │         │               │            │  read notes+write │       │
 │         │         │               │            │  ch01-06.md       │       │
 │         │         │               │◀───────────────────────        │       │
 │         │         │               │run(edit    │          │       │       │
 │         │         │               │task)       │          │       │       │
 │         │         │               │─────────────────────────────▶ │       │
 │         │         │               │            │       read+edit   │       │
 │         │         │               │            │       *_edited.md │       │
 │         │         │               │◀─────────────────────────────  │       │
 │         │         │◀──────────────│(edit done) │          │       │       │
 │         │approve_ │               │            │          │       │       │
 │         │markdown()               │            │          │       │       │
 │◀────────│"Approve?│               │            │          │       │       │
 │presses y│         │               │            │          │       │       │
 │────────▶│         │               │            │          │       │       │
 │         │         │               │run(latex   │          │       │       │
 │         │         │               │task)       │          │       │       │
 │         │         │               │──────────────────────────────────────▶│
 │         │         │               │            │      read .md → .tex      │
 │         │         │               │            │      chart→PNG            │
 │         │         │               │            │      lualatex×4           │
 │         │         │               │◀──────────────────────────────────────│
 │         │         │◀──────────────│(pdf done)  │          │       │       │
 │         │◀────────│ArticleResult  │            │          │       │       │
 │◀────────│"PDF:..." │               │            │          │       │       │
```

---

## 4. Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENTS                                                         │
│                                                                 │
│  <<abstract>>                                                   │
│  BaseAgent                                                      │
│  ─────────────────────────────────────────────────────────     │
│  - config_key: str                                              │
│  - _cfg: dict                                                   │
│  - _skill: FileSkill                                            │
│  - _tools: list[BaseTool]                                       │
│  ─────────────────────────────────────────────────────────     │
│  + __init__(config_key, tools)                                  │
│  + build() → Agent  [abstract]                                  │
│  # _make_agent() → Agent                                        │
│  ──────────────┬──────────────────┬────────────┬───────────    │
│               ╱│╲                 │            │        │       │
│  ResearcherAgent WriterAgent  EditorAgent  LaTeXAgent  │       │
│  + build()    + build()       + build()    + build()   │       │
└──────────────────────────────────────────────────────────/─────┘

┌──────────────────────────────────────────────────────────────┐
│  TOOLS                                                        │
│                                                               │
│  <<abstract>>                                                 │
│  BaseTool                                                     │
│  ──────────────────────────────────────────────────────      │
│  + name: str  [abstract property]                             │
│  + description: str  [abstract property]                      │
│  + run(*args, **kwargs) → Any  [abstract]                     │
│  + as_crewai_tool() → Any                                     │
│  ──────────────┬──────────────┬──────────────┬────────┐      │
│               ╱│╲             │              │        │       │
│  WebSearchTool FileReadTool FileWriteTool LaTeXCompileTool    │
│                                           ChartGeneratorTool  │
└───────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SKILLS                                                       │
│                                                               │
│  <<abstract>>                                                 │
│  BaseSkill                                                    │
│  ──────────────────────────────────────────────────────      │
│  + content: str  [abstract property]                          │
│  ─────────────────────────                                    │
│  FileSkill(BaseSkill)                                         │
│  - _skill_path: Path                                          │
│  + __init__(skill_ref: str | Path)                            │
│  + content: str                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SHARED INFRASTRUCTURE                                        │
│                                                               │
│  ApiGatekeeper  [Singleton]                                   │
│  - _instance: ApiGatekeeper                                   │
│  - _cfg: dict                                                 │
│  - _usage: dict[str, UsageRecord]                             │
│  - _call_times: dict[str, deque]                              │
│  + instance() → ApiGatekeeper  [classmethod]                  │
│  + call(service, fn, *args) → Any                             │
│  + get_spend_report() → dict                                  │
│                                                               │
│  StructuredLogger                                             │
│  - _component: str                                            │
│  - _fh: file                                                  │
│  + info(message, **fields)                                    │
│  + error(message, **fields)                                   │
│  + warning(message, **fields)                                 │
│                                                               │
│  ConfigLoader  [module-level singleton via _cache dict]       │
│  + get_config(name) → dict                                    │
│  + cfg(name, key, default) → Any                              │
│  + reload()                                                   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SDK + CREW                                                   │
│                                                               │
│  ArticleSDK                                                   │
│  + generate_article(topic: str) → CrewResult                  │
│  + approve_markdown() → bool                                  │
│  + compile_pdf() → str                                        │
│  + get_spend_report() → dict                                  │
│  + run_audit() → dict                                         │
│                                                               │
│  ArticleCrew                                                  │
│  - _cfg: dict                                                 │
│  + kickoff(topic, extra_inputs) → CrewResult                  │
│                                                               │
│  @dataclass CrewResult                                        │
│  - raw_output: str                                            │
│  - pdf_path: str | None                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Architectural Decision Records (ADRs)

### ADR-001: CrewAI over LangGraph

**Status:** Accepted
**Context:** Need to orchestrate 4 sequential AI agents for an article writing pipeline.
**Decision:** Use CrewAI `Process.sequential` rather than LangGraph.
**Rationale:** Article writing is a closed linear pipeline (research → write → edit → compile). LangGraph's directed graph model adds structural complexity with no benefit for a fixed-order workflow. CrewAI's `Role/Goal/Backstory` model directly maps to the agent personality requirements in the spec.
**Consequences:** No cyclic workflows possible; acceptable for this use case.

### ADR-002: Sequential over Hierarchical Process

**Status:** Accepted
**Context:** CrewAI supports `Process.sequential` and `Process.hierarchical`.
**Decision:** Use `Process.sequential`.
**Rationale:** Article chapters have strict write order (research first, then chapters, then editing, then LaTeX). A manager agent (hierarchical) would add token cost and complexity without enabling parallel chapter writing (which would require post-merge editing anyway).
**Consequences:** No parallelism; acceptable given ≤20-minute target.

### ADR-003: Markdown-First Workflow

**Status:** Accepted
**Context:** LaTeXAgent must produce valid `.tex` files. Agents could write LaTeX directly or write Markdown first.
**Decision:** Markdown-first: all writing agents produce `.md`, LaTeXAgent converts to `.tex`.
**Rationale:** Dr. Segal's own recommended workflow (Lecture 6, L1712). Markdown intermediates are human-readable for the approval checkpoint, debuggable, and easier to iterate on than raw LaTeX. Shorter LLM prompts (no LaTeX syntax noise for Writer/Editor).
**Consequences:** Extra LaTeXAgent task for conversion; worth it for debuggability.

### ADR-004: LuaLaTeX over XeLaTeX

**Status:** Accepted
**Context:** Hebrew BiDi requires a Unicode-aware LaTeX compiler.
**Decision:** LuaLaTeX.
**Rationale:** Dr. Segal stated both are equally acceptable (Lecture 6, L1722: "same thing"). LuaLaTeX chosen for its mature Lua scripting support and the existing `polyglossia` + `fontspec` integration.
**Consequences:** System must have LuaLaTeX installed (MacTeX or TeXLive).

### ADR-005: Single LLM Provider (Claude CLI)

**Status:** Accepted
**Context:** Could use different LLM providers per agent (Researcher = GPT-4, Writer = Claude, etc.).
**Decision:** Single provider: Claude CLI login for all agents.
**Rationale:** Voice consistency across chapters — same model avoids stylistic inconsistency in the written article. Claude CLI login avoids API key management. Single provider simplifies `ApiGatekeeper` configuration.
**Consequences:** All agents share the same rate limits; no provider diversity experiment.

### ADR-006: File-Based Skill Layer

**Status:** Accepted
**Context:** Need a way to inject agent-specific expertise beyond the `backstory` field.
**Decision:** File-based skills: `SKILL.md` files read at runtime by `FileSkill`.
**Rationale:** Matches spec Appendix A requirement exactly. File-based skills are version-controlled, human-readable, editable without code changes, and can be viewed by the grader as clear evidence of the skill layer implementation.
**Consequences:** Skills must be read from disk on each agent build; cheap operation.

### ADR-007: DuckDuckGo for Web Search

**Status:** Accepted
**Context:** ResearcherAgent needs web search access.
**Decision:** DuckDuckGo via `duckduckgo-search` package.
**Rationale:** No API key required. Free. Returns structured results. Sufficient for searching well-indexed academic/tech content (LangChain, CrewAI, agent architecture papers). Avoids Serper.dev / Tavily API key complexity.
**Consequences:** Rate limits apply; handled by `ApiGatekeeper` at 5 RPM.

---

## 6. ISO/IEC 25010 Quality Model

This project targets the following quality dimensions:

| Dimension | Target | Implementation |
|---|---|---|
| **Functional suitability** | All 20 H-rules satisfied | `run_audit()` + manual PDF inspection |
| **Performance efficiency** | ≤25 min full pipeline | Rate limit config, FIFO logging |
| **Compatibility** | macOS + Linux (CI) | `pyproject.toml` platform-agnostic dependencies |
| **Usability** | TUI menu, approval checkpoint | `rich` library, human-in-the-loop |
| **Reliability** | GatekeeperError on overrun, log on warning | `ApiGatekeeper`, `StructuredLogger` |
| **Security** | Zero secrets in code, `.env` gitignored | Pre-commit scan, `.env-example` |
| **Maintainability** | ≤150 lines/file, BaseAgent/Tool/Skill ABCs, 7 ADRs | `check_file_lines.py`, OOP hierarchy |
| **Portability** | `git clone && uv sync && uv run` | `uv.lock`, no hardcoded paths |

---

## 7. Extension Points

### 7.1 Adding a New Agent

1. Create `src/agent_article/agents/new_agent.py` subclassing `BaseAgent`
2. Add entry to `config/agents.json` with `role`, `goal`, `backstory`, `skill_ref`
3. Create `src/agent_article/skills/new_skill/SKILL.md`
4. Add to `ArticleCrew.kickoff()` agent list and `build_tasks()` task list
5. No other code changes required

### 7.2 Adding a New Tool

1. Create `src/agent_article/tools/new_tool.py` subclassing `BaseTool`
2. Implement `name`, `description`, `run()` properties/methods
3. Add to the relevant agent's tool list in `agents/*.py`
4. Add to `config/rate_limits.json` if the tool makes external calls

### 7.3 Adding a New Skill

1. Create `src/agent_article/skills/new_skill/SKILL.md`
2. Reference the skill by directory name in `config/agents.json` `skill_ref` field
3. No code changes required — `FileSkill` auto-discovers by directory name

### 7.4 Lifecycle Hooks (Future Extension)

Pre-wired hook points (currently no-ops):
```python
# ArticleCrew.kickoff() already calls these:
before_crew_kickoff(topic: str)
after_crew_kickoff(result: CrewResult)
before_task(task_name: str)
after_task(task_name: str, output: str)
```

---

## 8. Article Structure Plan

| Section | File | Pages | Key Features |
|---|---|---|---|
| Cover + TOC | `main.tex` | 2 | `\maketitle` + TikZ frame; `\tableofcontents` |
| Ch1: Introduction | `ch01_introduction.tex` | 2 | TikZ Crew block diagram (MANDATORY) |
| Ch2: Agent Architectures | `ch02_architectures.tex` | 3 | Python chart (bar chart of framework scores) |
| Ch3: Framework Comparison | `ch03_frameworks.tex` | 3 | Table (LangChain vs CrewAI vs LangGraph) |
| Ch4: Production Patterns | `ch04_production.tex` | 2 | Fancy math formula (token budget equation) |
| Ch5: ביצור מסמכים (BiDi) | `ch05_bidi.tex` | 2 | Hebrew↔English, `polyglossia` |
| Ch6: Case Study | `ch06_casestudy.tex` | 2 | OOP class diagram in TikZ |
| Bibliography | `main.tex` `\printbibliography` | 1 | biblatex, ≥5 entries, clickable |
| **Total** | | **≥17** | Safety margin above 15-page floor |

---

## 9. Configuration Architecture

```
config/
├── setup.json          {"version": "1.00", "workspace_dir": "workspace", ...}
├── agents.json         {"version": "1.00", "agents": { "researcher": {...}, ...}}
├── tasks.json          {"version": "1.00", "tasks": { "research": {"description": "..."}, ...}}
├── crew.json           {"version": "1.00", "process": "sequential", "verbose": true}
├── rate_limits.json    {"version": "1.00", "services": {"claude_cli": {"rpm": 10, ...}}}
├── logging_config.json {"version": "1.00", "fifo_files": 20, "max_lines_per_file": 500}
└── latex.json          {"version": "1.00", "compiler": "lualatex", "passes": 4, ...}
```

All config files carry `"version": "1.00"`. Zero hardcoded values in Python source.

---

## 10. Test Strategy

| Test tier | Location | Scope | LLM |
|---|---|---|---|
| Unit | `tests/unit/` | Single class/function, fully mocked | MockLLM |
| Integration | `tests/integration/` | Multi-component, real filesystem, real lualatex | MockLLM |
| E2E | (manual, `RUN_E2E=1`) | Full pipeline, real Claude CLI | Real Claude |

**CI runs:** unit + integration only. E2E never in CI (token cost).

**Coverage target:** 85% enforced via `fail_under = 85` in `pyproject.toml`.

---

---

## 11. Fast Pipeline — Haiku + Parallel LaTeX (FP-01)

**Status:** Approved (2026-06-09). See `docs/PRD_fast_pipeline.md` for full spec.

### 11.1 Motivation

Sequential `claude -p` calls at Sonnet model take 8–15 min each. With 3 sequential agents + 7 LaTeX tasks, total wall-clock was 60–80 min. Target: ≤ 10 min.

### 11.2 Two-Phase Architecture

```
Phase 1 — Sequential (unchanged, CrewAI Process.sequential):
  ResearcherAgent [Haiku] → WriterAgent [Haiku] → EditorAgent [Haiku]

Phase 2 — Parallel (Python ThreadPoolExecutor, outside CrewAI):
  Thread 1: latex_ch01 [Haiku]   Thread 2: latex_ch02 [Haiku]
  Thread 3: latex_ch03 [Haiku]   Thread 4: latex_ch04 [Haiku]
  Thread 5: latex_ch05 [Sonnet]  Thread 6: latex_ch06 [Haiku]
  Thread 7: latex_bib  [Haiku]
  (wall-clock = slowest thread = ch05 Sonnet ≈ 2 min)

Phase 3 — Compile (lualatex × 4 passes, unchanged):
  lualatex → biber → lualatex → lualatex
```

**Why ch05 uses Sonnet:** BiDi chapter requires exact `\begin{hebrew}...\end{hebrew}` blocks, `\hebrewheadingformat` / `\defaultheadingformat` calls, and `\addtocontents{toc}{...}` with RTL dot leaders. Haiku consistently drops these details.

### 11.3 Model Configuration

```json
// config/setup.json
"default_model": "claude-haiku-4-5-20251001"

// config/tasks.json — per task
"latex_ch05": {
  "model": "claude-sonnet-4-6",
  "description": "..."
}
// all other latex_ch* tasks inherit default_model (haiku)
```

### 11.4 Threading Model

```python
# crew/article_crew.py
def _run_latex_phase_parallel(self, tasks: list[Task]) -> list[str]:
    from concurrent.futures import ThreadPoolExecutor
    max_workers = min(len(tasks), os.cpu_count() or 4)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(self._run_single_latex_task, t): t for t in tasks}
        return [f.result() for f in futures.values()]
```

Each thread calls the task's agent directly (bypassing CrewAI's sequential lock) and writes output to `task.output_file`. Threads are independent — no shared mutable state.

### 11.5 Agent Prompt Quality Rules

To prevent manual post-processing, these rules are encoded into all `latex_ch*` task descriptions and into `latex/skills/latex_skill/SKILL.md`:

1. Output ONLY LaTeX — first character must be `%` or `\`
2. Tables: always use `p{Xcm}` column types, never bare `l`/`r`/`c`
3. Citation keys: use EXACTLY the `[AuthorYear]` keys from `workspace/research_notes.md`
4. No markdown fences (` ```latex `) or trailing prose after the closing `\end{...}` 
5. `latex_bib`: generate entries for EVERY `[AuthorYear]` key used in any chapter

### 11.6 Updated Timing Estimate

| Phase | Before FP-01 | After FP-01 |
|---|---|---|
| ResearcherAgent | ~8 min (Sonnet) | ~2 min (Haiku) |
| WriterAgent | ~12 min (Sonnet) | ~3 min (Haiku) |
| EditorAgent | ~8 min (Sonnet) | ~2 min (Haiku) |
| 7 LaTeX tasks | ~35 min sequential | ~2 min parallel (ch05 Sonnet gating) |
| LaTeX compile | ~1.5 min | ~1.5 min |
| **Total** | **~65 min** | **≤10 min** |

---

*PLAN Version 1.01 — Salah Qadah, Andalus Kalash — 2026-06-09 (§11 added: fast pipeline)*
