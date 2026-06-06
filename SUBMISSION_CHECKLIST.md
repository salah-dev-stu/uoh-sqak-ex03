# Submission Checklist — HW3

**Deadline:** Friday, 12 June 2026, 23:59 (Asia/Jerusalem) — Moodle assignment id=270973.
**Late penalty:** −5 pts / 24h.

**Pair:** Salah Qadah (323039974) + Andalus Kalash (211435797). Group code: `uoh-sqak`.
Each pair member uploads the same PDF separately on Moodle.

Tick every box before uploading the PDF.

## Documentation
- [ ] `README.md` at repo root, ≥200 lines, manual-grade
- [ ] README links to the sample PDF (`latex/output/uoh-sqak-article.pdf`)
- [ ] README includes cost analysis table for one full article generation
- [ ] README includes AI Usage Disclosure (verbatim Hebrew + English)
- [ ] README has dedicated "HW1 Extensibility remediation" section
- [ ] `docs/PRD.md` exists (approved, gate 1 cleared in git history)
- [ ] `docs/PLAN.md` exists with class diagram + C4 + UML + ≥7 ADRs + ISO/IEC 25010
- [ ] `docs/TODO.md` ≥500 tasks, target 800
- [ ] `docs/PROMPTS.md` ≥25 entries with 5-field template
- [ ] ≥10 per-mechanism PRDs in `docs/PRD_*.md`
- [ ] `docs/AUDIT.md` final-audit report
- [ ] `LICENSE` (MIT)

## Code quality (automated gates)
- [ ] `uv run ruff check src tests scripts` → 0 errors
- [ ] `uv run pytest tests/unit tests/integration --cov` → coverage ≥85%
- [ ] `uv run python scripts/check_file_lines.py` → 0 violations
- [ ] Grep for `sk-*` or `api_key=*` secrets → 0 leaks
- [ ] All `.py` files ≤150 logical lines

## Engineering process
- [ ] ≥50 commits on `main` with meaningful messages (conventional commit style)
- [ ] No `pip install` / `python -m` / `venv` references in code or docs
- [ ] All commands documented through `uv run`
- [ ] Pre-commit hook installed + working (ruff + line + pytest)
- [ ] CI workflow at `.github/workflows/ci.yml`

## CrewAI architecture (H16, H17)
- [ ] ≥4 agents defined: Researcher, Writer, Editor, LaTeX-Producer
- [ ] Each agent has `role`, `goal`, `backstory` in `config/agents.json`
- [ ] Each agent has a `src/<pkg>/skills/<role>_skill/SKILL.md`
- [ ] Tasks defined in `config/tasks.json` per agent
- [ ] Crew assembled with explicit Process (sequential or hierarchical)
- [ ] Real LLM calls flow through Gatekeeper

## LaTeX deliverable (H1-H15)
- [ ] `latex/main.tex` exists and compiles cleanly
- [ ] `latex/Makefile` runs `lualatex → biber → lualatex → lualatex` (≥4 passes)
- [ ] Cover sheet: topic, author(s), date, course 203.3763, lecturer Dr. Yoram Segal
- [ ] Table of contents populated
- [ ] ≥4 chapters with named headings
- [ ] Headers/footers (fancyhdr)
- [ ] ≥1 image in `latex/figures/`
- [ ] ≥1 Python-generated chart (script in `src/`, PNG committed)
- [ ] ≥1 table that fits the page (no overflow)
- [ ] ≥1 math formula rendered as "fancy" (amsmath/mathtools)
- [ ] ≥1 BiDi chapter (Hebrew↔English transitions)
- [ ] Bibliography in `.bib`, citations clickable in PDF
- [ ] ≥1 TikZ block diagram
- [ ] Page count: 14-17
- [ ] Hebrew used substantially (for spec bonus)
- [ ] Output `latex/output/uoh-sqak-article.pdf` committed

## Configuration (R6 versioning)
- [ ] `config/setup.json` — version "1.00"
- [ ] `config/agents.json` — version "1.00"
- [ ] `config/tasks.json` — version "1.00"
- [ ] `config/crew.json` — version "1.00"
- [ ] `config/rate_limits.json` — version "1.00"
- [ ] `config/logging_config.json` — version "1.00", fifo_files=20, max_lines_per_file=500
- [ ] `config/latex.json` — version "1.00"

## Security
- [ ] `.env-example` committed; `.env` git-ignored
- [ ] No API keys, passwords, tokens in source code
- [ ] `.gitignore` includes `.env`, `*.key`, `*.pem`, `credentials.json`
- [ ] `.gitignore` includes LaTeX intermediates: `*.aux`, `*.log`, `*.toc`, `*.bbl`, `*.blg`, `*.synctex.gz`, `*.fls`, `*.fdb_latexmk`, `*.out`

## GitHub (H22) — user action
- [ ] Repo PUBLIC at `https://github.com/salah-dev-stu/uoh-sqak-ex03`
- [ ] Verified accessible in incognito window (no login required)
- [ ] All commits pushed to `main`
- [ ] Andalus added as collaborator OR repo is public (public is sufficient)

## Submission PDF — user action
- [ ] `uv run python scripts/fill_submission_pdf.py` generates `uoh-sqak-ex03.pdf`
- [ ] PDF has exercise=03, group=uoh-sqak, self-grade=85
- [ ] Student 1: Salah Qadah (323039974) — English + Hebrew names
- [ ] Student 2: Andalus Kalash (211435797) — English + Hebrew names
- [ ] Repo URL in the PDF matches the public GitHub URL
- [ ] Late submission field correct (no, unless past deadline)

## Moodle upload (H21) — user action
- [ ] Salah uploads `uoh-sqak-ex03.pdf` to Moodle assignment id=270973
- [ ] Andalus uploads same PDF separately to her Moodle
- [ ] Both confirmations captured

## Final smoke test — recommended
- [ ] Fresh clone in a new directory: `git clone <repo>`
- [ ] `uv sync` succeeds without errors
- [ ] `uv run pytest tests/unit` passes
- [ ] `make -C latex` produces a PDF
- [ ] PDF opens, citation links work, BiDi looks right

---
Generated: 2026-06-06
