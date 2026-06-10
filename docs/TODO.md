# TODO — HW3 Article Generation Pipeline

**Total tasks: 724**
**Minimum: 500 | Target: 650 | Floor (rubric): 500**

Legend: `[ ]` = pending · `[x]` = done · `[-]` = skipped/N/A

---

## Phase 1: Repository & Scaffolding (T-001 – T-060)

### 1.1 GitHub Repository
- [ ] T-001: Create public GitHub repo `salah-dev-stu/uoh-sqak-ex03`
- [ ] T-002: Run `git init` in `hw3/` directory
- [ ] T-003: Add remote origin `https://github.com/salah-dev-stu/uoh-sqak-ex03.git`
- [ ] T-004: Create initial `.gitignore` with `.env`, `__pycache__/`, `*.pyc`, `workspace/`, `latex/output/`, `*.aux`, `*.log`, `*.toc`, `*.bbl`, `*.blg`
- [ ] T-005: Create `.env-example` with `ANTHROPIC_API_KEY=sk-ant-your-key-here`
- [ ] T-006: Add `LUALATEX_PATH=lualatex` to `.env-example`
- [ ] T-007: Add `BIBER_PATH=biber` to `.env-example`
- [ ] T-008: Verify `.env` is NOT committed (grep .gitignore)
- [ ] T-009: Push initial scaffold commit to GitHub
- [ ] T-010: Verify repo is publicly accessible (open in incognito browser)

### 1.2 uv Project Setup
- [ ] T-011: Create `pyproject.toml` with `[project]` metadata
- [ ] T-012: Set `name = "agent-article"` in pyproject.toml
- [ ] T-013: Set `version = "1.00"` in pyproject.toml
- [ ] T-014: Set `requires-python = ">=3.13"` in pyproject.toml
- [ ] T-015: Add `crewai>=0.80.0` to dependencies
- [ ] T-016: Add `langchain-anthropic>=0.3.0` to dependencies
- [ ] T-017: Add `duckduckgo-search>=7.0.0` to dependencies
- [ ] T-018: Add `python-dotenv>=1.0.0` to dependencies
- [ ] T-019: Add `matplotlib>=3.9.0` to dependencies
- [ ] T-020: Add `rich>=13.0.0` to dependencies
- [ ] T-021: Add dev dependency `pytest>=8.0.0`
- [ ] T-022: Add dev dependency `pytest-cov>=5.0.0`
- [ ] T-023: Add dev dependency `ruff>=0.4.0`
- [ ] T-024: Add dev dependency `pre-commit>=3.7.0`
- [ ] T-025: Add `[project.scripts]` entry: `agent-article = "agent_article.main:main"`
- [ ] T-026: Configure `[tool.ruff]` with `line-length = 100`, `target-version = "py313"`
- [ ] T-027: Configure `[tool.ruff.lint]` with `select = ["E","F","W","I","N","UP","B","C4","SIM"]`
- [ ] T-028: Add `ignore = ["E501"]` to ruff config
- [ ] T-029: Configure `[tool.pytest.ini_options]` with `testpaths = ["tests"]`
- [ ] T-030: Add `addopts = "--cov=src --cov-report=term-missing"` to pytest config
- [ ] T-031: Configure `[tool.coverage.report]` with `fail_under = 85`
- [ ] T-032: Configure `[build-system]` with hatchling
- [ ] T-033: Run `uv sync --dev` to install all dependencies
- [ ] T-034: Verify `uv.lock` is created
- [ ] T-035: Commit `pyproject.toml` and `uv.lock`

### 1.3 Directory Structure
- [ ] T-036: Create `src/agent_article/` package directory
- [ ] T-037: Create `src/agent_article/__init__.py` with `__version__ = "1.00"` and `__all__ = ["ArticleSDK"]`
- [ ] T-038: Create `src/agent_article/sdk/` directory with `__init__.py`
- [ ] T-039: Create `src/agent_article/agents/` directory with `__init__.py`
- [ ] T-040: Create `src/agent_article/tasks/` directory with `__init__.py`
- [ ] T-041: Create `src/agent_article/crew/` directory with `__init__.py`
- [ ] T-042: Create `src/agent_article/tools/` directory with `__init__.py`
- [ ] T-043: Create `src/agent_article/skills/` directory with `__init__.py`
- [ ] T-044: Create `src/agent_article/shared/` directory with `__init__.py`
- [ ] T-045: Create `src/agent_article/menu/` directory with `__init__.py`
- [ ] T-046: Create `tests/unit/` directory with `__init__.py`
- [ ] T-047: Create `tests/integration/` directory with `__init__.py`
- [ ] T-048: Create `tests/conftest.py` placeholder
- [ ] T-049: Create `docs/ADRs/` directory
- [ ] T-050: Create `docs/diagrams/` directory
- [ ] T-051: Create `config/` directory
- [ ] T-052: Create `workspace/` directory with `.gitkeep` (git-ignored content)
- [ ] T-053: Create `results/` directory with `.gitkeep`
- [ ] T-054: Create `assets/` directory with `.gitkeep`
- [ ] T-055: Create `scripts/` directory
- [ ] T-056: Create `latex/chapters/` directory
- [ ] T-057: Create `latex/figures/` directory
- [ ] T-058: Create `latex/bib/` directory
- [ ] T-059: Create `latex/style/` directory
- [ ] T-060: Create `latex/output/` directory (git-ignored)

---

## Phase 2: Quality Automation (T-061 – T-090)

### 2.1 Line Count Script
- [ ] T-061: Create `scripts/check_file_lines.py`
- [ ] T-062: Implement `count_logical_lines(path)` — skip blank lines and comment-only lines
- [ ] T-063: Implement `main()` — scan `src/`, `tests/`, `scripts/` for .py files
- [ ] T-064: Print violation list and return exit code 1 if any file > 150 lines
- [ ] T-065: Print "OK" and return exit code 0 if all files pass
- [ ] T-066: Test: create a 151-line test file and verify script catches it
- [ ] T-067: Commit `scripts/check_file_lines.py`

### 2.2 Pre-Commit Hooks
- [ ] T-068: Create `.pre-commit-config.yaml`
- [ ] T-069: Add `ruff` hook from `astral-sh/ruff-pre-commit` rev v0.4.0
- [ ] T-070: Add `check-file-lines` local hook pointing to `scripts/check_file_lines.py`
- [ ] T-071: Run `uv run pre-commit install` to wire up hooks
- [ ] T-072: Run `uv run pre-commit run --all-files` to verify hooks pass on current state
- [ ] T-073: Commit `.pre-commit-config.yaml`

### 2.3 GitHub Actions CI
- [ ] T-074: Create `.github/workflows/ci.yml`
- [ ] T-075: Add trigger on `push` and `pull_request`
- [ ] T-076: Add `ubuntu-latest` runner with Python 3.13
- [ ] T-077: Add `astral-sh/setup-uv` step
- [ ] T-078: Add `uv sync --dev` step
- [ ] T-079: Add `uv run ruff check src tests scripts` step
- [ ] T-080: Add `uv run python scripts/check_file_lines.py` step
- [ ] T-081: Add `uv run pytest tests/unit tests/integration --cov=src --cov-fail-under=85` step
- [ ] T-082: Add TeX Live installation step for integration tests (`sudo apt-get install texlive-full`)
- [ ] T-083: Commit `.github/workflows/ci.yml`
- [ ] T-084: Push to GitHub and verify CI runs green
- [ ] T-085: Fix any CI failures before proceeding

### 2.4 Project-Level Makefile
- [ ] T-086: Create top-level `Makefile` with targets: `install`, `test`, `lint`, `clean`, `pdf`
- [ ] T-087: `make install` → `uv sync --dev`
- [ ] T-088: `make test` → `uv run pytest tests/unit tests/integration --cov=src`
- [ ] T-089: `make lint` → `uv run ruff check src tests scripts`
- [ ] T-090: `make pdf` → `cd latex && make`

---

## Phase 3: Configuration Files (T-091 – T-130)

### 3.1 Config Files
- [ ] T-091: Create `config/setup.json` with version, package name, workspace_dir, results_dir, latex_dir, output_filename
- [ ] T-092: Set `"version": "1.00"` in setup.json
- [ ] T-093: Set `"workspace_dir": "workspace"` in setup.json
- [ ] T-094: Set `"output_filename": "uoh-sqak-article.pdf"` in setup.json
- [ ] T-095: Create `config/agents.json` with version and agents dict
- [ ] T-096: Add `researcher` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [ ] T-097: Add `writer` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [ ] T-098: Add `editor` agent entry: role, goal, backstory, llm, skill_ref, temperature
- [ ] T-099: Add `latex_producer` agent entry — goal MUST include "fancy formula, not plain text"
- [ ] T-100: Verify `latex_producer` backstory mentions "fancy formula, not plain text"
- [ ] T-101: Create `config/tasks.json` with version and tasks dict
- [ ] T-102: Add `research` task: description template with `{topic}` placeholder, expected_output
- [ ] T-103: Add `write` task: description referencing research_notes.md, 6-chapter structure
- [ ] T-104: Add `edit` task: description referencing workspace/chapters/
- [ ] T-105: Add `latex` task: description including "fancy formula, not plain text" verbatim
- [ ] T-106: Verify all task descriptions use `{topic}` placeholder (not hardcoded topic)
- [ ] T-107: Create `config/crew.json` with process, verbose, agent list, task list
- [ ] T-108: Create `config/rate_limits.json` with services: claude_cli, duckduckgo, lualatex
- [ ] T-109: Set `requests_per_minute: 10` for claude_cli
- [ ] T-110: Set `tokens_per_article: 200000` for claude_cli
- [ ] T-111: Set `hard_cap_percent: 95` for claude_cli
- [ ] T-112: Create `config/logging_config.json` with fifo_files: 20, max_lines_per_file: 500
- [ ] T-113: Create `config/latex.json` with compiler, biber, passes, chapter_list, output_dir
- [ ] T-114: Set `"passes": 4` in latex.json
- [ ] T-115: Set `"compiler": "lualatex"` in latex.json
- [ ] T-116: Set `"bib_style": "numeric-comp"` in latex.json
- [ ] T-117: Add 6 chapter names to `chapter_list` in latex.json
- [ ] T-118: Verify all config files have `"version": "1.00"` field
- [ ] T-119: Verify NO Python source file hardcodes any value from config
- [ ] T-120: Commit all config files

### 3.2 Config Loader
- [ ] T-121: Write failing test: `test_get_config_loads_setup` (tmp_path with fake setup.json)
- [ ] T-122: Run test — expect `ModuleNotFoundError`
- [ ] T-123: Create `src/agent_article/shared/config.py`
- [ ] T-124: Implement `_CONFIG_DIR` pointing to `config/` relative to package root
- [ ] T-125: Implement `_cache: dict[str, Any] = {}` module-level cache
- [ ] T-126: Implement `get_config(name: str) → dict` with cache-first logic
- [ ] T-127: Implement `cfg(name, key, default=None)` single-key accessor
- [ ] T-128: Implement `reload()` to clear cache (for tests)
- [ ] T-129: Run test — expect PASS
- [ ] T-130: Commit `shared/config.py` and test

---

## Phase 4: Shared Infrastructure (T-131 – T-200)

### 4.1 Version Module
- [ ] T-131: Write failing test: `test_version_format` — VERSION has 2 dot-separated parts
- [ ] T-132: Write failing test: `test_bump` — "1.00" → "1.01", "1.09" → "1.10"
- [ ] T-133: Run tests — expect FAIL
- [ ] T-134: Create `src/agent_article/shared/version.py`
- [ ] T-135: Implement `VERSION = "1.00"`
- [ ] T-136: Implement `bump(version: str) → str` — increments patch component
- [ ] T-137: Run tests — expect PASS
- [ ] T-138: Commit `shared/version.py` and tests

### 4.2 Constants
- [ ] T-139: Create `src/agent_article/constants.py`
- [ ] T-140: Implement `AgentRole(StrEnum)` with RESEARCHER, WRITER, EDITOR, LATEX_PRODUCER
- [ ] T-141: Implement `ServiceName(StrEnum)` with CLAUDE_CLI, DUCKDUCKGO, LUALATEX
- [ ] T-142: Implement `ProcessType(StrEnum)` with SEQUENTIAL, HIERARCHICAL
- [ ] T-143: Write test: `test_agent_role_values` — verify string values match config keys
- [ ] T-144: Run test — expect PASS
- [ ] T-145: Commit `constants.py` and test

### 4.3 Structured Logger (FIFO)
- [ ] T-146: Create `src/agent_article/shared/logging_fifo.py`
- [ ] T-147: Implement `StructuredLogger.__init__(component: str)` — reads logging_config.json
- [ ] T-148: Implement `_open_next()` — opens next numbered JSONL file in log_dir
- [ ] T-149: Implement `_rotate_if_needed()` — deletes oldest file when max_files reached
- [ ] T-150: Implement `_write(level, message, **fields)` — writes JSON line, thread-safe with lock
- [ ] T-151: Implement `info(message, **fields)` calling `_write("INFO", ...)`
- [ ] T-152: Implement `error(message, **fields)` calling `_write("ERROR", ...)`
- [ ] T-153: Implement `warning(message, **fields)` calling `_write("WARNING", ...)`
- [ ] T-154: Implement rotation on `_current_lines >= max_lines_per_file`
- [ ] T-155: Write test: verify log file is created in log_dir
- [ ] T-156: Write test: verify JSON structure (ts, level, component, message)
- [ ] T-157: Write test: verify rotation deletes oldest file when max_files exceeded
- [ ] T-158: Run tests — expect PASS
- [ ] T-159: Commit `shared/logging_fifo.py` and tests

### 4.4 API Gatekeeper
- [ ] T-160: Write failing test: `test_call_succeeds` — gatekeeper passes fn() result through
- [ ] T-161: Write failing test: `test_rate_limit_enforced` — 3rd call raises GatekeeperError
- [ ] T-162: Write failing test: `test_singleton` — `instance()` returns same object
- [ ] T-163: Write failing test: `test_budget_cap_raises` — raises at 95% of tokens_per_article
- [ ] T-164: Run tests — expect FAIL
- [ ] T-165: Create `src/agent_article/shared/gatekeeper.py`
- [ ] T-166: Implement `GatekeeperError(Exception)` custom exception class
- [ ] T-167: Implement `UsageRecord` dataclass with tokens_in, tokens_out, calls
- [ ] T-168: Implement `ApiGatekeeper._instance = None` class variable
- [ ] T-169: Implement `ApiGatekeeper.__init__()` — reads rate_limits.json, initializes deques
- [ ] T-170: Implement `instance()` classmethod — creates or returns singleton
- [ ] T-171: Implement `call(service, fn, *args, **kwargs)` — enforce limits then call fn
- [ ] T-172: Implement `_enforce_rate_limit(service)` — sliding window using time.monotonic()
- [ ] T-173: Implement `_check_budget(service)` — compares usage to hard_cap_percent
- [ ] T-174: Implement `get_spend_report()` — returns copy of _usage dict
- [ ] T-175: Add `threading.Lock()` for thread-safety in `_write` operations
- [ ] T-176: Run tests — expect PASS
- [ ] T-177: Verify all tests pass: `uv run pytest tests/unit/test_gatekeeper.py -v`
- [ ] T-178: Commit `shared/gatekeeper.py` and tests

---

## Phase 5: Tools (T-201 – T-280)

### 5.1 BaseTool
- [ ] T-201: Create `src/agent_article/tools/base_tool.py`
- [ ] T-202: Implement `BaseTool(ABC)` abstract base class
- [ ] T-203: Implement `name` abstract property → str
- [ ] T-204: Implement `description` abstract property → str
- [ ] T-205: Implement `run(*args, **kwargs) → Any` abstract method
- [ ] T-206: Implement `as_crewai_tool()` — wraps self using `@tool` decorator
- [ ] T-207: Write test: verify `BaseTool` is abstract (cannot instantiate directly)
- [ ] T-208: Run test — expect PASS

### 5.2 File Read/Write Tools
- [ ] T-209: Write failing test: `test_file_write_and_read` — write then read same file
- [ ] T-210: Write failing test: `test_file_write_creates_parent_dirs` — nested path
- [ ] T-211: Write failing test: `test_file_read_missing_raises` — FileNotFoundError
- [ ] T-212: Run tests — expect FAIL
- [ ] T-213: Create `src/agent_article/tools/file_rw.py`
- [ ] T-214: Implement `FileWriteTool(BaseTool)` with `base_dir` from config
- [ ] T-215: Implement `FileWriteTool.run(relative_path, content)` — creates parent dirs, writes UTF-8
- [ ] T-216: Implement `FileReadTool(BaseTool)` with `base_dir` from config
- [ ] T-217: Implement `FileReadTool.run(relative_path)` — raises FileNotFoundError if missing
- [ ] T-218: Run tests — expect PASS
- [ ] T-219: Commit `tools/file_rw.py` and tests

### 5.3 Web Search Tool
- [ ] T-220: Write failing test: `test_web_search_returns_string` — mock DDGS, verify format
- [ ] T-221: Write failing test: `test_web_search_no_results` — mock empty results, returns "No results"
- [ ] T-222: Run tests — expect FAIL
- [ ] T-223: Create `src/agent_article/tools/web_search.py`
- [ ] T-224: Implement `WebSearchTool(BaseTool)` using `duckduckgo_search.DDGS`
- [ ] T-225: Route search through `ApiGatekeeper.instance().call("duckduckgo", ...)`
- [ ] T-226: Format results as markdown: title, body, URL, separated by `---`
- [ ] T-227: Handle empty results with informative message
- [ ] T-228: Run tests — expect PASS
- [ ] T-229: Commit `tools/web_search.py` and tests

### 5.4 Chart Generator Tool
- [ ] T-230: Write failing test: `test_chart_creates_png` — bar chart, verify file exists
- [ ] T-231: Write failing test: `test_chart_nonzero_size` — file size > 0 bytes
- [ ] T-232: Write failing test: `test_chart_line_type` — line chart type
- [ ] T-233: Write failing test: `test_chart_creates_parent_dir` — creates output dir if needed
- [ ] T-234: Run tests — expect FAIL
- [ ] T-235: Create `src/agent_article/tools/chart_generator.py`
- [ ] T-236: Implement `ChartGeneratorTool(BaseTool)` with `output_dir` from config
- [ ] T-237: Use `matplotlib.use("Agg")` backend (no display required)
- [ ] T-238: Implement `run(chart_type, title, labels, values, ylabel, filename)` method
- [ ] T-239: Support chart types: bar, line, pie
- [ ] T-240: Save to `output_dir/filename` at 150 DPI
- [ ] T-241: Create output_dir if it doesn't exist
- [ ] T-242: Call `plt.close(fig)` to free memory
- [ ] T-243: Run tests — expect PASS
- [ ] T-244: Commit `tools/chart_generator.py` and tests

### 5.5 LaTeX Compile Tool
- [ ] T-245: Write failing test: `test_latex_compile_calls_4_subprocesses` — mock subprocess.run
- [ ] T-246: Write failing test: `test_latex_compile_order` — lualatex, biber, lualatex, lualatex
- [ ] T-247: Write failing test: `test_latex_compile_raises_on_nonzero_returncode`
- [ ] T-248: Write failing test: `test_check_log_warns_on_overfull_hbox`
- [ ] T-249: Run tests — expect FAIL
- [ ] T-250: Create `src/agent_article/tools/latex_compile.py`
- [ ] T-251: Implement `LaTeXCompileTool(BaseTool)` reading compiler/biber paths from config
- [ ] T-252: Implement `run(main_tex="main.tex")` — 4-pass compile sequence
- [ ] T-253: Pass `--interaction=nonstopmode` to lualatex
- [ ] T-254: Implement `_run_cmd(cmd)` — subprocess.run with capture_output, timeout=120
- [ ] T-255: Raise RuntimeError if returncode != 0 with stderr excerpt
- [ ] T-256: Implement `_check_log(stem)` — warn on "Rerun" and "Overfull \hbox"
- [ ] T-257: Route subprocess calls through `ApiGatekeeper.instance().call("lualatex", ...)`
- [ ] T-258: Run tests — expect PASS
- [ ] T-259: Commit `tools/latex_compile.py` and tests

---

## Phase 6: Skills Layer (T-281 – T-340)

### 6.1 Base Skill
- [ ] T-281: Write failing test: `test_file_skill_loads_content` — SKILL.md in tmp_path
- [ ] T-282: Write failing test: `test_file_skill_strips_yaml_frontmatter`
- [ ] T-283: Write failing test: `test_file_skill_missing_raises_file_not_found`
- [ ] T-284: Run tests — expect FAIL
- [ ] T-285: Create `src/agent_article/skills/base_skill.py`
- [ ] T-286: Implement `BaseSkill(ABC)` with `content` abstract property
- [ ] T-287: Implement `FileSkill(BaseSkill)` that reads SKILL.md from `skills/<ref>/SKILL.md`
- [ ] T-288: Strip YAML frontmatter (lines between `---` markers)
- [ ] T-289: Raise `FileNotFoundError` if SKILL.md doesn't exist
- [ ] T-290: Run tests — expect PASS
- [ ] T-291: Commit `skills/base_skill.py` and tests

### 6.2 Researcher Skill
- [ ] T-292: Create `src/agent_article/skills/researcher_skill/SKILL.md`
- [ ] T-293: Add YAML frontmatter: `name: researcher`, `description: Senior research analyst`
- [ ] T-294: Document research protocol: broad survey → 3-5 sources → extract claims → structure output
- [ ] T-295: Document citation format: `[AuthorYear]` inline, full ref at end
- [ ] T-296: Document quality checklist: ≥8 citations, 1500 words, clear headings
- [ ] T-297: Create `src/agent_article/skills/researcher_skill/references/` directory with citation style guide

### 6.3 Writer Skill
- [ ] T-298: Create `src/agent_article/skills/writer_skill/SKILL.md`
- [ ] T-299: Document writing protocol: read all notes → write chapter-by-chapter
- [ ] T-300: Document ch05 requirement: ≥2 Hebrew paragraphs mixed with English
- [ ] T-301: Document style guide: active voice, short sentences, no "utilize"/"leverage"
- [ ] T-302: Document chapter structure: headings, subheadings, target 350-500 words each
- [ ] T-303: Create `src/agent_article/skills/writer_skill/references/` with section length guide

### 6.4 Editor Skill
- [ ] T-304: Create `src/agent_article/skills/editor_skill/SKILL.md`
- [ ] T-305: Document editing checklist: terminology consistency, citation verification
- [ ] T-306: Document table formatting: pipe syntax for Markdown tables
- [ ] T-307: Document BiDi verification: ch05 must have ≥2 Hebrew paragraphs
- [ ] T-308: Document word limit: no chapter exceeds 550 words
- [ ] T-309: Document `[NEEDS_FORMULA]` marker for mathematical relationships
- [ ] T-310: Create `src/agent_article/skills/editor_skill/references/` directory

### 6.5 LaTeX Skill
- [ ] T-311: Create `src/agent_article/skills/latex_skill/SKILL.md`
- [ ] T-312: Document CRITICAL RULE: "fancy formula, not plain text" with WRONG/RIGHT examples
- [ ] T-313: Document required LaTeX preamble packages list
- [ ] T-314: Document BiDi chapter template with `\begin{hebrew}` environment
- [ ] T-315: Document compilation sequence: lualatex → biber → lualatex → lualatex (4 total)
- [ ] T-316: Document TikZ block diagram template for Crew architecture
- [ ] T-317: Document `biblatex` + `biber` usage (NOT legacy bibtex)
- [ ] T-318: Create `src/agent_article/skills/latex_skill/references/` with amsmath cheatsheet

### 6.6 Skill Integration Test
- [ ] T-319: Write test: load each of the 4 SKILL.md files and verify non-empty content
- [ ] T-320: Write test: verify researcher SKILL.md mentions "citation"
- [ ] T-321: Write test: verify latex SKILL.md mentions "fancy formula, not plain text"
- [ ] T-322: Run skill integration tests — expect PASS
- [ ] T-323: Commit all skill files and tests

---

## Phase 7: Agents (T-341 – T-420)

### 7.1 Base Agent
- [ ] T-341: Write failing test: `test_base_agent_build_returns_crewai_agent`
- [ ] T-342: Write failing test: `test_base_agent_injects_skill_into_backstory`
- [ ] T-343: Write failing test: `test_base_agent_loads_config_from_agents_json`
- [ ] T-344: Run tests — expect FAIL
- [ ] T-345: Create `src/agent_article/agents/__init__.py`
- [ ] T-346: Create `src/agent_article/agents/base_agent.py`
- [ ] T-347: Implement `BaseAgent(ABC)` with `config_key`, `tools`, `_skill` attributes
- [ ] T-348: Read agent config from `get_config("agents")["agents"][config_key]`
- [ ] T-349: Load skill via `FileSkill(self._cfg["skill_ref"])`
- [ ] T-350: Implement `_make_agent()` — concatenate backstory + skill content, build `crewai.Agent`
- [ ] T-351: Implement `build() → Agent` abstract method
- [ ] T-352: Pass tools as `[t.as_crewai_tool() for t in self._tools]`
- [ ] T-353: Set `verbose=True` on all agents
- [ ] T-354: Run tests — expect PASS
- [ ] T-355: Commit `agents/base_agent.py` and tests

### 7.2 Researcher Agent
- [ ] T-356: Create `src/agent_article/agents/researcher_agent.py`
- [ ] T-357: Implement `ResearcherAgent(BaseAgent)` with `config_key="researcher"`
- [ ] T-358: Pass tools: `[WebSearchTool(), FileWriteTool()]`
- [ ] T-359: Implement `build()` calling `self._make_agent()`
- [ ] T-360: Write test: `test_researcher_has_web_search_tool`
- [ ] T-361: Write test: `test_researcher_has_file_write_tool`
- [ ] T-362: Run tests — expect PASS
- [ ] T-363: Commit `agents/researcher_agent.py`

### 7.3 Writer Agent
- [ ] T-364: Create `src/agent_article/agents/writer_agent.py`
- [ ] T-365: Implement `WriterAgent(BaseAgent)` with `config_key="writer"`
- [ ] T-366: Pass tools: `[FileReadTool(), FileWriteTool()]`
- [ ] T-367: Implement `build()` calling `self._make_agent()`
- [ ] T-368: Write test: `test_writer_has_file_read_and_write_tools`
- [ ] T-369: Run test — expect PASS
- [ ] T-370: Commit `agents/writer_agent.py`

### 7.4 Editor Agent
- [ ] T-371: Create `src/agent_article/agents/editor_agent.py`
- [ ] T-372: Implement `EditorAgent(BaseAgent)` with `config_key="editor"`
- [ ] T-373: Pass tools: `[FileReadTool(), FileWriteTool()]`
- [ ] T-374: Implement `build()` calling `self._make_agent()`
- [ ] T-375: Write test: `test_editor_config_key_matches_agents_json`
- [ ] T-376: Run test — expect PASS
- [ ] T-377: Commit `agents/editor_agent.py`

### 7.5 LaTeX Agent
- [ ] T-378: Create `src/agent_article/agents/latex_agent.py`
- [ ] T-379: Implement `LaTeXAgent(BaseAgent)` with `config_key="latex_producer"`
- [ ] T-380: Pass tools: `[FileReadTool(), FileWriteTool(), LaTeXCompileTool(), ChartGeneratorTool()]`
- [ ] T-381: Implement `build()` calling `self._make_agent()`
- [ ] T-382: Write test: `test_latex_agent_goal_contains_fancy_formula_phrase`
- [ ] T-383: Verify `config/agents.json::latex_producer::goal` contains "fancy formula, not plain text"
- [ ] T-384: Run test — expect PASS
- [ ] T-385: Commit `agents/latex_agent.py`

### 7.6 Agent File Length Check
- [ ] T-386: Run `uv run python scripts/check_file_lines.py` — verify all agent files ≤150 lines
- [ ] T-387: Split any file that exceeds 150 lines before continuing
- [ ] T-388: Run full unit tests: `uv run pytest tests/unit/ -v`
- [ ] T-389: Commit any fixes

---

## Phase 8: Tasks & Crew (T-421 – T-470)

### 8.1 Article Tasks
- [ ] T-421: Create `src/agent_article/tasks/__init__.py`
- [ ] T-422: Create `src/agent_article/tasks/article_tasks.py`
- [ ] T-423: Implement `build_tasks(researcher, writer, editor, latex, topic)` function
- [ ] T-424: Load task descriptions from `get_config("tasks")["tasks"]`
- [ ] T-425: Format description with `{topic}` substitution
- [ ] T-426: Create `research_task` with `agent=researcher` (no context)
- [ ] T-427: Create `write_task` with `context=[research_task]`
- [ ] T-428: Create `edit_task` with `context=[write_task]`
- [ ] T-429: Create `latex_task` with `context=[edit_task]`
- [ ] T-430: Return list: `[research_task, write_task, edit_task, latex_task]`
- [ ] T-431: Write test: verify 4 tasks returned with correct context chains
- [ ] T-432: Write test: verify topic substitution works in task descriptions
- [ ] T-433: Run tests — expect PASS
- [ ] T-434: Commit `tasks/article_tasks.py` and tests

### 8.2 Article Crew
- [ ] T-435: Create `src/agent_article/crew/__init__.py`
- [ ] T-436: Create `src/agent_article/crew/article_crew.py`
- [ ] T-437: Implement `CrewResult` dataclass with `raw_output: str` and `pdf_path: str | None`
- [ ] T-438: Implement `ArticleCrew.__init__()` — reads crew.json config
- [ ] T-439: Implement `kickoff(topic, extra_inputs)` method
- [ ] T-440: Build all 4 agents via `ResearcherAgent().build()` etc.
- [ ] T-441: Call `build_tasks(researcher, writer, editor, latex, topic=topic)`
- [ ] T-442: Create `crewai.Crew` with `Process.sequential` and `verbose=True`
- [ ] T-443: Call `crew.kickoff(inputs={"topic": topic, ...})`
- [ ] T-444: Construct pdf_path from `config/latex.json` + `config/setup.json`
- [ ] T-445: Log `"crew_kickoff"` and `"crew_done"` events
- [ ] T-446: Write integration test: mock Crew.kickoff, verify crew is assembled with 4 agents
- [ ] T-447: Write integration test: verify topic passed to all tasks
- [ ] T-448: Run tests — expect PASS
- [ ] T-449: Commit `crew/article_crew.py` and tests

---

## Phase 9: SDK, Menu, Entry Point (T-471 – T-510)

### 9.1 ArticleSDK
- [ ] T-471: Create `src/agent_article/sdk/__init__.py`
- [ ] T-472: Create `src/agent_article/sdk/sdk.py`
- [ ] T-473: Implement `ArticleResult` dataclass: `pdf_path`, `token_cost`, `compile_warnings`
- [ ] T-474: Implement `ArticleSDK.__init__()` creating `ArticleCrew` and `StructuredLogger`
- [ ] T-475: Implement `generate_article(topic: str) → CrewResult`
- [ ] T-476: Implement `approve_markdown() → bool` — `input()` prompt, returns bool
- [ ] T-477: Implement `compile_pdf() → str` — calls `LaTeXCompileTool().run()`
- [ ] T-478: Implement `get_spend_report() → dict` — delegates to `ApiGatekeeper.instance()`
- [ ] T-479: Implement `run_audit() → dict` — checks main.tex for fancy formula markers
- [ ] T-480: `run_audit()` checks for `\begin{equation}` or `\frac{` or `\sum_` in .tex files
- [ ] T-481: `run_audit()` checks .log for "Overfull \hbox"
- [ ] T-482: Write test: `test_sdk_generate_article_calls_crew` (mock ArticleCrew)
- [ ] T-483: Write test: `test_sdk_approve_markdown_returns_true_on_y` (mock input)
- [ ] T-484: Write test: `test_sdk_approve_markdown_returns_false_on_n` (mock input)
- [ ] T-485: Write test: `test_sdk_run_audit_detects_missing_formula`
- [ ] T-486: Run tests — expect PASS
- [ ] T-487: Commit `sdk/sdk.py` and tests

### 9.2 Terminal Menu
- [ ] T-488: Create `src/agent_article/menu/__init__.py`
- [ ] T-489: Create `src/agent_article/menu/tui.py`
- [ ] T-490: Implement `MENU` constant string with G/C/A/S/X options
- [ ] T-491: Implement `TerminalMenu.__init__()` — creates `Console()` and `ArticleSDK()`
- [ ] T-492: Implement `run()` — while-loop with `input("Choice: ")`
- [ ] T-493: Handle `G` → call `_run_generation(topic)`
- [ ] T-494: Handle `C` → call `sdk.compile_pdf()` and display result
- [ ] T-495: Handle `A` → call `sdk.run_audit()` and display result
- [ ] T-496: Handle `S` → call `sdk.get_spend_report()` and display
- [ ] T-497: Handle `X` → break loop
- [ ] T-498: Implement `_run_generation(topic)` with approve_markdown checkpoint
- [ ] T-499: Load `default_topic` from `config/setup.json`
- [ ] T-500: Write test: `test_menu_exits_on_X` (mock input returning "X")
- [ ] T-501: Run test — expect PASS
- [ ] T-502: Commit `menu/tui.py` and tests

### 9.3 Entry Point
- [ ] T-503: Create `src/agent_article/main.py`
- [ ] T-504: Implement `main()` function calling `TerminalMenu().run()`
- [ ] T-505: Add `if __name__ == "__main__": main()` guard
- [ ] T-506: Verify `uv run agent-article` launches the TUI
- [ ] T-507: Write test: `test_main_calls_terminal_menu_run` (mock TerminalMenu)
- [ ] T-508: Run test — expect PASS
- [ ] T-509: Commit `main.py` and test

---

## Phase 10: LaTeX Project (T-511 – T-570)

### 10.1 Style File
- [ ] T-511: Create `latex/style/article.sty`
- [ ] T-512: Add `fontspec` package with FreeSerif main font
- [ ] T-513: Add `polyglossia` package with English main + Hebrew other
- [ ] T-514: Add `amsmath`, `amssymb`, `amsthm` packages
- [ ] T-515: Add `biblatex` with `backend=biber`, `style=numeric-comp`, `sorting=none`
- [ ] T-516: Add `hyperref` with colorlinks, linkcolor=blue, citecolor=blue
- [ ] T-517: Add `geometry` package: a4paper, margin=2.5cm
- [ ] T-518: Add `fancyhdr` package and configure headers/footers
- [ ] T-519: Set `fancyhead[L]` = article title and `fancyhead[R]` = course number
- [ ] T-520: Set `fancyfoot[C]` = `\thepage`
- [ ] T-521: Add `graphicx` with `\graphicspath{{figures/}}`
- [ ] T-522: Add `tikz` with `shapes`, `arrows.meta`, `positioning`, `fit` libraries
- [ ] T-523: Add `tabularx`, `booktabs` packages
- [ ] T-524: Add `listings` package for code snippets

### 10.2 Main Document
- [ ] T-525: Create `latex/main.tex`
- [ ] T-526: Add `\documentclass[12pt,a4paper]{article}`
- [ ] T-527: Add `\usepackage{style/article}`
- [ ] T-528: Add `\addbibresource{bib/references.bib}`
- [ ] T-529: Add `\title{}` with topic, authors, course, lecturer
- [ ] T-530: Cover `\title` MUST include "Course 203.3763" and "Dr. Yoram Reuven Segal"
- [ ] T-531: Add `\maketitle` on page 1, `\newpage`
- [ ] T-532: Add `\tableofcontents`, `\newpage`
- [ ] T-533: Add `\input` for each of 6 chapters with `\newpage` between
- [ ] T-534: Add `\printbibliography[heading=bibintoc]` at end

### 10.3 Chapter Stubs
- [ ] T-535: Create `latex/chapters/ch01_introduction.tex` stub
- [ ] T-536: Create `latex/chapters/ch02_architectures.tex` stub
- [ ] T-537: Create `latex/chapters/ch03_frameworks.tex` stub
- [ ] T-538: Create `latex/chapters/ch04_production.tex` stub
- [ ] T-539: Create `latex/chapters/ch05_bidi.tex` stub
- [ ] T-540: Create `latex/chapters/ch06_casestudy.tex` stub

### 10.4 TikZ Crew Architecture Diagram
- [ ] T-541: Create `latex/figures/crew_architecture.tikz`
- [ ] T-542: Define `agent` TikZ style: rectangle, blue, rounded corners
- [ ] T-543: Define `arrow` TikZ style: Stealth arrowhead, thick
- [ ] T-544: Add ResearcherAgent node
- [ ] T-545: Add WriterAgent node (right of Researcher)
- [ ] T-546: Add EditorAgent node (right of Writer)
- [ ] T-547: Add LaTeXAgent node (right of Editor)
- [ ] T-548: Add arrows with file labels: "notes.md", "ch*.md", "*_edited.md"
- [ ] T-549: Add output node: PDF (right of LaTeX)
- [ ] T-550: Add ApiGatekeeper dashed box below all agents
- [ ] T-551: Add `Process.sequential` label above diagram
- [ ] T-552: Test: include diagram in ch01.tex stub and compile to verify no TikZ errors

### 10.5 Bibliography
- [ ] T-553: Create `latex/bib/references.bib`
- [ ] T-554: Add `LangChain2024` entry (GitHub, 2024)
- [ ] T-555: Add `CrewAI2024` entry (GitHub, 2024)
- [ ] T-556: Add `LangGraph2024` entry (GitHub, 2024)
- [ ] T-557: Add `RussellNorvig2020` book entry (AI: A Modern Approach, 4th ed)
- [ ] T-558: Add `AutoGPT2023` entry
- [ ] T-559: Add at least 3 more entries (papers, docs) to reach ≥8 total
- [ ] T-560: Verify all .bib entries have author, title, year, url fields

### 10.6 LaTeX Makefile & Build Script
- [ ] T-561: Create `latex/Makefile` with all target
- [ ] T-562: Implement 4-pass compile sequence in Makefile
- [ ] T-563: Add `clean` target removing .aux, .log, .toc, .bbl, .blg, .bcf, .xml
- [ ] T-564: Create `scripts/build_article.py` with Python-driven 4-pass compile
- [ ] T-565: Print progress: "[1/4] lualatex...", "[2/4] biber...", etc.
- [ ] T-566: Print final PDF size in KB on success
- [ ] T-567: Raise SystemExit on compile failure with last 2000 chars of stderr
- [ ] T-568: Test: compile the skeleton (stub chapters) — should produce PDF
- [ ] T-569: Verify `latex/output/main.pdf` exists after `uv run python scripts/build_article.py`
- [ ] T-570: Commit all LaTeX files and build script

---

## Phase 11: Integration Tests (T-571 – T-610)

### 11.1 conftest.py
- [ ] T-571: Write `mock_config` fixture — provides tmp_path config dir with all JSON files
- [ ] T-572: Write `mock_llm` fixture — patches `crewai.Agent` to return MagicMock
- [ ] T-573: Write `tmp_workspace` fixture — creates workspace/chapters/ in tmp_path
- [ ] T-574: Write `mock_gatekeeper` fixture — resets ApiGatekeeper._instance
- [ ] T-575: Commit `tests/conftest.py`

### 11.2 Integration: Crew Assembly
- [ ] T-576: Write `test_crew_kickoff_calls_all_4_agents` — mock all agents and Crew
- [ ] T-577: Write `test_crew_kickoff_passes_topic_to_tasks` — verify topic in task descriptions
- [ ] T-578: Write `test_crew_result_has_pdf_path` — verify CrewResult.pdf_path set
- [ ] T-579: Write `test_crew_sequential_process` — verify `Process.sequential` used
- [ ] T-580: Run integration crew tests — expect PASS
- [ ] T-581: Commit `tests/integration/test_article_crew.py`

### 11.3 Integration: LaTeX Pipeline
- [ ] T-582: Write `test_latex_compile_tool_subprocess_calls` — mock subprocess.run
- [ ] T-583: Write `test_latex_skeleton_compiles` — real lualatex, skip if not installed
- [ ] T-584: Write `test_chart_generator_produces_includable_png`
- [ ] T-585: Write `test_bib_file_has_minimum_5_entries` — parse references.bib
- [ ] T-586: Run integration LaTeX tests — expect PASS (or skip if no lualatex)
- [ ] T-587: Commit `tests/integration/test_latex_pipeline.py`

### 11.4 Coverage Check
- [ ] T-588: Run `uv run pytest tests/unit tests/integration --cov=src --cov-report=term-missing`
- [ ] T-589: Identify uncovered branches (look for lines marked as missed)
- [ ] T-590: Add tests for any critical uncovered path (error branches, edge cases)
- [ ] T-591: Re-run coverage — verify ≥85%
- [ ] T-592: If below 85%, add more unit tests targeting the lowest-coverage modules
- [ ] T-593: Run `uv run python scripts/check_file_lines.py` — verify all files ≤150 lines
- [ ] T-594: Run `uv run ruff check src tests scripts` — verify 0 errors
- [ ] T-595: Fix all ruff violations before proceeding
- [ ] T-596: Commit all test fixes

---

## Phase 12: Per-Mechanism PRDs (T-611 – T-630)

- [ ] T-611: Write `docs/PRD_crew_orchestrator.md` with Input/Output/Setup + all required sections
- [ ] T-612: Write `docs/PRD_researcher_agent.md`
- [ ] T-613: Write `docs/PRD_writer_agent.md`
- [ ] T-614: Write `docs/PRD_editor_agent.md`
- [ ] T-615: Write `docs/PRD_latex_agent.md`
- [ ] T-616: Write `docs/PRD_skill_layer.md`
- [ ] T-617: Write `docs/PRD_tools.md`
- [ ] T-618: Write `docs/PRD_gatekeeper.md`
- [ ] T-619: Write `docs/PRD_bibliography.md`
- [ ] T-620: Write `docs/PRD_chart_generator.md`
- [ ] T-621: Verify each PRD has: Input, Output, Setup, Responsibilities, Interface, Test strategy, Acceptance criteria
- [ ] T-622: Commit all per-mechanism PRDs

---

## Phase 12b: GAP FIX — ADR Files, Class Diagram, Static Image (T-T1 – T-T9)

> Added after PRD verification: these requirements were in PRD/PLAN but missing from TODO tasks.

- [ ] T-T1: Create `docs/diagrams/class_diagram.md` — copy class diagram from PLAN.md into dedicated file
- [ ] T-T2: Create `docs/ADRs/ADR-001-crewai-over-langgraph.md` — copy ADR-001 from PLAN.md
- [ ] T-T3: Create `docs/ADRs/ADR-002-sequential-over-hierarchical.md`
- [ ] T-T4: Create `docs/ADRs/ADR-003-markdown-first-workflow.md`
- [ ] T-T5: Create `docs/ADRs/ADR-004-lualatex-over-xelatex.md`
- [ ] T-T6: Create `docs/ADRs/ADR-005-single-llm-provider.md`
- [ ] T-T7: Create `docs/ADRs/ADR-006-file-based-skill-layer.md`
- [ ] T-T8: Create `docs/ADRs/ADR-007-duckduckgo-web-search.md`
- [ ] T-T9: Source or create static image `latex/figures/cover_logo.png` (H4 — image distinct from Python chart). Use matplotlib to generate a simple logo/icon PNG if no CC0 image available.
- [ ] T-T10: Commit ADR files, class diagram, and static image

---

## Phase 13: PROMPTS.md (T-623 – T-635)

- [ ] T-623: Create `docs/PROMPTS.md`
- [ ] T-624: Add Entry 001: Researcher agent role prompt
- [ ] T-625: Add Entry 002: Writer agent role prompt
- [ ] T-626: Add Entry 003: Editor agent role prompt
- [ ] T-627: Add Entry 004: LaTeX agent role with "fancy formula, not plain text"
- [ ] T-628: Add Entry 005-008: 4 agent goal prompts
- [ ] T-629: Add Entry 009-012: 4 agent backstory prompts
- [ ] T-630: Add Entry 013-016: 4 task description prompts
- [ ] T-631: Add Entry 017: BiDi chapter prompt
- [ ] T-632: Add Entry 018: TikZ diagram prompt
- [ ] T-633: Add Entry 019: Fancy formula enforcement prompt
- [ ] T-634: Add Entry 020-025: 6 coding prompts used during implementation
- [ ] T-635: Commit `docs/PROMPTS.md`

---

## Phase 14: Full E2E Run & PDF Validation (T-636 – T-645)

- [ ] T-636: Verify Claude CLI is logged in: `claude --version`
- [ ] T-637: Run `uv run agent-article` and press G
- [ ] T-638: Wait for ResearcherAgent to complete — verify `workspace/research_notes.md` exists
- [ ] T-639: Wait for WriterAgent — verify 6 `workspace/chapters/ch0N.md` files exist
- [ ] T-640: Wait for EditorAgent — verify 6 `workspace/chapters/ch0N_edited.md` files exist
- [ ] T-641: Approve Markdown at human checkpoint: type `y`
- [ ] T-642: Wait for LaTeXAgent — verify `latex/output/uoh-sqak-article.pdf` exists
- [ ] T-643: Open PDF — verify ≥15 pages, cover, TOC, all 6 chapters, bibliography
- [ ] T-644: Click a citation in the PDF — verify it jumps to bibliography
- [ ] T-645: Verify fancy formula is in Chapter 4 (not plain text)

---

## Phase 15: README & Final Docs (T-646 – T-650)

- [ ] T-646: Write `README.md` — full product manual (Quick Start, Install, Usage, Architecture, Config, Cost, Extend, Ethics, License)
- [ ] T-647: Add verbatim AI usage disclosure (Hebrew + English)
- [ ] T-648: Add link to `docs/PROMPTS.md` in README AI section
- [ ] T-649: Add sample PDF screenshot or link in README
- [ ] T-650: Run `uv run python scripts/check_file_lines.py` final check

---

## Phase 16: Submission (T-651 – T-660)

- [ ] T-651: Tag final commit: `git tag v1.00`
- [ ] T-652: Push to GitHub: `git push origin main --tags`
- [ ] T-653: Verify repo public (incognito browser)
- [ ] T-654: Count commits on main — must be ≥50
- [ ] T-655: Run `uv run python scripts/fill_submission_pdf.py` to generate `uoh-sqak-ex03.pdf`
- [ ] T-656: Verify submission PDF: exercise=03, group=uoh-sqak, self-grade=85, both names
- [ ] T-657: Upload `uoh-sqak-ex03.pdf` to Moodle id=270973 as Salah Qadah
- [ ] T-658: Upload `uoh-sqak-ex03.pdf` to Moodle id=270973 as Andalus Kalash (separate upload)
- [ ] T-659: Note submission timestamp (must be before Friday 12 June 2026, 23:59 Asia/Jerusalem)
- [ ] T-660: Report back to orchestrator: repo URL, PDF page count, coverage%, commit count, any open issues

---

## Phase 17: Fast Pipeline — Haiku + Parallel LaTeX (T-661 – T-710)

> Implementing PRD_fast_pipeline.md (FP-01). Goal: reduce wall-clock from ~70 min to ≤10 min.
> Strategy: Haiku model by default, Sonnet for ch05 only, parallel ThreadPoolExecutor for 7 LaTeX tasks.

### 17a — PRD & Docs (T-661 – T-664)
- [x] T-661: Create `docs/PRD_fast_pipeline.md` — Option C spec (Haiku + Parallel), Input/Output/Setup, Acceptance Criteria
- [ ] T-662: Add fast pipeline section to `docs/PLAN.md` (architecture diagram, threading model)
- [ ] T-663: Add FP-01 entries to PRD coverage checklist at bottom of this file
- [ ] T-664: Commit PRD, PLAN update, and this TODO batch: `feat(docs): add fast pipeline PRD and TODO tasks (FP-01)`

### 17b — Config: per-task model override (T-665 – T-669)
- [ ] T-665: Add `"default_model": "claude-haiku-4-5-20251001"` field to `config/setup.json`
- [ ] T-666: Add `"model"` field to each of the 7 latex task entries in `config/tasks.json` — haiku for ch01–ch04, ch06, bib; sonnet for ch05
- [ ] T-667: Add `"haiku_timeout_seconds": 300` and `"sonnet_timeout_seconds": 600` to `config/rate_limits.json`
- [ ] T-668: Update `shared/config.py` — expose `default_model`, `haiku_timeout`, `sonnet_timeout` properties
- [ ] T-669: Commit config changes: `feat(config): add per-task model override fields for fast pipeline`

### 17c — ClaudeCLILLM: model + timeout per-instance (T-670 – T-675)
- [ ] T-670: Write failing test `tests/unit/test_claude_cli_llm_model.py` — assert `ClaudeCLILLM(model="claude-haiku-4-5-20251001").model == "claude-haiku-4-5-20251001"`
- [ ] T-671: Run test to confirm it fails: `uv run pytest tests/unit/test_claude_cli_llm_model.py -v`
- [ ] T-672: Update `ClaudeCLILLM` — replace hardcoded model string with `model: str` field, default from config `default_model`; update `_build_cmd()` to pass `--model {self.model}`; keep timeout field driven by config
- [ ] T-673: Run test to confirm it passes
- [ ] T-674: Confirm `shared/claude_cli_llm.py` is still ≤ 150 lines: `awk 'NF && !/^[[:space:]]*#/' src/agent_article/shared/claude_cli_llm.py | wc -l`
- [ ] T-675: Commit: `feat(llm): per-instance model + timeout from config in ClaudeCLILLM`

### 17d — Tasks: per-task model-aware agent (T-676 – T-682)
- [ ] T-676: Write failing test `tests/unit/test_build_latex_tasks_model.py` — assert `build_latex_tasks(...)` produces Task whose agent uses haiku for ch01 and sonnet for ch05
- [ ] T-677: Run test to confirm it fails
- [ ] T-678: Update `build_latex_tasks()` in `tasks/article_tasks.py` — read `model` field from `config/tasks.json` per task; instantiate `ClaudeCLILLM(model=task_model)` and build a new `LaTeXAgent` instance for that task
- [ ] T-679: Run test to confirm it passes
- [ ] T-680: Confirm `article_tasks.py` is still ≤ 150 lines
- [ ] T-681: Run full ruff check: `uv run ruff check src/agent_article/tasks/article_tasks.py`
- [ ] T-682: Commit: `feat(tasks): per-task model override for LaTeX tasks`

### 17e — Crew: parallel LaTeX phase (T-683 – T-693)
- [ ] T-683: Write failing test `tests/unit/test_parallel_latex.py` — mock `ClaudeCLILLM.call()` to record call timestamps; run `_run_latex_phase_parallel([t1..t7])`; assert all 7 tasks were called and max(start_times) - min(start_times) < 5s (they ran concurrently)
- [ ] T-684: Run test to confirm it fails
- [ ] T-685: Add `_run_latex_phase_parallel(tasks: list[Task]) -> list[str]` to `crew/article_crew.py` — uses `concurrent.futures.ThreadPoolExecutor(max_workers=min(7, os.cpu_count()))` to call each task's agent synchronously in a thread; writes output to `task.output_file`; logs thread ID + task name at start and completion; returns list of output file paths
- [ ] T-686: Update `ArticleCrew.run()` — after sequential crew finishes editor task, call `_run_latex_phase_parallel(latex_tasks)` instead of including latex tasks in the CrewAI sequential process
- [ ] T-687: Run test to confirm it passes
- [ ] T-688: Confirm `article_crew.py` is still ≤ 150 lines; if not, extract helpers to `crew/_latex_parallel.py`
- [ ] T-689: Run ruff check on modified files: `uv run ruff check src/agent_article/crew/`
- [ ] T-690: Run full test suite: `uv run pytest tests/ -v`
- [ ] T-691: Commit: `feat(crew): parallel LaTeX task execution via ThreadPoolExecutor`

### 17f — Agent prompt quality rules (T-694 – T-700)
- [ ] T-694: Update all 6 `latex_ch*` task descriptions in `config/tasks.json` — prepend explicit rule block: (1) output ONLY LaTeX (first char must be `%` or `\`); (2) tables always use `p{Xcm}` column types; (3) no markdown fences; (4) no trailing prose after LaTeX content; (5) cite keys must exactly match the `[AuthorYear]` keys in `workspace/research_notes.md`
- [ ] T-695: Update `latex_bib` task description — add rule: generate `@misc`/`@article`/`@book` entries for EVERY `[AuthorYear]` key used in chapter files
- [ ] T-696: Update `latex/skills/latex_skill/SKILL.md` — add "LaTeX Agent Quality Checklist" section encoding the same rules as SKILL.md backstory injection
- [ ] T-697: Bump `config/tasks.json` version field to 1.03
- [ ] T-698: Commit: `feat(prompts): encode table/citation/output quality rules into agent task descriptions`

### 17g — Integration test + timing (T-701 – T-706)
- [ ] T-701: Write `tests/integration/test_fast_pipeline.py` — mock `ClaudeCLILLM.call()` to return minimal valid LaTeX; assert all 7 `.tex` files are written; assert bib file is written; assert PDF compile is called after
- [ ] T-702: Run integration test: `uv run pytest tests/integration/test_fast_pipeline.py -v`
- [ ] T-703: Run full test suite + coverage: `uv run pytest --cov=src/agent_article --cov-report=term-missing`
- [ ] T-704: Confirm coverage ≥ 85%
- [ ] T-705: Run ruff on entire src: `uv run ruff check src/`
- [ ] T-706: Commit: `test: integration test for parallel fast pipeline (FP-01)`

### 17h — Live timing run (T-707 – T-710)
- [ ] T-707: Delete stale generated files: `rm -f latex/chapters/*.tex latex/bib/references.bib latex/output/*.pdf workspace/research_notes.md workspace/chapters/*.md`
- [ ] T-708: Run timed end-to-end: `time printf "1\nMulti-Agent Orchestration Patterns in AI Systems\n" | uv run python -m agent_article.main 2>&1 | tee results/fast_pipeline_run.log`
- [ ] T-709: Verify wall-clock ≤ 10 min; verify PDF ≥ 15 pages; verify no `[AuthorYear]` bold keys in PDF
- [ ] T-710: Commit final result: `feat(pipeline): FP-01 complete — parallel Haiku pipeline ≤10 min`

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
