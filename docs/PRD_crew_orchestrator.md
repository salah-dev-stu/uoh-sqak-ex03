# PRD: ArticleCrew Orchestrator

**Component**: `src/agent_article/crew/article_crew.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`ArticleCrew` is the top-level CrewAI `Crew` object that assembles the four specialist agents
(Researcher, Writer, Editor, LaTeXAgent) into a `Process.sequential` pipeline, wires their
tasks in order, and kicks off article generation. It reads all configuration from
`config/crew.json` and `config/agents.json` so that no values are hardcoded in source.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `topic` | `str` | Article topic passed by SDK at kickoff |
| **Input** `config_dir` | `Path` | Path to `config/` directory (injected by SDK) |
| **Input** `workspace_dir` | `Path` | Root output workspace (`workspace/`) for all agent artefacts |
| **Output** `kickoff_result` | `CrewOutput` | CrewAI `CrewOutput` object; `.raw` holds final LaTeX source |
| **Output** `artefact_paths` | `dict[str, Path]` | Map of `{"research_notes": …, "chapter_*.md": …, "main.tex": …}` |

---

## Functional Requirements

1. **FR-CO-01**: Load `config/crew.json` at instantiation; read process type (`sequential`),
   agent order list, task list, and verbose flag. Raise `ConfigError` if `"version"` key is absent.

2. **FR-CO-02**: Instantiate all four agents via their factory functions; each factory reads
   `config/agents.json` and injects the agent's `role`, `goal`, `backstory`, `llm`, and
   `skill_ref` from config — none of these strings may be hardcoded.

3. **FR-CO-03**: Build a `Task` list using templates from `config/tasks.json`; bind each task
   to its designated agent. The task list order defines the sequential pipeline:
   `[research_task → write_task → edit_task → latex_task]`.

4. **FR-CO-04**: Expose a single public method `kickoff(topic: str) -> CrewOutput` that wraps
   `Crew.kickoff(inputs={"topic": topic})`. All LLM calls within the Crew pass through
   `ApiGatekeeper` (injected via `CrewCallbacks`).

5. **FR-CO-05**: Emit structured log events at `INFO` level before and after crew kickoff, and
   at `DEBUG` level for each task completion. Use `logging_fifo.py` for the FIFO queue writer.

6. **FR-CO-06**: Support a dry-run mode (`dry_run: bool` in `config/crew.json`). When true,
   skip real LLM calls; return fixture artefacts from `tests/fixtures/`. Used in CI.

7. **FR-CO-07**: Expose lifecycle hooks `before_crew_kickoff`, `after_crew_kickoff`,
   `before_task`, `after_task` via a `CrewHooks` dataclass. Any callable registered there is
   invoked; the SDK layer uses this for token-cost accumulation.

---

## Non-Functional Requirements

- **NFR-CO-01 Performance**: Total crew kickoff (4 agents, 5 chapters) must complete within
  30 minutes wall-clock for a standard article; individual task timeouts configurable in
  `config/crew.json::task_timeout_seconds`.
- **NFR-CO-02 Maintainability**: Adding a fifth agent requires only a new entry in
  `config/agents.json` and `config/crew.json::agent_order` — no changes to `article_crew.py`.
- **NFR-CO-03 Testability**: `ArticleCrew` accepts injected `agent_factory` and
  `task_factory` callables so unit tests can substitute mocks without monkey-patching.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `crew.process` | `config/crew.json` | `"sequential"` or `"hierarchical"` |
| `crew.agent_order` | `config/crew.json` | Ordered list of agent keys matching `agents.json` |
| `crew.verbose` | `config/crew.json` | Boolean; enables CrewAI verbose output |
| `crew.dry_run` | `config/crew.json` | Boolean; bypasses LLM for CI |
| `crew.task_timeout_seconds` | `config/crew.json` | Per-task timeout; default 600 |
| `agents.*` | `config/agents.json` | Per-agent `role`, `goal`, `backstory`, `llm`, `skill_ref` |

No environment variables are read directly by this module; secrets flow through `ApiGatekeeper`.

---

## Acceptance Criteria

- [ ] `ArticleCrew().kickoff(topic="test")` runs end-to-end with `MockLLM` and produces a
      non-empty `CrewOutput.raw` string.
- [ ] Changing `crew.agent_order` in `config/crew.json` reorders tasks without code changes.
- [ ] `dry_run: true` in config causes `kickoff()` to return fixture content without any
      real LLM calls (verified by asserting `ApiGatekeeper.call_count == 0`).
- [ ] All four lifecycle hooks fire in the correct order (verified by a test that appends to a
      list inside each hook and checks ordering).
- [ ] `ruff check src/agent_article/crew/article_crew.py` returns 0 errors.
- [ ] File has ≤ 150 logical lines (comments + blanks excluded).
