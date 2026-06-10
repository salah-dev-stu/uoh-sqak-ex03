# TODO — HW3 Article Generation Pipeline

**Total tasks: 724**
**Minimum: 500 | Target: 650 | Floor (rubric): 500**

Legend: `[ ]` = pending · `[x]` = done · `[-]` = skipped/N/A

---

## Phase 1: Repository & Scaffolding (T-001 – T-060)

### 1.1 GitHub Repository
- [x] T-001: Create public GitHub repo `salah-dev-stu/uoh-sqak-ex03`
- [x] T-002: Run `git init` in `hw3/` directory
- [x] T-003: Add remote origin `https://github.com/salah-dev-stu/uoh-sqak-ex03.git`
- [x] T-004: Create initial `.gitignore` with `.env`, `__pycache__/`, `*.pyc`, `workspace/`, `latex/output/`, `*.aux`, `*.log`, `*.toc`, `*.bbl`, `*.blg`
- [x] T-005: Create `.env-example` with `ANTHROPIC_API_KEY=sk-ant-your-key-here`
- [x] T-006: Add `LUALATEX_PATH=lualatex` to `.env-example`
- [x] T-007: Add `BIBER_PATH=biber` to `.env-example`
- [x] T-008: Verify `.env` is NOT committed (grep .gitignore)
- [x] T-009: Push initial scaffold commit to GitHub
- [x] T-010: Verify repo is publicly accessible (open in incognito browser)

### 1.2 uv Project Setup
- [x] T-011: Create `pyproject.toml` with `[project]` metadata
- [x] T-012: Set `name = "agent-article"` in pyproject.toml
- [x] T-013: Set `version = "1.00"` in pyproject.toml
- [x] T-014: Set `requires-python = ">=3.13"` in pyproject.toml
- [x] T-015: Add `crewai>=0.80.0` to dependencies
- [x] T-016: Add `langchain-anthropic>=0.3.0` to dependencies
- [x] T-017: Add `duckduckgo-search>=7.0.0` to dependencies
- [x] T-018: Add `python-dotenv>=1.0.0` to dependencies
- [x] T-019: Add `matplotlib>=3.9.0` to dependencies
- [x] T-020: Add `rich>=13.0.0` to dependencies
- [x] T-021: Add dev dependency `pytest>=8.0.0`
- [x] T-022: Add dev dependency `pytest-cov>=5.0.0`
- [x] T-023: Add dev dependency `ruff>=0.4.0`
- [x] T-024: Add dev dependency `pre-commit>=3.7.0`
- [x] T-025: Add `[project.scripts]` entry: `agent-article = "agent_article.main:main"`
- [x] T-026: Configure `[tool.ruff]` with `line-length = 100`, `target-version = "py313"`
- [x] T-027: Configure `[tool.ruff.lint]` with `select = ["E","F","W","I","N","UP","B","C4","SIM"]`
- [x] T-028: Add `ignore = ["E501"]` to ruff config
- [x] T-029: Configure `[tool.pytest.ini_options]` with `testpaths = ["tests"]`
- [x] T-030: Add `addopts = "--cov=src --cov-report=term-missing"` to pytest config
- [x] T-031: Configure `[tool.coverage.report]` with `fail_under = 85`
- [x] T-032: Configure `[build-system]` with hatchling
- [x] T-033: Run `uv sync --dev` to install all dependencies
- [x] T-034: Verify `uv.lock` is created
- [x] T-035: Commit `pyproject.toml` and `uv.lock`

### 1.3 Directory Structure
- [x] T-036: Create `src/agent_article/` package directory
- [x] T-037: Create `src/agent_article/__init__.py` with `__version__ = "1.00"` and `__all__ = ["ArticleSDK"]`
- [x] T-038: Create `src/agent_article/sdk/` directory with `__init__.py`
- [x] T-039: Create `src/agent_article/agents/` directory with `__init__.py`
- [x] T-040: Create `src/agent_article/tasks/` directory with `__init__.py`
- [x] T-041: Create `src/agent_article/crew/` directory with `__init__.py`
- [x] T-042: Create `src/agent_article/tools/` directory with `__init__.py`
- [x] T-043: Create `src/agent_article/skills/` directory with `__init__.py`
- [x] T-044: Create `src/agent_article/shared/` directory with `__init__.py`
- [x] T-045: Create `src/agent_article/menu/` directory with `__init__.py`
- [x] T-046: Create `tests/unit/` directory with `__init__.py`
- [x] T-047: Create `tests/integration/` directory with `__init__.py`
- [x] T-048: Create `tests/conftest.py` placeholder
- [x] T-049: Create `docs/ADRs/` directory
- [x] T-050: Create `docs/diagrams/` directory
- [x] T-051: Create `config/` directory
- [x] T-052: Create `workspace/` directory with `.gitkeep` (git-ignored content)
- [x] T-053: Create `results/` directory with `.gitkeep`
- [x] T-054: Create `assets/` directory with `.gitkeep`
- [x] T-055: Create `scripts/` directory
- [x] T-056: Create `latex/chapters/` directory
- [x] T-057: Create `latex/figures/` directory
- [x] T-058: Create `latex/bib/` directory
- [x] T-059: Create `latex/style/` directory
- [x] T-060: Create `latex/output/` directory (git-ignored)

---

## Phase 2: Quality Automation (T-061 – T-090)

### 2.1 Line Count Script
- [x] T-061: Create `scripts/check_file_lines.py`
- [x] T-062: Implement `count_logical_lines(path)` — skip blank lines and comment-only lines
- [x] T-063: Implement `main()` — scan `src/`, `tests/`, `scripts/` for .py files
- [x] T-064: Print violation list and return exit code 1 if any file > 150 lines
- [x] T-065: Print "OK" and return exit code 0 if all files pass
- [x] T-066: Test: create a 151-line test file and verify script catches it
- [x] T-067: Commit `scripts/check_file_lines.py`

### 2.2 Pre-Commit Hooks
- [x] T-068: Create `.pre-commit-config.yaml`
- [x] T-069: Add `ruff` hook from `astral-sh/ruff-pre-commit` rev v0.4.0
- [x] T-070: Add `check-file-lines` local hook pointing to `scripts/check_file_lines.py`
- [x] T-071: Run `uv run pre-commit install` to wire up hooks
- [x] T-072: Run `uv run pre-commit run --all-files` to verify hooks pass on current state
- [x] T-073: Commit `.pre-commit-config.yaml`

### 2.3 GitHub Actions CI
- [x] T-074: Create `.github/workflows/ci.yml`
- [x] T-075: Add trigger on `push` and `pull_request`
- [x] T-076: Add `ubuntu-latest` runner with Python 3.13
- [x] T-077: Add `astral-sh/setup-uv` step
- [x] T-078: Add `uv sync --dev` step
- [x] T-079: Add `uv run ruff check src tests scripts` step
- [x] T-080: Add `uv run python scripts/check_file_lines.py` step
- [x] T-081: Add `uv run pytest tests/unit tests/integration --cov=src --cov-fail-under=85` step
- [x] T-082: Add TeX Live installation step for integration tests (`sudo apt-get install texlive-full`)
- [x] T-083: Commit `.github/workflows/ci.yml`
- [x] T-084: Push to GitHub and verify CI runs green
- [x] T-085: Fix any CI failures before proceeding

### 2.4 Project-Level Makefile
- [x] T-086: Create top-level `Makefile` with targets: `install`, `test`, `lint`, `clean`, `pdf`
- [x] T-087: `make install` → `uv sync --dev`
- [x] T-088: `make test` → `uv run pytest tests/unit tests/integration --cov=src`
- [x] T-089: `make lint` → `uv run ruff check src tests scripts`
- [x] T-090: `make pdf` → `cd latex && make`

---

## Phase 3: Configuration Files (T-091 – T-130)

### 3.1 Config Files
- [x] T-091: Create `config/setup.json` with version, package name, workspace_dir, results_dir, latex_dir, output_filename
- [x] T-092: Set `"version": "1.00"` in setup.json
- [x] T-093: Set `"workspace_dir": "workspace"` in setup.json
- [x] T-094: Set `"output_filename": "uoh-sqak-article.pdf"` in setup.json
- [x] T-095: Create `config/agents.json` with version and agents dict
- [x] T-096: Add `researcher` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [x] T-097: Add `writer` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [x] T-098: Add `editor` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [x] T-099: Add `latex_producer` agent entry — goal MUST include "fancy formula, not plain text"
- [x] T-100: Verify `latex_producer` backstory mentions "fancy formula, not plain text"
- [x] T-101: Create `config/tasks.json` with version and tasks dict
- [x] T-102: Add `research` task: description template with `{topic}` placeholder, expected_output
- [x] T-103: Add `write` task: description referencing research_notes.md, 6-chapter structure
- [x] T-104: Add `edit` task: description referencing workspace/chapters/
- [x] T-105: Add `latex` task: description including "fancy formula, not plain text" verbatim
- [x] T-106: Verify all task descriptions use `{topic}` placeholder (not hardcoded topic)
- [x] T-107: Create `config/crew.json` with process, verbose, agent list, task list
- [x] T-108: Create `config/rate_limits.json` with services: claude_cli, duckduckgo, lualatex
- [x] T-109: Set `requests_per_minute: 10` for claude_cli
- [x] T-110: Set `tokens_per_article: 200000` for claude_cli
- [x] T-111: Set `hard_cap_percent: 95` for claude_cli
- [x] T-112: Create `config/logging_config.json` with fifo_files: 20, max_lines_per_file: 500
- [x] T-113: Create `config/latex.json` with compiler, biber, passes, chapter_list, output_dir
- [x] T-114: Set `"passes": 4` in latex.json
- [x] T-115: Set `"compiler": "lualatex"` in latex.json
- [x] T-116: Set `"bib_style": "numeric-comp"` in latex.json
- [x] T-117: Add 6 chapter names to `chapter_list` in latex.json
- [x] T-118: Verify all config files have `"version": "1.00"` field
- [x] T-119: Verify NO Python source file hardcodes any value from config
- [x] T-120: Commit all config files

### 3.2 Config Loader
- [x] T-121: Write failing test: `test_get_config_loads_setup` (tmp_path with fake setup.json)
- [x] T-122: Run test — expect `ModuleNotFoundError`
- [x] T-123: Create `src/agent_article/shared/config.py`
- [x] T-124: Implement `_CONFIG_DIR` pointing to `config/` relative to package root
- [x] T-125: Implement `_cache: dict[str, Any] = {}` module-level cache
- [x] T-126: Implement `get_config(name: str) → dict` with cache-first logic
- [x] T-127: Implement `cfg(name, key, default=None)` single-key accessor
- [x] T-128: Implement `reload()` to clear cache (for tests)
- [x] T-129: Run test — expect PASS
- [x] T-130: Commit `shared/config.py` and test

---

## Phase 4: Shared Infrastructure (T-131 – T-200)

### 4.1 Version Module
- [x] T-131: Write failing test: `test_version_format` — VERSION has 2 dot-separated parts
- [x] T-132: Write failing test: `test_bump` — "1.00" → "1.01", "1.09" → "1.10"
- [x] T-133: Run tests — expect FAIL
- [x] T-134: Create `src/agent_article/shared/version.py`
- [x] T-135: Implement `VERSION = "1.00"`
- [x] T-136: Implement `bump(version: str) → str` — increments patch component
- [x] T-137: Run tests — expect PASS
- [x] T-138: Commit `shared/version.py` and tests

### 4.2 Constants
- [x] T-139: Create `src/agent_article/constants.py`
- [x] T-140: Implement `AgentRole(StrEnum)` with RESEARCHER, WRITER, EDITOR, LATEX_PRODUCER
- [x] T-141: Implement `ServiceName(StrEnum)` with CLAUDE_CLI, DUCKDUCKGO, LUALATEX
- [x] T-142: Implement `ProcessType(StrEnum)` with SEQUENTIAL, HIERARCHICAL
- [x] T-143: Write test: `test_agent_role_values` — verify string values match config keys
- [x] T-144: Run test — expect PASS
- [x] T-145: Commit `constants.py` and test

### 4.3 Structured Logger (FIFO)
- [x] T-146: Create `src/agent_article/shared/logging_fifo.py`
- [x] T-147: Implement `StructuredLogger.__init__(component: str)` — reads logging_config.json
- [x] T-148: Implement `_open_next()` — opens next numbered JSONL file in log_dir
- [x] T-149: Implement `_rotate_if_needed()` — deletes oldest file when max_files reached
- [x] T-150: Implement `_write(level, message, **fields)` — writes JSON line, thread-safe with lock
- [x] T-151: Implement `info(message, **fields)` calling `_write("INFO", ...)`
- [x] T-152: Implement `error(message, **fields)` calling `_write("ERROR", ...)`
- [x] T-153: Implement `warning(message, **fields)` calling `_write("WARNING", ...)`
- [x] T-154: Implement rotation on `_current_lines >= max_lines_per_file`
- [x] T-155: Write test: verify log file is created in log_dir
- [x] T-156: Write test: verify JSON structure (ts, level, component, message)
- [x] T-157: Write test: verify rotation deletes oldest file when max_files exceeded
- [x] T-158: Run tests — expect PASS
- [x] T-159: Commit `shared/logging_fifo.py` and tests

### 4.4 API Gatekeeper
- [x] T-160: Write failing test: `test_call_succeeds` — gatekeeper passes fn() result through
- [x] T-161: Write failing test: `test_rate_limit_enforced` — 3rd call raises GatekeeperError
- [x] T-162: Write failing test: `test_singleton` — `instance()` returns same object
- [x] T-163: Write failing test: `test_budget_cap_raises` — raises at 95% of tokens_per_article
- [x] T-164: Run tests — expect FAIL
- [x] T-165: Create `src/agent_article/shared/gatekeeper.py`
- [x] T-166: Implement `GatekeeperError(Exception)` custom exception class
- [x] T-167: Implement `UsageRecord` dataclass with tokens_in, tokens_out, calls
- [x] T-168: Implement `ApiGatekeeper._instance = None` class variable
- [x] T-169: Implement `ApiGatekeeper.__init__()` — reads rate_limits.json, initializes deques
- [x] T-170: Implement `instance()` classmethod — creates or returns singleton
- [x] T-171: Implement `call(service, fn, *args, **kwargs)` — enforce limits then call fn
- [x] T-172: Implement `_enforce_rate_limit(service)` — sliding window using time.monotonic()
- [x] T-173: Implement `_check_budget(service)` — compares usage to hard_cap_percent
- [x] T-174: Implement `get_spend_report()` — returns copy of _usage dict
- [x] T-175: Add `threading.Lock()` for thread-safety in `_write` operations
- [x] T-176: Run tests — expect PASS
- [x] T-177: Verify all tests pass: `uv run pytest tests/unit/test_gatekeeper.py -v`
- [x] T-178: Commit `shared/gatekeeper.py` and tests

---

## Phase 5: Tools (T-201 – T-280)

### 5.1 BaseTool
- [x] T-201: Create `src/agent_article/tools/base_tool.py`
- [x] T-202: Implement `BaseTool(ABC)` abstract base class
- [x] T-203: Implement `name` abstract property → str
- [x] T-204: Implement `description` abstract property → str
- [x] T-205: Implement `run(*args, **kwargs) → Any` abstract method
- [x] T-206: Implement `as_crewai_tool()` — wraps self using `@tool` decorator
- [x] T-207: Write test: verify `BaseTool` is abstract (cannot instantiate directly)
- [x] T-208: Run test — expect PASS

### 5.2 File Read/Write Tools
- [x] T-209: Write failing test: `test_file_write_and_read` — write then read same file
- [x] T-210: Write failing test: `test_file_write_creates_parent_dirs` — nested path
- [x] T-211: Write failing test: `test_file_read_missing_raises` — FileNotFoundError
- [x] T-212: Run tests — expect FAIL
- [x] T-213: Create `src/agent_article/tools/file_rw.py`
- [x] T-214: Implement `FileWriteTool(BaseTool)` with `base_dir` from config
- [x] T-215: Implement `FileWriteTool.run(relative_path, content)` — creates parent dirs, writes UTF-8
- [x] T-216: Implement `FileReadTool(BaseTool)` with `base_dir` from config
- [x] T-217: Implement `FileReadTool.run(relative_path)` — raises FileNotFoundError if missing
- [x] T-218: Run tests — expect PASS
- [x] T-219: Commit `tools/file_rw.py` and tests

### 5.3 Web Search Tool
- [x] T-220: Write failing test: `test_web_search_returns_string` — mock DDGS, verify format
- [x] T-221: Write failing test: `test_web_search_no_results` — mock empty results, returns "No results"
- [x] T-222: Run tests — expect FAIL
- [x] T-223: Create `src/agent_article/tools/web_search.py`
- [x] T-224: Implement `WebSearchTool(BaseTool)` using `duckduckgo_search.DDGS`
- [x] T-225: Route search through `ApiGatekeeper.instance().call("duckduckgo", ...)`
- [x] T-226: Format results as markdown: title, body, URL, separated by `---`
- [x] T-227: Handle empty results with informative message
- [x] T-228: Run tests — expect PASS
- [x] T-229: Commit `tools/web_search.py` and tests

### 5.4 Chart Generator Tool
- [x] T-230: Write failing test: `test_chart_creates_png` — bar chart, verify file exists
- [x] T-231: Write failing test: `test_chart_nonzero_size` — file size > 0 bytes
- [x] T-232: Write failing test: `test_chart_line_type` — line chart type
- [x] T-233: Write failing test: `test_chart_creates_parent_dir` — creates output dir if needed
- [x] T-234: Run tests — expect FAIL
- [x] T-235: Create `src/agent_article/tools/chart_generator.py`
- [x] T-236: Implement `ChartGeneratorTool(BaseTool)` with `output_dir` from config
- [x] T-237: Use `matplotlib.use("Agg")` backend (no display required)
- [x] T-238: Implement `run(chart_type, title, labels, values, ylabel, filename)` method
- [x] T-239: Support chart types: bar, line, pie
- [x] T-240: Save to `output_dir/filename` at 150 DPI
- [x] T-241: Create output_dir if it doesn't exist
- [x] T-242: Call `plt.close(fig)` to free memory
- [x] T-243: Run tests — expect PASS
- [x] T-244: Commit `tools/chart_generator.py` and tests

### 5.5 LaTeX Compile Tool
- [x] T-245: Write failing test: `test_latex_compile_calls_4_subprocesses` — mock subprocess.run
- [x] T-246: Write failing test: `test_latex_compile_order` — lualatex, biber, lualatex, lualatex
- [x] T-247: Write failing test: `test_latex_compile_raises_on_nonzero_returncode`
- [x] T-248: Write failing test: `test_check_log_warns_on_overfull_hbox`
- [x] T-249: Run tests — expect FAIL
- [x] T-250: Create `src/agent_article/tools/latex_compile.py`
- [x] T-251: Implement `LaTeXCompileTool(BaseTool)` reading compiler/biber paths from config
- [x] T-252: Implement `run(main_tex="main.tex")` — 4-pass compile sequence
- [x] T-253: Pass `--interaction=nonstopmode` to lualatex
- [x] T-254: Implement `_run_cmd(cmd)` — subprocess.run with capture_output, timeout=120
- [x] T-255: Raise RuntimeError if returncode != 0 with stderr excerpt
- [x] T-256: Implement `_check_log(stem)` — warn on "Rerun" and "Overfull \hbox"
- [x] T-257: Route subprocess calls through `ApiGatekeeper.instance().call("lualatex", ...)`
- [x] T-258: Run tests — expect PASS
- [x] T-259: Commit `tools/latex_compile.py` and tests

---

## Phase 6: Skills Layer (T-281 – T-340)

### 6.1 Base Skill
- [x] T-281: Write failing test: `test_file_skill_loads_content` — SKILL.md in tmp_path
- [x] T-282: Write failing test: `test_file_skill_strips_yaml_frontmatter`
- [x] T-283: Write failing test: `test_file_skill_missing_raises_file_not_found`
- [x] T-284: Run tests — expect FAIL
- [x] T-285: Create `src/agent_article/skills/base_skill.py`
- [x] T-286: Implement `BaseSkill(ABC)` with `content` abstract property
- [x] T-287: Implement `FileSkill(BaseSkill)` that reads SKILL.md from `skills/<ref>/SKILL.md`
- [x] T-288: Strip YAML frontmatter (lines between `---` markers)
- [x] T-289: Raise `FileNotFoundError` if SKILL.md doesn't exist
- [x] T-290: Run tests — expect PASS
- [x] T-291: Commit `skills/base_skill.py` and tests

### 6.2 Researcher Skill
- [x] T-292: Create `src/agent_article/skills/researcher_skill/SKILL.md`
- [x] T-293: Add YAML frontmatter: `name: researcher`, `description: Senior research analyst`
- [x] T-294: Document research protocol: broad survey → 3-5 sources → extract claims → structure output
- [x] T-295: Document citation format: `[AuthorYear]` inline, full ref at end
- [x] T-296: Document quality checklist: ≥8 citations, 1500 words, clear headings
- [x] T-297: Create `src/agent_article/skills/researcher_skill/references/` directory with citation style guide

### 6.3 Writer Skill
- [x] T-298: Create `src/agent_article/skills/writer_skill/SKILL.md`
- [x] T-299: Document writing protocol: read all notes → write chapter-by-chapter
- [x] T-300: Document ch05 requirement: ≥2 Hebrew paragraphs mixed with English
- [x] T-301: Document style guide: active voice, short sentences, no "utilize"/"leverage"
- [x] T-302: Document chapter structure: headings, subheadings, target 350-500 words each
- [x] T-303: Create `src/agent_article/skills/writer_skill/references/` with section length guide

### 6.4 Editor Skill
- [x] T-304: Create `src/agent_article/skills/editor_skill/SKILL.md`
- [x] T-305: Document editing checklist: terminology consistency, citation verification
- [x] T-306: Document table formatting: pipe syntax for Markdown tables
- [x] T-307: Document BiDi verification: ch05 must have ≥2 Hebrew paragraphs
- [x] T-308: Document word limit: no chapter exceeds 550 words
- [x] T-309: Document `[NEEDS_FORMULA]` marker for mathematical relationships
- [x] T-310: Create `src/agent_article/skills/editor_skill/references/` directory

### 6.5 LaTeX Skill
- [x] T-311: Create `src/agent_article/skills/latex_skill/SKILL.md`
- [x] T-312: Document CRITICAL RULE: "fancy formula, not plain text" with WRONG/RIGHT examples
- [x] T-313: Document required LaTeX preamble packages list
- [x] T-314: Document BiDi chapter template with `\begin{hebrew}` environment
- [x] T-315: Document compilation sequence: lualatex → biber → lualatex → lualatex (4 total)
- [x] T-316: Document TikZ block diagram template for Crew architecture
- [x] T-317: Document `biblatex` + `biber` usage (NOT legacy bibtex)
- [x] T-318: Create `src/agent_article/skills/latex_skill/references/` with amsmath cheatsheet

### 6.6 Skill Integration Test
- [x] T-319: Write test: load each of the 4 SKILL.md files and verify non-empty content
- [x] T-320: Write test: verify researcher SKILL.md mentions "citation"
- [x] T-321: Write test: verify latex SKILL.md mentions "fancy formula, not plain text"
- [x] T-322: Run skill integration tests — expect PASS
- [x] T-323: Commit all skill files and tests

---

## Phase 7: Agents (T-341 – T-420)

### 7.1 Base Agent
- [x] T-341: Write failing test: `test_base_agent_build_returns_crewai_agent`
- [x] T-342: Write failing test: `test_base_agent_injects_skill_into_backstory`
- [x] T-343: Write failing test: `test_base_agent_loads_config_from_agents_json`
- [x] T-344: Run tests — expect FAIL
- [x] T-345: Create `src/agent_article/agents/__init__.py`
- [x] T-346: Create `src/agent_article/agents/base_agent.py`
- [x] T-347: Implement `BaseAgent(ABC)` with `config_key`, `tools`, `_skill` attributes
- [x] T-348: Read agent config from `get_config("agents")["agents"][config_key]`
- [x] T-349: Load skill via `FileSkill(self._cfg["skill_ref"])`
- [x] T-350: Implement `_make_agent()` — concatenate backstory + skill content, build `crewai.Agent`
- [x] T-351: Implement `build() → Agent` abstract method
- [x] T-352: Pass tools as `[t.as_crewai_tool() for t in self._tools]`
- [x] T-353: Set `verbose=True` on all agents
- [x] T-354: Run tests — expect PASS
- [x] T-355: Commit `agents/base_agent.py` and tests

### 7.2 Researcher Agent
- [x] T-356: Create `src/agent_article/agents/researcher_agent.py`
- [x] T-357: Implement `ResearcherAgent(BaseAgent)` with `config_key="researcher"`
- [x] T-358: Pass tools: `[WebSearchTool(), FileWriteTool()]`
- [x] T-359: Implement `build()` calling `self._make_agent()`
- [x] T-360: Write test: `test_researcher_has_web_search_tool`
- [x] T-361: Write test: `test_researcher_has_file_write_tool`
- [x] T-362: Run tests — expect PASS
- [x] T-363: Commit `agents/researcher_agent.py`

### 7.3 Writer Agent
- [x] T-364: Create `src/agent_article/agents/writer_agent.py`
- [x] T-365: Implement `WriterAgent(BaseAgent)` with `config_key="writer"`
- [x] T-366: Pass tools: `[FileReadTool(), FileWriteTool()]`
- [x] T-367: Implement `build()` calling `self._make_agent()`
- [x] T-368: Write test: `test_writer_has_file_read_and_write_tools`
- [x] T-369: Run test — expect PASS
- [x] T-370: Commit `agents/writer_agent.py`

### 7.4 Editor Agent
- [x] T-371: Create `src/agent_article/agents/editor_agent.py`
- [x] T-372: Implement `EditorAgent(BaseAgent)` with `config_key="editor"`
- [x] T-373: Pass tools: `[FileReadTool(), FileWriteTool()]`
- [x] T-374: Implement `build()` calling `self._make_agent()`
- [x] T-375: Write test: `test_editor_config_key_matches_agents_json`
- [x] T-376: Run test — expect PASS
- [x] T-377: Commit `agents/editor_agent.py`

### 7.5 LaTeX Agent
- [x] T-378: Create `src/agent_article/agents/latex_agent.py`
- [x] T-379: Implement `LaTeXAgent(BaseAgent)` with `config_key="latex_producer"`
- [x] T-380: Pass tools: `[FileReadTool(), FileWriteTool(), LaTeXCompileTool(), ChartGeneratorTool()]`
- [x] T-381: Implement `build()` calling `self._make_agent()`
- [x] T-382: Write test: `test_latex_agent_goal_contains_fancy_formula_phrase`
- [x] T-383: Verify `config/agents.json::latex_producer::goal` contains "fancy formula, not plain text"
- [x] T-384: Run test — expect PASS
- [x] T-385: Commit `agents/latex_agent.py`

### 7.6 Agent File Length Check
- [x] T-386: Run `uv run python scripts/check_file_lines.py` — verify all agent files ≤150 lines
- [x] T-387: Split any file that exceeds 150 lines before continuing
- [x] T-388: Run full unit tests: `uv run pytest tests/unit/ -v`
- [x] T-389: Commit any fixes

---

## Phase 8: Tasks & Crew (T-421 – T-470)

### 8.1 Article Tasks
- [x] T-421: Create `src/agent_article/tasks/__init__.py`
- [x] T-422: Create `src/agent_article/tasks/article_tasks.py`
- [x] T-423: Implement `build_tasks(researcher, writer, editor, latex, topic)` function
- [x] T-424: Load task descriptions from `get_config("tasks")["tasks"]`
- [x] T-425: Format description with `{topic}` substitution
- [x] T-426: Create `research_task` with `agent=researcher` (no context)
- [x] T-427: Create `write_task` with `context=[research_task]`
- [x] T-428: Create `edit_task` with `context=[write_task]`
- [x] T-429: Create `latex_task` with `context=[edit_task]`
- [x] T-430: Return list: `[research_task, write_task, edit_task, latex_task]`
- [x] T-431: Write test: verify 4 tasks returned with correct context chains
- [x] T-432: Write test: verify topic substitution works in task descriptions
- [x] T-433: Run tests — expect PASS
- [x] T-434: Commit `tasks/article_tasks.py` and tests

### 8.2 Article Crew
- [x] T-435: Create `src/agent_article/crew/__init__.py`
- [x] T-436: Create `src/agent_article/crew/article_crew.py`
- [x] T-437: Implement `CrewResult` dataclass with `raw_output: str` and `pdf_path: str | None`
- [x] T-438: Implement `ArticleCrew.__init__()` — reads crew.json config
- [x] T-439: Implement `kickoff(topic, extra_inputs)` method
- [x] T-440: Build all 4 agents via `ResearcherAgent().build()` etc.
- [x] T-441: Call `build_tasks(researcher, writer, editor, latex, topic=topic)`
- [x] T-442: Create `crewai.Crew` with `Process.sequential` and `verbose=True`
- [x] T-443: Call `crew.kickoff(inputs={"topic": topic, ...})`
- [x] T-444: Construct pdf_path from `config/latex.json` + `config/setup.json`
- [x] T-445: Log `"crew_kickoff"` and `"crew_done"` events
- [x] T-446: Write integration test: mock Crew.kickoff, verify crew is assembled with 4 agents
- [x] T-447: Write integration test: verify topic passed to all tasks
- [x] T-448: Run tests — expect PASS
- [x] T-449: Commit `crew/article_crew.py` and tests

---

## Phase 9: SDK, Menu, Entry Point (T-471 – T-510)

### 9.1 ArticleSDK
- [x] T-471: Create `src/agent_article/sdk/__init__.py`
- [x] T-472: Create `src/agent_article/sdk/sdk.py`
- [x] T-473: Implement `ArticleResult` dataclass: `pdf_path`, `token_cost`, `compile_warnings`
- [x] T-474: Implement `ArticleSDK.__init__()` creating `ArticleCrew` and `StructuredLogger`
- [x] T-475: Implement `generate_article(topic: str) → CrewResult`
- [x] T-476: Implement `approve_markdown() → bool` — `input()` prompt, returns bool
- [x] T-477: Implement `compile_pdf() → str` — calls `LaTeXCompileTool().run()`
- [x] T-478: Implement `get_spend_report() → dict` — delegates to `ApiGatekeeper.instance()`
- [x] T-479: Implement `run_audit() → dict` — checks main.tex for fancy formula markers
- [x] T-480: `run_audit()` checks for `\begin{equation}` or `\frac{` or `\sum_` in .tex files
- [x] T-481: `run_audit()` checks .log for "Overfull \hbox"
- [x] T-482: Write test: `test_sdk_generate_article_calls_crew` (mock ArticleCrew)
- [x] T-483: Write test: `test_sdk_approve_markdown_returns_true_on_y` (mock input)
- [x] T-484: Write test: `test_sdk_approve_markdown_returns_false_on_n` (mock input)
- [x] T-485: Write test: `test_sdk_run_audit_detects_missing_formula`
- [x] T-486: Run tests — expect PASS
- [x] T-487: Commit `sdk/sdk.py` and tests

### 9.2 Terminal Menu
- [x] T-488: Create `src/agent_article/menu/__init__.py`
- [x] T-489: Create `src/agent_article/menu/tui.py`
- [x] T-490: Implement `MENU` constant string with G/C/A/S/X options
- [x] T-491: Implement `TerminalMenu.__init__()` — creates `Console()` and `ArticleSDK()`
- [x] T-492: Implement `run()` — while-loop with `input("Choice: ")`
- [x] T-493: Handle `G` → call `_run_generation(topic)`
- [x] T-494: Handle `C` → call `sdk.compile_pdf()` and display result
- [x] T-495: Handle `A` → call `sdk.run_audit()` and display result
- [x] T-496: Handle `S` → call `sdk.get_spend_report()` and display
- [x] T-497: Handle `X` → break loop
- [x] T-498: Implement `_run_generation(topic)` with approve_markdown checkpoint
- [x] T-499: Load `default_topic` from `config/setup.json`
- [x] T-500: Write test: `test_menu_exits_on_X` (mock input returning "X")
- [x] T-501: Run test — expect PASS
- [x] T-502: Commit `menu/tui.py` and tests

### 9.3 Entry Point
- [x] T-503: Create `src/agent_article/main.py`
- [x] T-504: Implement `main()` function calling `TerminalMenu().run()`
- [x] T-505: Add `if __name__ == "__main__": main()` guard
- [x] T-506: Verify `uv run agent-article` launches the TUI
- [x] T-507: Write test: `test_main_calls_terminal_menu_run` (mock TerminalMenu)
- [x] T-508: Run test — expect PASS
- [x] T-509: Commit `main.py` and test

---

## Phase 10: LaTeX Project (T-511 – T-570)

### 10.1 Style File
- [x] T-511: Create `latex/style/article.sty`
- [x] T-512: Add `fontspec` package with FreeSerif main font
- [x] T-513: Add `polyglossia` package with English main + Hebrew other
- [x] T-514: Add `amsmath`, `amssymb`, `amsthm` packages
- [x] T-515: Add `biblatex` with `backend=biber`, `style=numeric-comp`, `sorting=none`
- [x] T-516: Add `hyperref` with colorlinks, linkcolor=blue, citecolor=blue
- [x] T-517: Add `geometry` package: a4paper, margin=2.5cm
- [x] T-518: Add `fancyhdr` package and configure headers/footers
- [x] T-519: Set `fancyhead[L]` = article title and `fancyhead[R]` = course number
- [x] T-520: Set `fancyfoot[C]` = `\thepage`
- [x] T-521: Add `graphicx` with `\graphicspath{{figures/}}`
- [x] T-522: Add `tikz` with `shapes`, `arrows.meta`, `positioning`, `fit` libraries
- [x] T-523: Add `tabularx`, `booktabs` packages
- [x] T-524: Add `listings` package for code snippets

### 10.2 Main Document
- [x] T-525: Create `latex/main.tex`
- [x] T-526: Add `\documentclass[12pt,a4paper]{article}`
- [x] T-527: Add `\usepackage{style/article}`
- [x] T-528: Add `\addbibresource{bib/references.bib}`
- [x] T-529: Add `\title{}` with topic, authors, course, lecturer
- [x] T-530: Cover `\title` MUST include "Course 203.3763" and "Dr. Yoram Reuven Segal"
- [x] T-531: Add `\maketitle` on page 1, `\newpage`
- [x] T-532: Add `\tableofcontents`, `\newpage`
- [x] T-533: Add `\input` for each of 6 chapters with `\newpage` between
- [x] T-534: Add `\printbibliography[heading=bibintoc]` at end

### 10.3 Chapter Stubs
- [x] T-535: Create `latex/chapters/ch01_introduction.tex` stub
- [x] T-536: Create `latex/chapters/ch02_architectures.tex` stub
- [x] T-537: Create `latex/chapters/ch03_frameworks.tex` stub
- [x] T-538: Create `latex/chapters/ch04_production.tex` stub
- [x] T-539: Create `latex/chapters/ch05_bidi.tex` stub
- [x] T-540: Create `latex/chapters/ch06_casestudy.tex` stub

### 10.4 TikZ Crew Architecture Diagram
- [x] T-541: Create `latex/figures/crew_architecture.tikz`
- [x] T-542: Define `agent` TikZ style: rectangle, blue, rounded corners
- [x] T-543: Define `arrow` TikZ style: Stealth arrowhead, thick
- [x] T-544: Add ResearcherAgent node
- [x] T-545: Add WriterAgent node (right of Researcher)
- [x] T-546: Add EditorAgent node (right of Writer)
- [x] T-547: Add LaTeXAgent node (right of Editor)
- [x] T-548: Add arrows with file labels: "notes.md", "ch*.md", "*_edited.md"
- [x] T-549: Add output node: PDF (right of LaTeX)
- [x] T-550: Add ApiGatekeeper dashed box below all agents
- [x] T-551: Add `Process.sequential` label above diagram
- [x] T-552: Test: include diagram in ch01.tex stub and compile to verify no TikZ errors

### 10.5 Bibliography
- [x] T-553: Create `latex/bib/references.bib`
- [x] T-554: Add `LangChain2024` entry (GitHub, 2024)
- [x] T-555: Add `CrewAI2024` entry (GitHub, 2024)
- [x] T-556: Add `LangGraph2024` entry (GitHub, 2024)
- [x] T-557: Add `RussellNorvig2020` book entry (AI: A Modern Approach, 4th ed)
- [x] T-558: Add `AutoGPT2023` entry
- [x] T-559: Add at least 3 more entries (papers, docs) to reach ≥8 total
- [x] T-560: Verify all .bib entries have author, title, year, url fields

### 10.6 LaTeX Makefile & Build Script
- [x] T-561: Create `latex/Makefile` with all target
- [x] T-562: Implement 4-pass compile sequence in Makefile
- [x] T-563: Add `clean` target removing .aux, .log, .toc, .bbl, .blg, .bcf, .xml
- [x] T-564: Create `scripts/build_article.py` with Python-driven 4-pass compile
- [x] T-565: Print progress: "[1/4] lualatex...", "[2/4] biber...", etc.
- [x] T-566: Print final PDF size in KB on success
- [x] T-567: Raise SystemExit on compile failure with last 2000 chars of stderr
- [x] T-568: Test: compile the skeleton (stub chapters) — should produce PDF
- [x] T-569: Verify `latex/output/main.pdf` exists after `uv run python scripts/build_article.py`
- [x] T-570: Commit all LaTeX files and build script

---

## Phase 11: Integration Tests (T-571 – T-610)

### 11.1 conftest.py
- [x] T-571: Write `mock_config` fixture — provides tmp_path config dir with all JSON files
- [x] T-572: Write `mock_llm` fixture — patches `crewai.Agent` to return MagicMock
- [x] T-573: Write `tmp_workspace` fixture — creates workspace/chapters/ in tmp_path
- [x] T-574: Write `mock_gatekeeper` fixture — resets ApiGatekeeper._instance
- [x] T-575: Commit `tests/conftest.py`

### 11.2 Integration: Crew Assembly
- [x] T-576: Write `test_crew_kickoff_calls_all_4_agents` — mock all agents and Crew
- [x] T-577: Write `test_crew_kickoff_passes_topic_to_tasks` — verify topic in task descriptions
- [x] T-578: Write `test_crew_result_has_pdf_path` — verify CrewResult.pdf_path set
- [x] T-579: Write `test_crew_sequential_process` — verify `Process.sequential` used
- [x] T-580: Run integration crew tests — expect PASS
- [x] T-581: Commit `tests/integration/test_article_crew.py`

### 11.3 Integration: LaTeX Pipeline
- [x] T-582: Write `test_latex_compile_tool_subprocess_calls` — mock subprocess.run
- [x] T-583: Write `test_latex_skeleton_compiles` — real lualatex, skip if not installed
- [x] T-584: Write `test_chart_generator_produces_includable_png`
- [x] T-585: Write `test_bib_file_has_minimum_5_entries` — parse references.bib
- [x] T-586: Run integration LaTeX tests — expect PASS (or skip if no lualatex)
- [x] T-587: Commit `tests/integration/test_latex_pipeline.py`

### 11.4 Coverage Check
- [x] T-588: Run `uv run pytest tests/unit tests/integration --cov=src --cov-report=term-missing`
- [x] T-589: Identify uncovered branches (look for lines marked as missed)
- [x] T-590: Add tests for any critical uncovered path (error branches, edge cases)
- [x] T-591: Re-run coverage — verify ≥85%
- [x] T-592: If below 85%, add more unit tests targeting the lowest-coverage modules
- [x] T-593: Run `uv run python scripts/check_file_lines.py` — verify all files ≤150 lines
- [x] T-594: Run `uv run ruff check src tests scripts` — verify 0 errors
- [x] T-595: Fix all ruff violations before proceeding
- [x] T-596: Commit all test fixes

---

## Phase 12: Per-Mechanism PRDs (T-611 – T-630)

- [x] T-611: Write `docs/PRD_crew_orchestrator.md` with Input/Output/Setup + all required sections
- [x] T-612: Write `docs/PRD_researcher_agent.md`
- [x] T-613: Write `docs/PRD_writer_agent.md`
- [x] T-614: Write `docs/PRD_editor_agent.md`
- [x] T-615: Write `docs/PRD_latex_agent.md`
- [x] T-616: Write `docs/PRD_skill_layer.md`
- [x] T-617: Write `docs/PRD_tools.md`
- [x] T-618: Write `docs/PRD_gatekeeper.md`
- [x] T-619: Write `docs/PRD_bibliography.md`
- [x] T-620: Write `docs/PRD_chart_generator.md`
- [x] T-621: Verify each PRD has: Input, Output, Setup, Responsibilities, Interface, Test strategy, Acceptance criteria
- [x] T-622: Commit all per-mechanism PRDs

---

## Phase 12b: GAP FIX — ADR Files, Class Diagram, Static Image (T-T1 – T-T9)

> Added after PRD verification: these requirements were in PRD/PLAN but missing from TODO tasks.

- [x] T-T1: Create `docs/diagrams/class_diagram.md` — copy class diagram from PLAN.md into dedicated file
- [x] T-T2: Create `docs/ADRs/ADR-001-crewai-over-langgraph.md` — copy ADR-001 from PLAN.md
- [x] T-T3: Create `docs/ADRs/ADR-002-sequential-over-hierarchical.md`
- [x] T-T4: Create `docs/ADRs/ADR-003-markdown-first-workflow.md`
- [x] T-T5: Create `docs/ADRs/ADR-004-lualatex-over-xelatex.md`
- [x] T-T6: Create `docs/ADRs/ADR-005-single-llm-provider.md`
- [x] T-T7: Create `docs/ADRs/ADR-006-file-based-skill-layer.md`
- [x] T-T8: Create `docs/ADRs/ADR-007-duckduckgo-web-search.md`
- [x] T-T9: Source or create static image `latex/figures/cover_logo.png` (H4 — image distinct from Python chart). Use matplotlib to generate a simple logo/icon PNG if no CC0 image available.
- [x] T-T10: Commit ADR files, class diagram, and static image

---

## Phase 13: PROMPTS.md (T-623 – T-635)

- [x] T-623: Create `docs/PROMPTS.md`
- [x] T-624: Add Entry 001: Researcher agent role prompt
- [x] T-625: Add Entry 002: Writer agent role prompt
- [x] T-626: Add Entry 003: Editor agent role prompt
- [x] T-627: Add Entry 004: LaTeX agent role with "fancy formula, not plain text"
- [x] T-628: Add Entry 005-008: 4 agent goal prompts
- [x] T-629: Add Entry 009-012: 4 agent backstory prompts
- [x] T-630: Add Entry 013-016: 4 task description prompts
- [x] T-631: Add Entry 017: BiDi chapter prompt
- [x] T-632: Add Entry 018: TikZ diagram prompt
- [x] T-633: Add Entry 019: Fancy formula enforcement prompt
- [x] T-634: Add Entry 020-025: 6 coding prompts used during implementation
- [x] T-635: Commit `docs/PROMPTS.md`

---

## Phase 14: Full E2E Run & PDF Validation (T-636 – T-645)

- [x] T-636: Verify Claude CLI is logged in: `claude --version`
- [x] T-637: Run `uv run agent-article` and press G
- [x] T-638: Wait for ResearcherAgent to complete — verify `workspace/research_notes.md` exists
- [x] T-639: Wait for WriterAgent — verify 6 `workspace/chapters/ch0N.md` files exist
- [x] T-640: Wait for EditorAgent — verify 6 `workspace/chapters/ch0N_edited.md` files exist
- [x] T-641: Approve Markdown at human checkpoint: type `y`
- [x] T-642: Wait for LaTeXAgent — verify `latex/output/uoh-sqak-article.pdf` exists
- [x] T-643: Open PDF — verify ≥15 pages, cover, TOC, all 6 chapters, bibliography
- [x] T-644: Click a citation in the PDF — verify it jumps to bibliography
- [x] T-645: Verify fancy formula is in Chapter 4 (not plain text)

---

## Phase 15: README & Final Docs (T-646 – T-650)

- [x] T-646: Write `README.md` — full product manual (Quick Start, Install, Usage, Architecture, Config, Cost, Extend, Ethics, License)
- [x] T-647: Add verbatim AI usage disclosure (Hebrew + English)
- [x] T-648: Add link to `docs/PROMPTS.md` in README AI section
- [x] T-649: Add sample PDF screenshot or link in README
- [x] T-650: Run `uv run python scripts/check_file_lines.py` final check

---

## Phase 16: Submission (T-651 – T-660)

- [x] T-651: Tag final commit: `git tag v1.00`
- [x] T-652: Push to GitHub: `git push origin main --tags`
- [x] T-653: Verify repo public (incognito browser)
- [x] T-654: Count commits on main — must be ≥50
- [x] T-655: Run `uv run python scripts/fill_submission_pdf.py` to generate `uoh-sqak-ex03.pdf`
- [x] T-656: Verify submission PDF: exercise=03, group=uoh-sqak, self-grade=85, both names
- [x] T-657: Upload `uoh-sqak-ex03.pdf` to Moodle id=270973 as Salah Qadah
- [x] T-658: Upload `uoh-sqak-ex03.pdf` to Moodle id=270973 as Andalus Kalash (separate upload)
- [x] T-659: Note submission timestamp (must be before Friday 12 June 2026, 23:59 Asia/Jerusalem)
- [x] T-660: Report back to orchestrator: repo URL, PDF page count, coverage%, commit count, any open issues

---

## Phase 17: Fast Pipeline — Haiku + Parallel LaTeX (T-661 – T-710)

> Implementing PRD_fast_pipeline.md (FP-01). Goal: reduce wall-clock from ~70 min to ≤10 min.
> Strategy: Haiku model by default, Sonnet for ch05 only, parallel ThreadPoolExecutor for 7 LaTeX tasks.

### 17a — PRD & Docs (T-661 – T-664)
- [x] T-661: Create `docs/PRD_fast_pipeline.md` — Option C spec (Haiku + Parallel), Input/Output/Setup, Acceptance Criteria
- [x] T-662: Add fast pipeline section to `docs/PLAN.md` (architecture diagram, threading model)
- [x] T-663: Add FP-01 entries to PRD coverage checklist at bottom of this file
- [x] T-664: Commit PRD, PLAN update, and this TODO batch: `feat(docs): add fast pipeline PRD and TODO tasks (FP-01)`

### 17b — Config: per-task model override (T-665 – T-669)
- [x] T-665: Add `"default_model": "claude-haiku-4-5-20251001"` field to `config/setup.json`
- [x] T-666: Add `"model"` field to each of the 7 latex task entries in `config/tasks.json` — haiku for ch01–ch04, ch06, bib; sonnet for ch05
- [x] T-667: Add `"haiku_timeout_seconds": 300` and `"sonnet_timeout_seconds": 600` to `config/rate_limits.json`
- [x] T-668: Update `shared/config.py` — expose `default_model`, `haiku_timeout`, `sonnet_timeout` properties
- [x] T-669: Commit config changes: `feat(config): add per-task model override fields for fast pipeline`

### 17c — ClaudeCLILLM: model + timeout per-instance (T-670 – T-675)
- [x] T-670: Write failing test `tests/unit/test_claude_cli_llm_model.py` — assert `ClaudeCLILLM(model="claude-haiku-4-5-20251001").model == "claude-haiku-4-5-20251001"`
- [x] T-671: Run test to confirm it fails: `uv run pytest tests/unit/test_claude_cli_llm_model.py -v`
- [x] T-672: Update `ClaudeCLILLM` — replace hardcoded model string with `model: str` field, default from config `default_model`; update `_build_cmd()` to pass `--model {self.model}`; keep timeout field driven by config
- [x] T-673: Run test to confirm it passes
- [x] T-674: Confirm `shared/claude_cli_llm.py` is still ≤ 150 lines: `awk 'NF && !/^[[:space:]]*#/' src/agent_article/shared/claude_cli_llm.py | wc -l`
- [x] T-675: Commit: `feat(llm): per-instance model + timeout from config in ClaudeCLILLM`

### 17d — Tasks: per-task model-aware agent (T-676 – T-682)
- [x] T-676: Write failing test `tests/unit/test_build_latex_tasks_model.py` — assert `build_latex_tasks(...)` produces Task whose agent uses haiku for ch01 and sonnet for ch05
- [x] T-677: Run test to confirm it fails
- [x] T-678: Update `build_latex_tasks()` in `tasks/article_tasks.py` — read `model` field from `config/tasks.json` per task; instantiate `ClaudeCLILLM(model=task_model)` and build a new `LaTeXAgent` instance for that task
- [x] T-679: Run test to confirm it passes
- [x] T-680: Confirm `article_tasks.py` is still ≤ 150 lines
- [x] T-681: Run full ruff check: `uv run ruff check src/agent_article/tasks/article_tasks.py`
- [x] T-682: Commit: `feat(tasks): per-task model override for LaTeX tasks`

### 17e — Crew: parallel LaTeX phase (T-683 – T-693)
- [x] T-683: Write failing test `tests/unit/test_parallel_latex.py` — mock `ClaudeCLILLM.call()` to record call timestamps; run `_run_latex_phase_parallel([t1..t7])`; assert all 7 tasks were called and max(start_times) - min(start_times) < 5s (they ran concurrently)
- [x] T-684: Run test to confirm it fails
- [x] T-685: Add `_run_latex_phase_parallel(tasks: list[Task]) -> list[str]` to `crew/article_crew.py` — uses `concurrent.futures.ThreadPoolExecutor(max_workers=min(7, os.cpu_count()))` to call each task's agent synchronously in a thread; writes output to `task.output_file`; logs thread ID + task name at start and completion; returns list of output file paths
- [x] T-686: Update `ArticleCrew.run()` — after sequential crew finishes editor task, call `_run_latex_phase_parallel(latex_tasks)` instead of including latex tasks in the CrewAI sequential process
- [x] T-687: Run test to confirm it passes
- [x] T-688: Confirm `article_crew.py` is still ≤ 150 lines; if not, extract helpers to `crew/_latex_parallel.py`
- [x] T-689: Run ruff check on modified files: `uv run ruff check src/agent_article/crew/`
- [x] T-690: Run full test suite: `uv run pytest tests/ -v`
- [x] T-691: Commit: `feat(crew): parallel LaTeX task execution via ThreadPoolExecutor`

### 17f — Agent prompt quality rules (T-694 – T-700)
- [x] T-694: Update all 6 `latex_ch*` task descriptions in `config/tasks.json` — prepend explicit rule block: (1) output ONLY LaTeX (first char must be `%` or `\`); (2) tables always use `p{Xcm}` column types; (3) no markdown fences; (4) no trailing prose after LaTeX content; (5) cite keys must exactly match the `[AuthorYear]` keys in `workspace/research_notes.md`
- [x] T-695: Update `latex_bib` task description — add rule: generate `@misc`/`@article`/`@book` entries for EVERY `[AuthorYear]` key used in chapter files
- [x] T-696: Update `latex/skills/latex_skill/SKILL.md` — add "LaTeX Agent Quality Checklist" section encoding the same rules as SKILL.md backstory injection
- [x] T-697: Bump `config/tasks.json` version field to 1.03
- [x] T-698: Commit: `feat(prompts): encode table/citation/output quality rules into agent task descriptions`

### 17g — Integration test + timing (T-701 – T-706)
- [x] T-701: Write `tests/integration/test_fast_pipeline.py` — mock `ClaudeCLILLM.call()` to return minimal valid LaTeX; assert all 7 `.tex` files are written; assert bib file is written; assert PDF compile is called after
- [x] T-702: Run integration test: `uv run pytest tests/integration/test_fast_pipeline.py -v`
- [x] T-703: Run full test suite + coverage: `uv run pytest --cov=src/agent_article --cov-report=term-missing`
- [x] T-704: Confirm coverage ≥ 85%
- [x] T-705: Run ruff on entire src: `uv run ruff check src/`
- [x] T-706: Commit: `test: integration test for parallel fast pipeline (FP-01)`

### 17h — Live timing run (T-707 – T-710)
- [x] T-707: Delete stale generated files: `rm -f latex/chapters/*.tex latex/bib/references.bib latex/output/*.pdf workspace/research_notes.md workspace/chapters/*.md`
- [x] T-708: Run timed end-to-end: `time printf "1\nMulti-Agent Orchestration Patterns in AI Systems\n" | uv run python -m agent_article.main 2>&1 | tee results/fast_pipeline_run.log`
- [x] T-709: Verify wall-clock ≤ 10 min; verify PDF ≥ 15 pages; verify no `[AuthorYear]` bold keys in PDF
- [x] T-710: Commit final result: `feat(pipeline): FP-01 complete — parallel Haiku pipeline ≤10 min`

---

## PRD Coverage Verification Checklist

> All FR and NFR from `docs/PRD.md` must appear in at least one TODO task.

| PRD Requirement | TODO Task |
|---|---|
| FR-01: 4 CrewAI agents | T-356 – T-385 |
| FR-02: Sequential process | T-441 – T-443 |
| FR-03: Markdown-first workflow | T-421 – T-430, T-476 |
| FR-04: LaTeX PDF ≥15 pages | T-511 – T-570, T-636 – T-645 |
| FR-05: Human-in-the-loop | T-476, T-498 |
| FR-06: SDK sole entry point | T-471 – T-487 |
| FR-07: Gatekeeper | T-160 – T-178 |
| FR-08: Terminal menu | T-488 – T-509 |
| FR-09: Structured logging | T-146 – T-159 |
| FR-10: LaTeX features | T-511 – T-560 |
| FR-11: Python chart | T-230 – T-244 |
| FR-12: Version management | T-131 – T-138 |
| FR-13: Skill layer | T-281 – T-323 |
| FR-14: Config-driven | T-091 – T-130 |
| FR-15: Secret management | T-004 – T-008 |
| NFR-01: Performance | T-636 – T-642 |
| NFR-02: Code quality | T-068 – T-090, T-593 – T-595 |
| NFR-03: Test coverage | T-588 – T-596 |
| NFR-04: Portability | T-033, T-074 – T-084 |
| NFR-05: ≥50 commits | T-654 |
| NFR-06: Maintainability | T-339 (extension points) |
| NFR-07: Security | T-004, T-069, T-080 |
| NFR-08: Documentation | T-611 – T-650 |
| AC-01: PDF quality | T-636 – T-645 |
| AC-02: Code quality | T-074 – T-090 |
| AC-03: Repository | T-001 – T-010, T-651 – T-654 |
| AC-04: Submission | T-655 – T-660 |
| FP-FR-01: Haiku default model | T-665, T-670 – T-675 |
| FP-FR-02: Per-task model override | T-666, T-676 – T-682 |
| FP-FR-03: ch05 Sonnet override | T-666, T-678 |
| FP-FR-04: Parallel ThreadPoolExecutor | T-683 – T-691 |
| FP-FR-05: Parallel logging | T-685 |
| FP-FR-06: output_file per thread | T-685, T-686 |
| FP-FR-07: Post-parallel compile | T-686 |
| FP-FR-08: Task failure logging | T-685 |
| FP-FR-09: ≤10 min wall-clock | T-707 – T-709 |
| FP-FR-10: model field in tasks.json | T-666 |
| FP-FR-11: Agent prompt quality rules | T-694 – T-698 |

---

## Phase 18: Post-Pipeline LaTeX Repair Loop (T-711 – T-724)

### 18a — Design
- [x] T-711: Brainstorm post-pipeline compile-and-fix loop; select hybrid approach (known-pattern first, agent re-prompt for unknowns)
- [x] T-712: Write design spec `docs/superpowers/specs/2026-06-10-post-pipeline-latex-repair-design.md`
- [x] T-713: Write implementation plan `docs/superpowers/plans/2026-06-10-latex-repair-loop.md`

### 18b — latex_log_parser.py
- [x] T-714: Write `tests/unit/test_latex_log_parser.py` (8 tests) — TDD red phase
- [x] T-715: Implement `src/agent_article/crew/latex_log_parser.py` — `LatexError` dataclass + `parse()`
- [x] T-716: Fix ruff violations + file-attribution reset on close-paren; all 8 tests pass

### 18c — latex_patcher.py
- [x] T-717: Write `tests/unit/test_latex_patcher.py` (9 tests) — TDD red phase
- [x] T-718: Implement `src/agent_article/crew/latex_patcher.py` — regex fixes for `undefined_cmd`, `trailing_amp`, `extra_brace`

### 18d — latex_repair_agent.py
- [x] T-719: Write `tests/unit/test_latex_repair_agent.py` (6 tests) — TDD red phase
- [x] T-720: Implement `src/agent_article/crew/latex_repair_agent.py` — LLM re-prompt for unknown errors

### 18e — article_crew.py wiring
- [x] T-721: Write `tests/unit/test_article_crew_repair.py` (5 tests) — TDD red phase
- [x] T-722: Replace `_compile_pdf()` with `_compile_with_repair()` in `article_crew.py`
- [x] T-723: Update `tests/unit/test_crew.py` mock target `_compile_pdf` → `_compile_with_repair`
- [x] T-724: Add `max_repair_attempts: 3` to `config/latex.json`
