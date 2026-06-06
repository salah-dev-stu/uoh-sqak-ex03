# Grading Rubric (distilled from `software_submission_guidelines-V3.pdf` + HW3 spec)

> The source PDF is 39 pages of Hebrew. Same rubric as HW1+HW2 — only the HW3-specific items differ. This document is the actionable summary plus HW3-specific items from `materials/hw3-spec-main-L06-summary-and-ex03-definition.pdf`. Read it carefully before starting.

## Quick-reference scorecard (R1-R13 — Table 5, page 33 of the PDF)

| # | Rule | Threshold | How it's audited |
|---|------|-----------|------------------|
| R1 | **SDK Architecture** | All business logic flows through an SDK layer | Code review |
| R2 | **OOP / no duplication** | Anything used 2+ times must be extracted (base class / mixin / Template Method). **Class diagram required.** | Code review + diagram |
| R3 | **API Gatekeeper** | All external API calls (LLMs, web search, LaTeX compile) through a centralized class | Code review + test |
| R4 | **Rate Limiting + Token Budget** | Defined in JSON config, never in code. Gatekeeper enforces. | Config test |
| R5 | **Wave management (queue)** | FIFO queue, backpressure, drain mechanism, no crashes when limits hit | Integration test |
| R6 | **Versioning** | Code + config versions start at `1.00`, `+0.01` per change | Version module check |
| R7 | **TDD** | Red → Green → Refactor, tests written before/with code | Work process |
| R8 | **File size** | ≤ 150 logical lines per Python file (excluding comments/blanks) | Automated count |
| R9 | **Linter** | `ruff check` returns 0 failures | ruff |
| R10 | **Test coverage** | `pytest --cov` ≥ 85% (`fail_under = 85` in pyproject.toml) | pytest |
| R11 | **Hardcoded values** | 0 in source — all values in config | Code review |
| R12 | **Secrets** | 0 in source — `.env-example` + `os.environ.get(...)`, `.env` git-ignored | Auto scan |
| R13 | **Package manager** | `uv` for everything (no pip/venv/virtualenv) | Auto |

## HW3-specific scorecard (from HW3 spec §13)

| # | Rule | Threshold | How it's audited |
|---|------|-----------|------------------|
| H1 | **15-page PDF** | **15 is the floor** (negotiated live in class L1678–1702, *"שיהיה חמש עשרה. סגרנו"*). Planning range 14–17 OK. Hebrew gives bonus credit but is NOT required end-to-end — English is fine if at least one chapter demonstrates Hebrew↔English BiDi (L1622–1629). | PDF page count + language scan |
| H2 | **Cover sheet** | Topic, author name(s), date, course code (203.3763), course name, lecturer (Dr. Yoram Segal) | PDF first page inspection |
| H3 | **Table of contents** | `\tableofcontents` populated correctly after 4 compile passes | PDF page 2 inspection |
| H4 | **Chapter division** | At least 4-5 named chapters, each with its own heading | PDF inspection |
| H5 | **Headers/footers** | LaTeX `fancyhdr` package: page number + book/article title at minimum | PDF inspection |
| H6 | **≥1 image** | Embedded raster/vector image (not just TikZ-only). PNG/JPG/PDF in `latex/figures/`. | PDF + repo audit |
| H7 | **≥1 Python-generated chart** | Created by code in `src/` (matplotlib/plotly/seaborn). Committed Python script + generated PNG. | PDF + repo audit (script must exist) |
| H8 | **≥1 table** | LaTeX `tabular` or `tabularx`. **Must not overflow the page** (Dr. Segal's verbatim check). | PDF inspection |
| H9 | **≥1 math formula** | Rendered with `amsmath` / `mathtools` as **"fancy formula, not plain text"** (literal English phrase MUST appear in LaTeX-Producer agent prompt — L1742–1748). If model emits flat text, request fix per spec §13.2. | PDF inspection + agent prompt review |
| H10 | **BiDi section** | At least one chapter demonstrates Hebrew↔English transitions correctly. Uses `bidi` or `polyglossia` package. | PDF inspection |
| H11 | **Bibliography with linked citations** | `.bib` file + **`biblatex` package** (NOT legacy `bibtex`) + **`biber`** compiler invoked + clicking citation in PDF jumps to bibliography entry. **If links don't jump, missing compilation pass — fail.** | PDF link test (open + click) + repo audit |
| H12 | **LaTeX project in repo** | `latex/main.tex` + `latex/bib/*.bib` + `latex/figures/*` + `latex/Makefile` committed to git | Repo audit |
| H13 | **LuaLaTeX OR XeLaTeX** | Equal preference per lecturer (L1706 verbatim *"לא משנה לי, ממש לא"* / "doesn't matter to me at all"). MiKTeX (Windows) or MacTeX (macOS) or TeXLive (Linux). **Overleaf FORBIDDEN** (L1622 verbatim *"לא, לא, ממש לא. אני מתעקש על זה"*) — must compile locally. | Makefile inspection + no Overleaf config |
| H14 | **4 compilation passes** | `lualatex → biber → lualatex → lualatex` (or `→ lualatex`) until citations + ToC + refs all settle | Makefile rules |
| H15 | **TikZ for block diagrams** | At least one `tikzpicture` block diagram. **The Crew architecture block diagram MUST appear inside the article PDF itself** (L1708–1714) — not just in repo docs. OOP class diagram inside the article = bonus path. | PDF + .tex inspection |
| H16 | **CrewAI multi-agent** | At minimum: Researcher / Writer / Editor / LaTeX-Producer. Real LLM calls (not stubbed). Configured via `config/agents.json`. | Code review + log inspection |
| H17 | **Skill layer** | Each agent has a `skills/<role>_skill/SKILL.md` (YAML frontmatter + Markdown body). Tools vs Skills clearly separated. | Repo audit |
| H18 | **Markdown→LaTeX intermediate** | Workflow first produces Markdown per chapter, then LaTeX-Producer converts to .tex | Code review (not strict, but recommended per spec) |
| H19 | **Hebrew or English output** | NOT Arabic. Dr. Segal can't read Arabic. | Output language scan |
| H20 | **Pairs only** | Confirmed Salah + Andalus | Submission check |
| H21 | **Each pair member uploads separately** to Moodle assignment id=270973 | Moodle |
| H22 | **Public repo OR shared with rmisegal@gmail.com** | HW2-lecturer-confirmed: inaccessible repo = auto-zero, no resubmit | Public verification |
| H23 | **Cost analysis** (rubric §11 + §17.5) | README must include token cost table for one full article generation | README inspection |
| H24 | **AI ethics disclosure** | README must include verbatim Hebrew + English ethics paragraph from syllabus | README inspection |
| H25 | **Continuous git commits** | ≥50 commits, conventional commit style, ≥4 per day during build week | Git history audit |

## Section-by-section requirements

### 1. README.md (root, mandatory)
Must read like a full user manual. **Carry over HW2's manual-grade structure:**
- **Installation**: prerequisites (Python 3.13+, uv, MiKTeX/TeXLive, optionally Claude CLI), step-by-step setup
- **Usage**: how to launch the menu, how to generate the article, how to compile the LaTeX
- **Examples & Demos**: code samples, **screenshots of menu + Crew runtime + generated PDF**
- **Architecture Diagram**: embed class diagram + IPC flow + CrewAI Crew graph
- **Configuration Guide**: explanation of every JSON config + every agent's `role`/`goal`/`backstory`
- **Sample PDF** — link to `latex/output/uoh-sqak-article.pdf` so grader can see the artifact without compiling
- **Cost analysis** (R11 + §17.5 mandate) — token table for one full article-generation run
- **AI Usage Disclosure** — verbatim Hebrew + English paragraph
- **Contribution Guidelines** + **License** (MIT)
- **HW1 Extensibility remediation section** — explicitly call out how this project addresses each transferable HW1 weakness

### 2. `docs/` folder (mandatory)
- **`docs/PRD.md`** — root Product Requirements Document with all standard sections
- **`docs/PLAN.md`** — architecture & technical plan:
  - **C4 Model** (Context, Container, Component, Code)
  - **UML** sequence diagram of one full Crew kickoff
  - **Class diagram** of OOP hierarchy (BaseAgent → ResearcherAgent / WriterAgent / EditorAgent / LaTeXAgent, Skill, Tool, Gatekeeper)
  - **ADRs**:
    - ADR-001: Why CrewAI over LangGraph for this task
    - ADR-002: Sequential vs Hierarchical Process (default: sequential)
    - ADR-003: Markdown-first vs LaTeX-first workflow
    - ADR-004: LuaLaTeX vs XeLaTeX (Hebrew rendering)
    - ADR-005: Same-provider vs mixed-provider per agent
    - ADR-006: Skill layer file format (YAML+Markdown)
    - ADR-007: Web search provider choice
  - **ISO/IEC 25010 paragraph** covering all 8 dimensions
- **`docs/TODO.md`** — full task list:
  - **MIN 500 tasks. Aim for 800.**
  - Phase breakdown matching IDEA.md phases 1-13
- **Per-mechanism PRDs** — for each significant component (Crew, Researcher, Writer, Editor, LaTeXAgent, Skill, Tools, Gatekeeper, Bibliography, Chart-Generator, BiDi-Handler)
- **`docs/PROMPTS.md`** — Prompt Engineering Log
  - Every agent's `role` + `goal` + `backstory` recorded with iterations
  - Every significant `Task.description` recorded
  - 5-field format (context, goal, prompt, output, improvements, best-practice)

### 3. Mandatory work process (page 9 of PDF)
1. Create `docs/PRD.md` and **get user approval** before continuing
2. Create `docs/PLAN.md`
3. Create `docs/TODO.md`
4. Create per-mechanism PRDs
5. **Approve all docs before development starts**
6. Develop with TODO.md as you go, updating as you progress
7. Save results, create visualizations, update README.md

### 4. Code structure
```
src/<package>/
├── sdk/                ← single entry point
├── agents/             ← CrewAI Agent definitions
├── crew/               ← Crew assembly, Process
├── tasks/              ← Task templates
├── tools/              ← Tool implementations
├── skills/             ← Skill directories (SKILL.md + refs + scripts)
├── shared/             ← gatekeeper, config, logger, version
├── menu/               ← TerminalMenu
├── constants.py
└── main.py
```

Max 150 logical lines per Python file. Use mixins / Template Method when needed.

### 5. SDK Architecture
```
External Consumers (Terminal Menu / CLI / Tests)
        |
        v
+-------+-------+
|     SDK       |  ← Single entry point for ALL logic
+-------+-------+
        |
        v
+-------+-------+
| Crew +        |  ← CrewAI Crew + Agents + Tasks
| Skills        |
+-------+-------+
        |
        v
+-------+-------+
| Infrastructure|  ← LLM API, web search, LaTeX compile, file I/O
+---------------+
```

### 6. Gatekeeper rules (§5)
All external calls go through `ApiGatekeeper`:
- LLM calls (Claude / OpenAI / Gemini via LangChain or CrewAI's built-in)
- Web search calls
- LaTeX compile invocations
- Bibliography lookup (e.g., Crossref API)

Rate limits + token budgets in `config/rate_limits.json`:
```json
{
  "version": "1.00",
  "services": {
    "claude_sonnet": {
      "requests_per_minute": 30,
      "tokens_per_article": 200000,
      "tokens_per_day": 500000,
      "price_input_per_million_tokens": 3.00,
      "price_output_per_million_tokens": 15.00,
      "warn_at_percent": 75,
      "hard_cap_percent": 95
    },
    "brave_search": {
      "requests_per_minute": 10
    }
  }
}
```

### 7. TDD (§6)
- RED → GREEN → REFACTOR
- Every public function gets ≥1 test
- Mock LLM + Mock web search + Mock LaTeX compile for unit tests
- Integration tests exercise the full Crew with MockLLM (NO real Claude calls in CI)
- E2E tests gated by `RUN_E2E=1`
- Coverage ≥85% global (`fail_under = 85` in pyproject)

### 8. Linter — Ruff
```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "SIM"]
ignore = ["E501"]
```

### 9. No hardcoded values
| Category | Wrong | Right |
|---|---|---|
| LLM model | `"claude-sonnet-4-5"` in code | `cfg.get("model")` |
| Chapter count | `n_chapters = 5` in code | `cfg.get("chapter_count", 5)` |
| Page target | `target_pages = 15` | `cfg.get("target_pages", 15)` |
| Agent goal text | hardcoded in agent file | `config/agents.json::agents.researcher.goal` |

### 10. Configuration architecture
```
config/
├── setup.json            ← global app config (versioned)
├── agents.json           ← per-agent: role, goal, backstory, llm, skill_ref
├── tasks.json            ← task templates per chapter
├── crew.json             ← Crew assembly: agents, tasks, process type
├── rate_limits.json      ← API rate limits + token budgets (versioned)
├── logging_config.json   ← FIFO log rotation (versioned)
├── latex.json            ← compiler choice, package list, BiDi config
.env                      ← secrets (git-ignored)
.env-example              ← placeholders (committed)
pyproject.toml            ← build / lint / test settings
src/<package>/constants.py  ← immutable enums
```

### 11. Information security
- No API keys, passwords, tokens in source code
- `os.environ.get("ANTHROPIC_API_KEY")` only
- `.gitignore`: `.env`, `*.key`, `*.pem`, `credentials.json`, `latex/output/*.aux`, `*.log`, `*.toc`, `*.bbl`, `*.blg`, `*.synctex.gz`
- `.env-example` committed with placeholders

### 12. Versioning (§8.1)
| Item | Location | Initial value |
|---|---|---|
| Code version | `src/<package>/shared/version.py` | `1.00` |
| Setup config | `config/setup.json` `"version"` | `1.00` |
| Agents config | `config/agents.json` `"version"` | `1.00` |
| Tasks config | `config/tasks.json` `"version"` | `1.00` |
| Crew config | `config/crew.json` `"version"` | `1.00` |
| Rate limits | `config/rate_limits.json` `"version"` | `1.00` |
| LaTeX config | `config/latex.json` `"version"` | `1.00` |
| Logging | `config/logging_config.json` `"version"` | `1.00` |

### 13. Git workflow
- Continuous commits, conventional commit style (`feat(crew):`, `fix(latex):`, `docs(prd):`, etc.)
- Use feature branches when needed; merge to `main` for visibility
- Tag `v1.00` at submission
- **HW2 lesson**: 138 commits worked well, ≥50 commits is the floor

### 14. Prompt Engineering Log (`docs/PROMPTS.md`)
5 required fields per entry:
- Context (what we were trying to do)
- Goal (what output we wanted)
- The actual prompt text
- Example output received
- Iterative improvements (what we changed and why)
- Best practice extracted (reusable lesson)

For HW3 specifically: log every CrewAI agent prompt (role + goal + backstory), every Task description, every coding prompt to Claude during development. Aim ≥25 entries (HW2 had 21).

### 15. uv as package manager (§8.4)
**MUST** use `uv`. **CANNOT** use: `pip install`, `python -m`, `venv`, `virtualenv`.

| Task | Right (uv) | Wrong |
|---|---|---|
| Install dependencies | `uv sync` | `pip install` |
| Add a dependency | `uv add crewai` | `pip install crewai` |
| Run a script | `uv run python script.py` | `python script.py` |
| Run tests | `uv run pytest tests/` | `python -m pytest` |
| Lock dependencies | `uv lock` | `pip freeze` |

### 16. Extension architecture (§12.1)
HW1 was flagged here. Don't repeat. For HW3:
- **Agent registry** — adding a new agent (e.g., "Fact-Checker") = drop a file + register
- **Skill registry** — adding a new skill = drop a directory under `src/<pkg>/skills/`
- **Tool registry** — adding a tool = subclass of `BaseTool` (CrewAI's native pattern)
- **Lifecycle hooks** — `before_crew_kickoff`, `after_crew_kickoff`, `before_task`, `after_task`, `before_llm_call`, `after_llm_call`
- **API-first** — every component exposes a clean interface
- Document extension points in `docs/PLAN.md` AND `README.md`.

### 17. ISO/IEC 25010 quality dimensions (§13.1)
One paragraph per dimension in `docs/PLAN.md`:
1. **Functional Suitability** — generates 15-page PDF with all content requirements
2. **Performance Efficiency** — < 5 min per chapter generation; < 30s LaTeX compile
3. **Compatibility** — works on macOS, Linux, WSL
4. **Usability** — terminal menu navigable by keyboard
5. **Reliability** — Gatekeeper handles LLM timeouts gracefully
6. **Security** — no secrets, rate-limited, sandboxed LaTeX compile
7. **Maintainability** — modular Crew, swappable agents, swappable LaTeX engine
8. **Portability** — `uv sync` reproducible, `MAKEFILE` portable

### 18. Building blocks design (§16.3)
Every significant class gets Input/Output/Setup docstring:
```python
class WriterAgent:
    """
    Input:  research_notes (List[ResearchNote]), chapter_outline (Outline)
    Output: chapter_markdown (str)
    Setup:  llm_provider (LLMProvider), skill_path (Path), style_guide (str)
    """
    ...
```

### 19. Parallel processing
CrewAI's `Process.sequential` is single-threaded. For bonus, `Process.hierarchical` adds a manager agent. If implementing concurrent agent runs (e.g., parallel research over multiple topics), use `multiprocessing.Pool` or `asyncio.gather`. Document thread safety + lock protection in ADR.

### 20. Final checklist
Before submission:

**Documentation & structure**:
- [ ] Comprehensive README.md at root (manual-grade + sample PDF embed/link + cost table + AI ethics)
- [ ] `docs/` folder with PRD.md, PLAN.md, TODO.md (≥500 tasks)
- [ ] Per-mechanism PRDs for every component (researcher, writer, editor, latex agent, skill, tools, gatekeeper)
- [ ] 4 architecture diagrams: C4 context + C4 container + class diagram + UML sequence
- [ ] PROMPTS.md with ≥25 entries

**Architecture & code**:
- [ ] SDK as single entry point
- [ ] OOP class diagram matches code
- [ ] Gatekeeper handles all external calls
- [ ] Rate limits + token budget in JSON
- [ ] Files ≤150 lines
- [ ] 4 CrewAI agents minimum (Researcher + Writer + Editor + LaTeXProducer)
- [ ] Skills directory under each role
- [ ] Real LLM calls (no faked content)

**Tests & quality**:
- [ ] Coverage ≥85%
- [ ] Ruff: 0 errors
- [ ] All files ≤150 lines
- [ ] Pre-commit hook configured (ruff + line + pytest unit)
- [ ] GitHub Actions CI workflow

**Configuration & security**:
- [ ] All configs versioned at 1.00
- [ ] `.env-example` with placeholders
- [ ] No secrets in code
- [ ] `.gitignore` includes LaTeX intermediate files (.aux, .log, .bbl, .blg)

**LaTeX deliverable**:
- [ ] `latex/main.tex` compiles cleanly
- [ ] Cover sheet present with all 5 fields
- [ ] TOC populated
- [ ] ≥1 image embedded
- [ ] ≥1 Python-generated chart
- [ ] ≥1 table fits page
- [ ] ≥1 fancy math formula
- [ ] BiDi section with Hebrew↔English transition
- [ ] Linked bibliography (citations clickable)
- [ ] TikZ block diagram
- [ ] Page count 14-17
- [ ] Hebrew language used heavily (for the bonus)
- [ ] Makefile runs `lualatex → biber → lualatex → lualatex`
- [ ] Output `latex/output/uoh-sqak-article.pdf` committed

**Submission**:
- [ ] GitHub repo PUBLIC at `https://github.com/salah-dev-stu/uoh-sqak-ex03`
- [ ] Repo URL verified anonymously (incognito window)
- [ ] `uoh-sqak-ex03.pdf` (submission cover) generated via `scripts/fill_submission_pdf.py`
- [ ] Salah uploads to Moodle id=270973
- [ ] Andalus uploads same PDF to her Moodle separately

## Self-grade strategy

HW1 self-graded at 90 → actual 85.54 (over-claimed by 4.5 pts → "rigorous lens" scrutiny). HW2 not yet graded — can't recalibrate.

**Recommended HW3 self-grade**: `85` placeholder. Bump to 88-90 only if all transferable weaknesses (planning, config portability, extensibility, quality automation) are genuinely addressed AND the PDF is technically perfect.

**Never claim more than 92.** The rubric's "elephant-in-the-needle" strict-mode kicks in.

## How the lecturer will probably grade

1. Open the GitHub repo URL — verify accessibility (auto-zero if 404)
2. Read README.md — verify it's manual-grade, has sample PDF link, has cost table
3. Open `latex/output/uoh-sqak-article.pdf` — the central artifact
4. Click 2-3 citation links — verify they jump (the "envelope" check)
5. Scroll the PDF — look for Hebrew, formulas, tables, TikZ diagram, BiDi section
6. Run `ruff check`, `pytest --cov`, file-line counter, secrets scan
7. Inspect `docs/` for PRD + PLAN + TODO + per-mechanism PRDs
8. Inspect git history density
9. Spot-check `latex/main.tex` source — verify the LaTeX is well-organized
10. Spot-check `src/agent_article/` — verify the CrewAI architecture is real
11. Read PROMPTS.md — sample 2-3 entries
12. Apply self-grade-modulated strictness

## Important note (page 33 of PDF, end)
> "מומלץ להשתמש בכלי LLM וסוכני AI לעזרה בהשלמת הפרויקט. מובהר כי כחלק מהבדיקה יתכן וייעשה שימוש בסוכני AI לביצוע הבדיקה."
> *"Recommended to use LLM tools and AI agents to help complete the project. As part of the inspection, AI agents may be used to perform the check."*

The lecturer encourages using AI agents — and this whole worker session is literally that. Just document the prompts in `docs/PROMPTS.md` per the ethics policy.
