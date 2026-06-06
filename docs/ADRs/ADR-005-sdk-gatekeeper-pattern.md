# ADR-005: SDK as Single Entry Point + ApiGatekeeper Singleton

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

The grading rubric has two structural hard rules that interact:
- **R1**: All business logic must flow through an SDK layer (single public surface).
- **R3**: All external API calls (LLMs, web search, LaTeX subprocess) must pass through a `Gatekeeper` class.

These are architectural constraints, not suggestions. Violations are caught by automated code review.

---

## Decision

1. `ArticleSDK` (in `sdk/sdk.py`) is the **sole public interface** of the `agent_article` package. All callers (TUI, tests, CLI) import and call `ArticleSDK` only.
2. `ApiGatekeeper` (in `shared/gatekeeper.py`) is a **singleton** that intercepts every external call: LLM invocations via LangChain/CrewAI, DuckDuckGo search requests, `subprocess.run(lualatex)` calls.

---

## Design

```
ArticleSDK.generate_article(topic)
    └── ArticleCrew.kickoff(topic)
            └── ResearcherAgent.execute_task()
                    └── WebSearchTool.run(query)
                            └── ApiGatekeeper.call(provider="duckduckgo", ...)
                                    └── DuckDuckGoSearchRun(query)
```

`ApiGatekeeper` exposes a single method:
```python
def call(self, provider: str, payload: dict) -> dict:
    ...  # rate-limit check, token budget check, log, dispatch, log response
```

All tool `_run()` methods call `ApiGatekeeper.get_instance().call(...)` rather than making external calls directly. This means:
- Rate limits and token budgets (from `config/rate_limits.json`) are enforced in one place.
- Every external call is logged with timestamp, provider, token count, and latency.
- Tests can swap the Gatekeeper for a mock without patching individual tools.

---

## Rationale

1. **Rubric compliance**: R1 and R3 are explicit code-review audit gates. Non-compliance costs points regardless of functionality.
2. **Testability**: `ApiGatekeeper` can be replaced with `MockGatekeeper` in tests via `ApiGatekeeper._instance = MockGatekeeper()`. No monkeypatching of network calls required.
3. **Rate limit enforcement**: All per-provider limits live in `config/rate_limits.json`. Gatekeeper raises `RateLimitError` before the external call, preventing wasted API spend.
4. **Observability**: `StructuredLogger` receives every Gatekeeper event. The log file `results/run_*.jsonl` records every LLM call with token counts — useful for cost analysis.

---

## Consequences

- **Positive**: Single enforcement point for security, rate limits, logging, and error handling.
- **Positive**: `ArticleSDK` public API is narrow and stable — changing internal orchestration does not break callers.
- **Negative**: Slight indirection overhead. Acceptable; these are IO-bound calls where network latency dominates.
- **Singleton caveat**: Tests must call `ApiGatekeeper.reset()` in `teardown` to avoid state leakage between test cases. `conftest.py` handles this via a session-scoped fixture.
