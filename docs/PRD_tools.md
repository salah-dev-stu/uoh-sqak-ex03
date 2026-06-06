# PRD: Tools Layer

**Component**: `src/agent_article/tools/`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

The Tools layer provides all action capabilities used by CrewAI agents. Each tool is a
subclass of `BaseTool(ABC)` and is registered in `ToolRegistry`. All tools that make
external calls (web search, LaTeX compile, subprocess) route through `ApiGatekeeper`.
File I/O tools use `pathlib.Path` exclusively. The five concrete tools are:
`WebSearchTool`, `FileReadTool`, `FileWriteTool`, `ChartGeneratorTool`, and
`LaTeXCompileTool`.

---

## Inputs / Outputs

| Tool | Input | Output |
|---|---|---|
| `WebSearchTool` | `query: str`, `max_results: int` | `list[SearchResult]` (title, url, snippet) |
| `FileReadTool` | `path: Path` | `str` — file contents |
| `FileWriteTool` | `path: Path`, `content: str` | `None`; raises on permission error |
| `ChartGeneratorTool` | `script_path: Path`, `output_path: Path` | `Path` to generated PNG |
| `LaTeXCompileTool` | `tex_dir: Path`, `passes: list[str]` | `CompileResult` (exit_code, stdout, stderr) |

---

## Functional Requirements

1. **FR-TL-01**: Define `BaseTool(ABC)` in `src/agent_article/tools/__init__.py`. It must
   expose:
   - Abstract method `run(*args, **kwargs)` — the tool's primary action.
   - `name: str` — class-level attribute; used by `ToolRegistry` and CrewAI tool binding.
   - `description: str` — class-level attribute; shown to the LLM as tool description.
   All concrete tools inherit from `BaseTool` and from CrewAI's `BaseTool` via multiple
   inheritance so they are compatible with the CrewAI agent tool-calling interface.

2. **FR-TL-02** (`WebSearchTool`): Wrap DuckDuckGo search (via the `duckduckgo-search`
   library) as the default provider. If `BRAVE_SEARCH_API_KEY` is set in the environment,
   switch to the Brave Search API without code changes. Route every search call through
   `ApiGatekeeper.call(service="web_search", …)`.

3. **FR-TL-03** (`FileReadTool`): Read a file at the given `Path` and return its contents as a
   UTF-8 string. Raise `FileNotFoundError` (not a silent empty string) if the path does not
   exist. Constrain reads to within the project root (deny path-traversal outside `hw3/`).

4. **FR-TL-04** (`FileWriteTool`): Write `content` to `path`; create intermediate directories
   via `path.parent.mkdir(parents=True, exist_ok=True)`. Overwrite if file exists. All writes
   are routed through `ApiGatekeeper.call(service="file_write", …)` for rate accounting.

5. **FR-TL-05** (`ChartGeneratorTool`): Execute `script_path` via `uv run python {script_path}`
   in a subprocess. Capture stdout/stderr; raise `ChartGenerationError` if exit code != 0.
   Verify that `output_path` was created after execution. Do not use `exec()` or `eval()`.

6. **FR-TL-06** (`LaTeXCompileTool`): Run the compile passes specified in `passes`
   (e.g. `["lualatex main.tex", "biber main", "lualatex main.tex", "lualatex main.tex"]`)
   as subprocesses with `cwd=tex_dir`. Raise `CompilationError` on any non-zero exit code,
   including the stderr text so the error message is actionable.

7. **FR-TL-07**: Implement `ToolRegistry` as a module-level dict mapping tool names to tool
   classes. The `ArticleCrew` and agent factories look up tools from the registry. Adding a
   new tool requires only subclassing `BaseTool` and registering — no changes to existing
   agents.

---

## Non-Functional Requirements

- **NFR-TL-01 Isolation**: Each tool runs statelessly; it must not store results in instance
  variables between calls. Results are returned and passed explicitly by CrewAI's task context.
- **NFR-TL-02 Timeout**: `WebSearchTool`, `ChartGeneratorTool`, and `LaTeXCompileTool` all
  enforce a per-call timeout (read from `config/rate_limits.json::services.*.timeout_seconds`).
  Exceeding the timeout raises `ToolTimeoutError`.
- **NFR-TL-03 Security**: `ChartGeneratorTool` and `LaTeXCompileTool` may only execute scripts
  and binaries from an allowlist in `config/setup.json::allowed_executables`. Any unlisted
  executable raises `SecurityError` before subprocess creation.

---

## Setup / Configuration

| Key | File / Env | Description |
|---|---|---|
| `services.web_search.timeout_seconds` | `config/rate_limits.json` | Per-search timeout |
| `services.latex_compile.timeout_seconds` | `config/rate_limits.json` | Per-pass compile timeout |
| `setup.allowed_executables` | `config/setup.json` | Allowlist for subprocess execution |
| `BRAVE_SEARCH_API_KEY` | `.env` (optional) | Upgrades WebSearchTool to Brave |

---

## Acceptance Criteria

- [ ] `WebSearchTool.run("test query", max_results=3)` with `MockSearchProvider` returns a
      `list` of length ≤ 3, each item having `title`, `url`, `snippet` keys.
- [ ] `FileReadTool.run(path=Path("/nonexistent"))` raises `FileNotFoundError`.
- [ ] `FileWriteTool.run(path=tmp_path/"sub/file.txt", content="x")` creates intermediate
      directory and writes content (pytest `tmp_path` fixture).
- [ ] `ChartGeneratorTool.run(script_path=…, output_path=…)` with a failing script raises
      `ChartGenerationError` containing the subprocess stderr.
- [ ] `LaTeXCompileTool.run(…)` with `MockSubprocess(exit_code=1)` raises `CompilationError`.
- [ ] `ToolRegistry` contains all five tool names at import time.
- [ ] `ruff check` returns 0; each tool file has ≤ 150 logical lines.
