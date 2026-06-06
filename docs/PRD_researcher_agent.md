# PRD: ResearcherAgent

**Component**: `src/agent_article/agents/researcher_agent.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`ResearcherAgent` is the first agent in the sequential CrewAI pipeline. Given the article
topic, it searches the web for relevant sources, organises the findings into structured
research notes, and writes them to `workspace/research_notes.md`. All web search calls are
routed through `ApiGatekeeper`. The agent is given domain expertise via
`skills/researcher_skill/SKILL.md`.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `topic` | `str` | Article topic string injected by Crew at task start |
| **Input** `chapter_outline` | `list[str]` | Planned chapter titles from `config/tasks.json` |
| **Input** `skill_path` | `Path` | Resolved path to `skills/researcher_skill/SKILL.md` |
| **Input** `max_search_queries` | `int` | Upper bound on web searches; read from `config/agents.json` |
| **Output** `research_notes.md` | `str` | Markdown file written to `workspace/research_notes.md` |
| **Output** `sources_list` | `list[dict]` | List of `{title, url, snippet, relevance_score}` dicts |

---

## Functional Requirements

1. **FR-RA-01**: Load `role`, `goal`, and `backstory` from `config/agents.json::agents.researcher`;
   none of these strings may appear in source code. Raise `ConfigError` on missing key.

2. **FR-RA-02**: Equip the CrewAI agent with `WebSearchTool` and `FileWriteTool`. Tool
   instances are created via the shared tool registry; `WebSearchTool` wraps DuckDuckGo search
   through `ApiGatekeeper`.

3. **FR-RA-03**: For each planned chapter title, issue at least one targeted web search query
   and collect ≥ 2 distinct sources. Deduplicate by URL before writing notes.

4. **FR-RA-04**: Write `workspace/research_notes.md` in this structure:
   ```
   # Research Notes — {topic}
   ## Chapter: {chapter_title}
   ### Source {n}: {title}
   - URL: {url}
   - Key points: …
   ```
   This exact schema is what `WriterAgent` reads; any deviation breaks the pipeline.

5. **FR-RA-05**: Respect `max_search_queries` from config; stop issuing searches once the
   limit is reached and note `[SEARCH_LIMIT_REACHED]` in the notes file.

6. **FR-RA-06**: Each source entry must include at least one quoted sentence or factual claim
   that can be used as the basis for a `[AuthorYear]`-style in-text citation by the Writer.

7. **FR-RA-07**: Log each web search call as a structured JSON line to the FIFO log
   (`{"event": "web_search", "query": "…", "hits": N, "agent": "researcher"}`).

---

## Non-Functional Requirements

- **NFR-RA-01 Latency**: Each individual web search call must complete within 10 seconds;
  implement a timeout wrapper in `WebSearchTool`.
- **NFR-RA-02 Resilience**: If a search returns 0 results or raises a network error, log a
  warning and continue with remaining queries rather than aborting the task.
- **NFR-RA-03 Portability**: No API key is required for DuckDuckGo fallback; optional
  `BRAVE_SEARCH_API_KEY` in `.env` upgrades the provider without code changes.

---

## Setup / Configuration

| Key | File / Env | Description |
|---|---|---|
| `agents.researcher.role` | `config/agents.json` | CrewAI `role` string |
| `agents.researcher.goal` | `config/agents.json` | CrewAI `goal` string |
| `agents.researcher.backstory` | `config/agents.json` | CrewAI `backstory` string |
| `agents.researcher.llm` | `config/agents.json` | LLM model key (e.g. `"claude-sonnet"`) |
| `agents.researcher.max_search_queries` | `config/agents.json` | Integer cap on searches |
| `agents.researcher.skill_ref` | `config/agents.json` | Relative path to `SKILL.md` |
| `BRAVE_SEARCH_API_KEY` | `.env` (optional) | Upgrades web search from DDG to Brave |

---

## Acceptance Criteria

- [ ] With `MockLLM` and `MockSearchTool`, `ResearcherAgent` produces a non-empty
      `workspace/research_notes.md` containing at least one `## Chapter:` heading.
- [ ] When `max_search_queries` is set to 1 in config, exactly 1 `web_search` event appears in
      the structured log.
- [ ] Network error in `WebSearchTool` triggers a warning log entry and does not raise an
      unhandled exception.
- [ ] The notes file schema matches the expected format (regex test on section headings).
- [ ] `ruff check` returns 0; file has ≤ 150 logical lines.
