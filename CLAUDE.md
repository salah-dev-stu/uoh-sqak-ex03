# HW3 Worker Session — Orchestration of AI Agents (Course 203.3763)

## Who you are
You are the **HW3 worker session**. The orchestrator session (in `/Users/salah/Projects/orch-ai-agents/`) has read the course materials, downloaded everything from Moodle, transcribed the lecture (when whisper finishes), and distilled the rubric. It scaffolded this directory for you:

- **`CLAUDE.md`** (this file) — orientation, the rules, the workflow, gotchas
- **`IDEA.md`** — vibe input you feed into Plan Mode to generate the PRD
- **`RULES.md`** — distilled grading rubric (the source PDF is 39 pages of Hebrew; this is the actionable summary)
- **`CONTEXT-lecture-06.md`** — Lec 06 transcript digest (Dr. Segal's verbatim guidance on LangChain/CrewAI/LaTeX — written after whisper finishes)
- **`CONTEXT-lec06-pdfs.md`** — deep digest of all 5 Lec 06 PDFs (CrewAI Part A+B, LangChain, Agent Architecture 2026, Spec)
- **`CONTEXT-rubric-and-pdfs.md`** — distilled rubric (carry over from HW2; same software_submission_guidelines-V3.pdf)
- **`IDEA-raw.txt`** — raw Hebrew text extraction from the HW3 spec PDF (backup for verbatim quoting)

The user runs you in a separate window. When you finish (or get blocked), they go back to the orchestrator with results.

## Course context
- **Course**: 203.3763 — "Orchestration of AI Agents" (אורקסטרציה של סוכני AI)
- **Institution**: University of Haifa, Spring 2026 (תשפ"ו, semester ב)
- **Lecturer**: Dr. Yoram Reuven Segal — `rmisegal@gmail.com`
- **Today**: orchestrator will inject current date on handoff
- **HW3 deadline**: **Friday, 12 June 2026, 23:59** (Asia/Jerusalem) — Moodle assignment `id=270973`. Opens 29 May 2026. Confirmed by orchestrator on 2026-06-06 ~11:30 — remaining time at that moment was ≈ 6 days 12 hours.
- **Late penalty**: −5 points per 24h (no special request needed)
- **Grade weight**: HW3 ≈ 10% of course (60% homeworks ÷ 6 assignments)

## Previous assignment results
- **HW1 final grade**: **85.54/100** (75.54 pre-bonus + 10 automatic compensation bonus). Below the 92 target. Self-grade was 90; over-claim triggered "especially rigorous lens" scrutiny.
- **HW2**: submitted 29 May 2026 11:31 AM (well before deadline). **NOT YET GRADED.** No feedback available to inform HW3 calibration; rely on HW1 lessons + own engineering judgement.
- **HW1 feedback** at `../hw1/feedback/Detailed_Feedback_Report.pdf` — **read it before drafting the PRD.** Transferable lessons (still apply):
  - Project planning docs were called out as weak — make `docs/PRD.md` / `docs/PLAN.md` rigorous
  - Config & security portability — the grader should be able to clone, `uv sync`, and run on a different machine with zero hand-holding
  - Extensibility / plugin architecture — must be visible even if not currently used
  - Quality standards automation — pre-commit + CI, not just "ruff was run"
- **HW2 patterns proven to work** (use as templates): SDK layer + Gatekeeper + Watchdog + structured logging + per-mechanism PRDs + ADRs + class diagram + comprehensive README with embedded artifacts.

## The mandatory workflow (Vibe Coding Lifecycle)
Dr. Segal walked through this live in Lecture 1 (~lines 1140–1500). Quotes are verbatim from the transcript (Hebrew → English).

```
Idea → PRD → Plan → TODO → Verify → Execute → README → Run → Push to GitHub
```

The full canonical sequence — **use these prompt phrases verbatim** so Claude recognizes them as the standard lifecycle:

1. **Read context first**: `IDEA.md` → `RULES.md` → `CONTEXT-lec06-pdfs.md` → `CONTEXT-lecture-06.md` (when ready) → `../hw1/feedback/Detailed_Feedback_Report.pdf` → `../hw2/README.md` (good HW2 patterns) → `../hw2/docs/PLAN.md` (architecture template).
2. **Collect user-specific info** (see below).
3. **Enter Plan Mode**: type `/plan` or write *"insert into plan mode"*.
4. **PRD** (`docs/PRD.md`): the master prompt is verbatim *"your mission is to create the following PRD document based on the following description"* followed by bullets distilled from `IDEA.md`. **⚠️ STOP HERE AND GET USER APPROVAL** — rubric §2.5 makes this an explicit gate.
5. **Plan** (`docs/PLAN.md`): architecture and technical plan — C4 model, UML sequence diagram for the CrewAI agent task flow, **class diagram (mandatory per rubric)**, ADRs (CrewAI vs LangGraph choice, LuaLaTeX vs XeLaTeX choice, Markdown→LaTeX pipeline, etc.), ISO/IEC 25010 paragraph.
6. **TODO** (`docs/TODO.md`): Dr. Segal's verbatim quote (Lec 1 line 1170): *"מינימום 500 משימות, בדרך כלל 1000 משימות, 900, 800"* — **MIN 500 tasks, typically 800–1000**.
7. **Per-mechanism PRDs**: `docs/PRD_crew_orchestrator.md`, `docs/PRD_researcher_agent.md`, `docs/PRD_writer_agent.md`, `docs/PRD_editor_agent.md`, `docs/PRD_latex_compiler_agent.md`, `docs/PRD_skill_layer.md`, `docs/PRD_tools.md`, `docs/PRD_gatekeeper.md`, `docs/PRD_bibliography.md` — one per significant component, each with Input/Output/Setup docstring shape (rubric §16.3).
8. **⚠️ APPROVAL GATE #2**: get user approval on the **entire docs package** (PRD + PLAN + TODO + per-mechanism PRDs) before any code is written. Rubric §2.5 step 5 makes this explicit.
9. **Verify**: verbatim prompt: *"you must be very critical: check that every PRD requirement appears in TODO. Add missing tasks."* Dr. Segal said this typically adds ~200 missed tasks.
10. **Execute**: verbatim: *"execute the to do list one by one and mark each that was done or complete"*. This marking is what enables session resumption.
11. **README** (`README.md`): verbatim Lec 1 line 1247: *"you must create a readme file — this is the most important thing"*.
12. **Run**: verbatim: *"run the project"* — verify it works end-to-end before pushing.
13. **Push to GitHub continuously**: verbatim: *"push to github [public]"*. Continuous commits — Dr. Segal grades commit *density* and *progression*, not just count. **One big-bang push at the end is a significant grade reduction.** He only inspects commits on `main` (Lec 4 line 577).

## User-specific info — pre-populated from HW2 (confirm with user, don't re-ask)

| Field | Value | Source |
|---|---|---|
| **Group code** | `uoh-sqak` | Same as HW1 + HW2; semester-long code |
| **Pair status** | **Pair** (Salah + Andalus) | Same as HW1 + HW2 |
| **Student 1 (you)** | Salah Qadah / סלאח קדח / ID **323039974** | HW1+HW2 submissions |
| **Student 2 (partner)** | Andalus Kalash / אנדלוס כלש / ID **211435797** | HW1+HW2 submissions |
| **Repo owner** | `salah-dev-stu` on GitHub | HW1 = `uoh-sqak-ex01`, HW2 = `uoh-sqak-ex02` |
| **Repo URL (suggested)** | `https://github.com/salah-dev-stu/uoh-sqak-ex03` | follows pattern |
| **Self-grade placeholder** | `85` | HW1 self-graded 90, actual 85.54 → calibrate down |
| **Late submission** | `no` (default) | adjust if late |

**Still to ask the user at session start (NOT covered above):**

1. **Article/book topic** — free choice. Any non-trivial subject. Dr. Segal's spec says Hebrew article gets more credit ("Hebrew is harder and more appreciated"). Examples: history of AI in Israel, software engineering principles, agent debate techniques, etc.
2. **LLM provider strategy** — Claude CLI login (default, per HW2) or API key. Different providers per CrewAI agent could be a bonus.
3. **LaTeX compiler** — recommended LuaLaTeX (best Hebrew support); XeLaTeX allowed. Defaults to LuaLaTeX.
4. **Compilation environment** — TeXLive (Linux/Mac default) or MiKTeX (Dr. Segal's recommendation per spec). On the user's macOS, TeXLive likely already installed (the user has it from HW1).
5. **CrewAI installation budget** — CrewAI consumes tokens per agent invocation. Discuss token economy upfront with the user.

A `scripts/fill_submission_pdf.py` script (carried over from HW2 and adapted for ex03) already has Student 1, Student 2, group code, and structure pre-filled. The worker can run `uv run python scripts/fill_submission_pdf.py` at submission time.

## Quality target — READ THIS

**The user's target is ≥92 overall in the course.** HW1 came in at 85.54; HW2 awaits grading. HW3 needs to materially beat HW1 quality. This means:

- **Aim for 90+ on HW3** by genuinely addressing every HW1 weakness, *and* honest self-grade of 85–88
- **TODO must have 800–1000 tasks**, not the 500 minimum
- **Planning docs must be rigorous** — Dr. Segal flagged HW1 planning as weak. Don't repeat that.
- **Architecture diagrams are explicit** — class diagram for OOP layout (mandatory per spec), C4 model in PLAN.md, UML sequence for CrewAI task flow
- **Config portability** — grader on a fresh machine should `git clone && uv sync && make pdf` and have everything work
- **Extensibility shown** — Skill registry, Agent factory, plugin pattern; document the extension points
- **Quality automation** — pre-commit hook running ruff + pytest, CI workflow file, coverage threshold in pyproject.toml
- **README reads like a published product manual** — install, usage, examples, configuration, contribution, license; include the **final PDF embedded** or linked
- **The PDF artifact is the centerpiece**: this is uniquely HW3's evaluation criterion. The spec says *"check is technical, on the envelope and not on content correctness: links connect, citations exist, BiDi correct, tables don't exceed page, formulas are fancy"*

## What HW3 actually is — short version

Build a **CrewAI multi-agent team** that produces a **15-page LaTeX article/book** on a chosen topic. Toolchain: CrewAI + LangChain + LuaLaTeX. Content must include: cover sheet, TOC, ≥1 image, ≥1 Python-generated chart, ≥1 table, ≥1 math formula, BiDi (Hebrew-English) section, linked bibliography. **The PDF is the central artifact graded.**

Full spec is in `IDEA.md`. Strict requirements are in `RULES.md`. Authoritative source-of-truth is `lectures/lecture-06-langchain-crewai.txt` when the orchestrator finishes transcribing (~110 min from now). PDF spec is `materials/hw3-spec-main-L06-summary-and-ex03-definition.pdf`.

## Top 13 hard rules (the grading agent enforces these — see `RULES.md` for full list)

| # | Rule | Audit |
|---|------|-------|
| 1 | All business logic flows through an SDK layer | Code review |
| 2 | OOP, no code duplication (extract via base class / mixin / Template Method). **Submit class diagram.** | Code review + diagram |
| 3 | All external API calls (LLMs, web search, LaTeX compile) go through the Gatekeeper class | Code review + test |
| 4 | Rate limits + token budgets in JSON config, never in code | Config test |
| 5 | Versioning: starts at `1.00`, `+0.01` per change, in code AND config | Version module |
| 6 | TDD: Red → Green → Refactor, tests written before/with code | Work process |
| 7 | **≤ 150 lines per Python file** (no comments/blanks counted) | Automated |
| 8 | `ruff check` returns zero failures (line-length 100, py313, rules E/F/W/I/N/UP/B/C4/SIM, ignore E501) | ruff |
| 9 | `pytest --cov` ≥ **85%** coverage (`fail_under = 85` in pyproject.toml) | pytest |
| 10 | **Zero hardcoded values** in source — everything via config | Code review |
| 11 | Zero secrets in code — `.env-example` + `os.environ.get(...)`, `.env` git-ignored | Auto scan |
| 12 | `uv` is mandatory — pip / `python -m` / `pip install` / venv / virtualenv all FORBIDDEN. Everything via `uv run`, `uv sync`, `uv add`, `uv lock` | Auto |
| 13 | Continuous git commits with meaningful messages — one big push at the end is heavily penalized | Git history audit |

## HW3-specific additions to the rule set (from the spec §13)

| # | Rule | Audit |
|---|------|-------|
| H1 | **15-page PDF target** — Hebrew article gets more credit | Page-count + language check |
| H2 | **Cover sheet** — topic, author, date, course (203.3763), lecturer (Dr. Yoram Segal) | PDF inspection |
| H3 | **Table of contents, chapters, headers/footers** | PDF inspection |
| H4 | **≥1 image** | PDF inspection |
| H5 | **≥1 Python-generated chart** — must be created BY CODE, not pulled from web | PDF + code review |
| H6 | **≥1 table** that fits the page (doesn't overflow) | PDF inspection |
| H7 | **≥1 math formula** rendered as "fancy formula", NOT flat text | PDF inspection |
| H8 | **BiDi section** — at least one chapter demonstrates Hebrew↔English transitions correctly | PDF inspection |
| H9 | **Bibliography with linked citations** — `.bib` file + biber pass; clicking a citation jumps to the reference | PDF link test + repo audit |
| H10 | **LaTeX project committed to GitHub** — `.tex`, `.bib`, figures dir, Makefile or build script | Repo audit |
| H11 | **CrewAI agent team** — at least: Researcher / Writer / Editor / LaTeX-Producer; "real" multi-agent, no faked dialogue | Code + log inspection |
| H12 | **Markdown→LaTeX intermediate workflow recommended** | Code review (not strict) |
| H13 | **LuaLaTeX preferred** (XeLaTeX allowed) for Hebrew support | Build script |
| H14 | **4 compilation passes** for cross-references to settle | Build script |
| H15 | **TikZ for block diagrams** | PDF/source inspection |
| H16 | **Pairs only** — confirmed Salah + Andalus | Submission check |
| H17 | **Each pair member uploads PDF separately** to Moodle id=270973 | Moodle |
| H18 | **Repo accessibility** — public OR shared with `rmisegal@gmail.com`. Inaccessible = automatic rejection, no resubmit | Submission check |
| H19 | **Hebrew or English** dialogue/output, not Arabic | Output inspection |
| H20 | **Skills layer** — each CrewAI agent gets a `Skill` (`SKILL.md` + references + scripts) | Repo audit |

## Required project layout

```
hw3/
├── src/
│   └── <package>/                 ← e.g., agent_article
│       ├── __init__.py            ← MUST define __version__ and __all__
│       ├── sdk/                   ← public single-entry SDK
│       │   ├── __init__.py
│       │   └── sdk.py
│       ├── agents/                ← CrewAI agent definitions
│       │   ├── __init__.py
│       │   ├── researcher_agent.py
│       │   ├── writer_agent.py
│       │   ├── editor_agent.py
│       │   └── latex_agent.py
│       ├── crew/                  ← Crew assembly + Process definition
│       │   ├── __init__.py
│       │   └── article_crew.py
│       ├── tasks/                 ← Task definitions per agent
│       │   ├── __init__.py
│       │   └── article_tasks.py
│       ├── tools/                 ← Tool definitions (web search, file I/O, LaTeX compile)
│       │   ├── __init__.py
│       │   ├── web_search.py
│       │   ├── chart_generator.py    ← Python plotting → PNG
│       │   └── latex_compiler.py
│       ├── skills/                ← Skills layer (file-based expertise injection)
│       │   ├── __init__.py
│       │   ├── researcher_skill/
│       │   │   ├── SKILL.md
│       │   │   └── references/
│       │   ├── writer_skill/
│       │   ├── editor_skill/
│       │   └── latex_skill/
│       ├── shared/                ← cross-cutting concerns
│       │   ├── __init__.py
│       │   ├── gatekeeper.py      ← API gatekeeper
│       │   ├── config.py
│       │   ├── logging_fifo.py
│       │   └── version.py
│       ├── menu/                  ← terminal menu
│       │   └── tui.py
│       ├── constants.py
│       └── main.py
├── latex/                         ← THE LaTeX project (graded!)
│   ├── main.tex
│   ├── chapters/                  ← chapter-by-chapter Markdown source + .tex output
│   ├── figures/                   ← image assets + Python-generated charts
│   ├── bib/
│   │   └── references.bib
│   ├── style/
│   │   └── article.cls            ← optional custom class
│   ├── Makefile                   ← lualatex + biber + 4 passes
│   └── output/
│       └── <group-code>-article.pdf   ← THE deliverable
├── tests/
│   ├── unit/
│   ├── integration/               ← end-to-end Crew runs with mock LLM
│   └── conftest.py
├── docs/
│   ├── PRD.md
│   ├── PLAN.md
│   ├── TODO.md                    ← ≥500 tasks
│   ├── PRD_crew_orchestrator.md   ← per-mechanism PRDs
│   ├── PRD_researcher_agent.md
│   ├── PRD_writer_agent.md
│   ├── PRD_editor_agent.md
│   ├── PRD_latex_agent.md
│   ├── PRD_skill_layer.md
│   ├── PRD_tools.md
│   ├── PRD_gatekeeper.md
│   ├── PRD_bibliography.md
│   ├── PRD_chart_generator.md
│   ├── PROMPTS.md
│   ├── ADRs/
│   ├── diagrams/                  ← C4 / UML / class diagram (mandatory)
│   └── ...
├── config/
│   ├── setup.json
│   ├── agents.json                ← per-agent: role, goal, backstory, LLM, skill ref
│   ├── tasks.json                 ← task templates
│   ├── rate_limits.json
│   └── logging_config.json
├── results/
├── assets/                        ← screenshots, architecture diagrams
├── README.md                      ← MANDATORY (full user manual + sample-PDF embed + architecture)
├── pyproject.toml                 ← uv config + ruff + pytest + coverage
├── uv.lock                        ← MUST exist and be tracked
├── .env-example
├── .env                           ← git-ignored
└── .gitignore                     ← + latex/output/*.aux, *.log, *.toc, *.bbl, *.blg
```

## Submission process (last steps)
1. Final code + LaTeX project + README + sample-PDF committed and pushed to GitHub (public OR shared with `rmisegal@gmail.com`).
2. Open the submission template `uoh-rl07-ex03-template.docx` (already in this dir). **Do not change the field structure.** Fill in:
   - Submitting an exercise number: **03**
   - Group ID code: **`uoh-sqak`**
   - Recommendation for self-scoring: **85** placeholder; orchestrator calibrates after audit
   - Student 1: Salah Qadah / ID 323039974 / סלאח קדח
   - Student 2: Andalus Kalash / ID 211435797 / אנדלוס כלש
   - Link to GitHub: `https://github.com/salah-dev-stu/uoh-sqak-ex03`
   - Late: no
3. Save as PDF named `uoh-sqak-ex03.pdf`.
4. Upload to Moodle assignment `id=270973`.
5. **Each pair member submits separately** — submission timestamp is per-individual.

A `scripts/fill_submission_pdf.py` is already adapted for ex03. Run `uv run python scripts/fill_submission_pdf.py` at submission time.

## Gotchas / Dr. Segal's pet peeves

- **The PDF is the centerpiece.** All other audit gates matter, but the PDF must look professional. *"Check is on the envelope, not on content correctness"* — links, citations, BiDi, formulas, tables.
- **Hebrew article = more credit.** Spec explicitly says *"עברית קשה יותר ולכן מוערכת יותר"* — "Hebrew is harder and therefore more appreciated."
- **Don't dump the rubric PDF into your context.** It's Hebrew, ~30k tokens. Use `RULES.md` instead, and only Read specific pages of the PDF if you need a verbatim quote.
- **TODO.md must be exhaustive.** 500 tasks is the floor. Dr. Segal said anything less means you're skipping things. Aim for 800.
- **Continuous commits.** Push after each completed major task. The grader looks at history density. **HW2 lesson: keep this up.**
- **`uv run` for everything.** Even pytest: `uv run pytest`. Even running the script: `uv run python -m agent_article.main`.
- **150 lines is strict.** When a file gets long, split.
- **Compile 4 times** when there's `.bib`. The Makefile must do this automatically.
- **TikZ vs matplotlib**: TikZ for block diagrams (architecture), matplotlib for data charts. Spec specifies Python-generated chart, so matplotlib/seaborn is needed.
- **"fancy formula" not "plain text"**: pass the right hint to the LaTeX-producing agent.
- **CrewAI agent prompts**: each agent has `role`, `goal`, `backstory`. These are not optional — they shape the agent's behavior. Backstory = "you are a senior researcher with 10 years experience..."

## Tools the lecturer expects
- **Claude CLI** (you are this) — Login auth preferred
- `uv` — package manager (mandatory)
- `ruff` — linter
- `pytest` + `pytest-cov`
- `git` + GitHub
- **CrewAI** — pip via `uv add crewai`
- **LangChain** — pip via `uv add langchain langchain-anthropic` (or langchain-openai etc.)
- **MiKTeX or TeXLive** — for LuaLaTeX + biber + bibtex
- **matplotlib** or **plotly** — for the Python-generated chart
- The user is on macOS, plain terminal, TeXLive already installed (HW1 had it).

## How the grader will run this project — 4 paths (from HW2 README pattern)

After cloning + `uv sync`:

**A — Already logged into Claude CLI (the lecturer's preferred mode):**
Nothing to do. Skip to test/build step.

**B — Not logged in, but has a Claude subscription:**
```bash
claude --login   # opens a browser; finish the consent flow once per machine
```

**C — Has an Anthropic API key:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...   # CrewAI / LangChain providers pick this up
```

**D — Automated grader / no Claude access at all:**
Run tests instead: `uv run pytest tests/unit tests/integration --cov=src` — full crew + LaTeX pipeline exercised with mock LLM.

For LaTeX compilation:
```bash
cd latex && make
# Or: lualatex main.tex && biber main && lualatex main.tex && lualatex main.tex
```

## Lecturer contact (use sparingly, only if truly stuck)
- **Email**: `rmisegal@gmail.com`
- **Office hours**: Mondays 20:00–21:00 via Zoom
- **AI ethics policy**: include the verbatim Hebrew + English paragraph in `README.md` "AI Usage Disclosure" section. Reference `docs/PROMPTS.md` as the audit trail.

## Reporting back
This worker session has no direct channel to the orchestrator. When you finish a major milestone (PRD done, Plan done, code complete, PDF generated, repo pushed), surface a clear summary so the user can copy-paste it back to the orchestrator.

## First action — required reading order

Before asking the user anything or drafting any document, read these files in this exact order:

1. **`IDEA.md`** (this dir) — what HW3 is, distilled from the spec PDF
2. **`RULES.md`** (this dir) — the grading rubric + HW3-specific audit gates
3. **`CONTEXT-lec06-pdfs.md`** (this dir) — deep digest of CrewAI Parts A+B, LangChain, Architecture-2026, and the spec PDF itself
4. **`CONTEXT-lecture-06.md`** (this dir, when whisper finishes) — verbatim quotes from Dr. Segal's lecture
5. **`../hw1/feedback/Detailed_Feedback_Report.pdf`** — the lecturer's HW1 feedback. **Your checklist of what to fix.**
6. **`../hw2/README.md`** — manual-grade README pattern that worked
7. **`../hw2/docs/PLAN.md`** + **`../hw2/docs/AUDIT.md`** — architecture patterns that worked

Then:
8. Ask the user for the 5 placeholder fields above (article topic, LLM provider strategy, LaTeX compiler, compilation env, token budget).
9. Acknowledge constraints; surface any clarifying questions.
10. **Enter Plan Mode** (`/plan`) and begin the Vibe Coding lifecycle.

**Do not start writing code until PRD + PLAN + TODO + per-mechanism PRDs are approved by the user — this is two explicit approval gates per rubric §2.5.**
