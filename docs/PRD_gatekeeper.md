# PRD: ApiGatekeeper

**Component**: `src/agent_article/shared/gatekeeper.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`ApiGatekeeper` is a singleton class that mediates every external API call made by the
system: LLM calls (Claude via LangChain-Anthropic), web search (DuckDuckGo/Brave), LaTeX
subprocess invocations, and file-write accounting. It enforces rate limits, token budgets,
and daily quotas defined in `config/rate_limits.json`, and implements exponential backoff
with jitter for retryable failures. No external call may bypass the Gatekeeper — this is
rubric rule R3.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `service` | `str` | Service key matching a key in `rate_limits.json::services` |
| **Input** `call_fn` | `Callable[..., T]` | The actual I/O function to invoke |
| **Input** `*args, **kwargs` | `Any` | Forwarded to `call_fn` |
| **Input** `token_count` | `int` (optional) | Pre-estimated tokens; used for budget tracking |
| **Output** | `T` | Return value of `call_fn`, unchanged |
| **Side-effect** | Log entry | Structured JSON log written via `logging_fifo.py` |

---

## Functional Requirements

1. **FR-GK-01**: Implement `ApiGatekeeper` as a singleton using the `__new__` pattern.
   `ApiGatekeeper.get_instance()` always returns the same object; tests can reset state via
   `ApiGatekeeper._reset_for_testing()` (a test-only method, guarded by an assertion that
   checks `os.environ.get("PYTEST_CURRENT_TEST")`).

2. **FR-GK-02**: Load all rate limit and token budget values from
   `config/rate_limits.json` at first instantiation. Keys read:
   - `services.{service}.requests_per_minute` — sliding-window counter
   - `services.{service}.tokens_per_article` — cumulative token cap per article run
   - `services.{service}.tokens_per_day` — cumulative daily cap
   - `services.{service}.warn_at_percent` — log a WARNING when usage crosses this %
   - `services.{service}.hard_cap_percent` — raise `BudgetExceededError` when reached
   No numeric value may be hardcoded in `gatekeeper.py`.

3. **FR-GK-03**: Implement a per-service sliding-window rate limiter. When a request would
   exceed `requests_per_minute`, block (sleep) until the window clears. Maximum sleep is
   bounded by `config/rate_limits.json::services.{service}.max_wait_seconds`; if exceeded,
   raise `RateLimitError`.

4. **FR-GK-04**: Implement exponential backoff with jitter for HTTP 429 / 503 / transient
   network errors. Retry formula: `sleep(min(base * 2^attempt + jitter, max_wait))`.
   Base, maximum, and jitter range are read from `rate_limits.json`. Maximum retries are
   configurable per service.

5. **FR-GK-05**: Track token usage per service per article run and per calendar day.
   After each LLM call, read the `usage` object from the LangChain response metadata and
   add `prompt_tokens + completion_tokens` to the running counters. Log a structured
   `{"event": "token_usage", "service": …, "tokens": …, "cumulative": …}` line.

6. **FR-GK-06**: When cumulative token usage crosses `warn_at_percent` of the budget, emit a
   `logging.WARNING`. When it crosses `hard_cap_percent`, raise `BudgetExceededError` with a
   message that includes the service name, current usage, and the configured cap — without
   exposing any secret keys in the message.

7. **FR-GK-07**: Expose a `cost_report() -> dict` method that returns a summary of tokens
   used and estimated cost per service for the current article run. The cost estimate
   uses `price_input_per_million_tokens` and `price_output_per_million_tokens` from
   `rate_limits.json`. The SDK layer writes this to `results/cost_report.json` at end of run.

---

## Non-Functional Requirements

- **NFR-GK-01 Thread Safety**: All counter mutations use `threading.Lock`. The Gatekeeper is
  safe for concurrent tool calls (even if `Process.sequential` rarely triggers concurrency).
- **NFR-GK-02 Transparency**: Every call that the Gatekeeper mediates produces a structured
  log line with at minimum: `event`, `service`, `timestamp_iso`, `latency_ms`, `success`.
  Failed calls additionally log `error_type` and `retry_attempt`.
- **NFR-GK-03 Zero Secrets**: The Gatekeeper never logs, prints, or stores API key values.
  Keys are read from `os.environ.get(…)` by the LangChain provider; the Gatekeeper receives
  only the callable, not the key itself.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `services.claude_sonnet.*` | `config/rate_limits.json` | Claude rate limits + token budgets |
| `services.web_search.*` | `config/rate_limits.json` | Web search rate limits |
| `services.latex_compile.*` | `config/rate_limits.json` | LaTeX subprocess limits |
| `services.*.max_retries` | `config/rate_limits.json` | Max retry attempts per service |
| `services.*.backoff_base_seconds` | `config/rate_limits.json` | Exponential backoff base |
| `ANTHROPIC_API_KEY` | `.env` | Passed to LangChain; never read by Gatekeeper directly |

---

## Acceptance Criteria

- [ ] `ApiGatekeeper.get_instance()` called twice returns the same object (`is` check).
- [ ] When `MockLLM` returns a response with `usage.total_tokens = 100`, the Gatekeeper's
      cumulative counter increments by exactly 100.
- [ ] When cumulative tokens exceed `warn_at_percent` of the budget, a `logging.WARNING` is
      emitted (captured via `caplog` in pytest).
- [ ] When cumulative tokens exceed `hard_cap_percent`, `BudgetExceededError` is raised.
- [ ] When `call_fn` raises an HTTP 429 error, the Gatekeeper retries up to `max_retries`
      times before re-raising `RateLimitError`.
- [ ] `cost_report()` returns a dict with `"total_estimated_cost_usd"` key (float).
- [ ] `ruff check` returns 0; file has ≤ 150 logical lines.
