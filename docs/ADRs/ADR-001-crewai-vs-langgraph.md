# ADR-001: CrewAI over LangGraph for Agent Orchestration

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

HW3 requires a multi-agent pipeline with at least four specialized agents (Researcher, Writer, Editor, LaTeX Producer) executing in a defined order. Two viable orchestration frameworks were evaluated: **CrewAI** and **LangGraph**.

The pipeline is linear (sequential hand-off of artifacts) with optional human checkpoints. Agents need distinct identities (role, goal, backstory) and file-based Skill augmentation. The grading rubric explicitly names CrewAI in lecture materials and the spec PDF, and Dr. Segal demonstrated CrewAI syntax in Lecture 6.

---

## Decision

Use **CrewAI** (`crewai>=0.28`) with `Process.sequential` as the orchestration framework.

---

## Alternatives Considered

| Framework | Notes |
|---|---|
| **LangGraph** | Graph-based state machine; excellent for conditional branching and cycles. Overkill for a linear pipeline. Requires explicit edge definition between every node. No native role/goal/backstory concept. |
| **AutoGen** | Conversation-centric; suited for debate-style multi-agent setups. Less clean separation of agent responsibilities. Not referenced in course materials. |
| **Raw LangChain** | Would require hand-rolling agent coordination, memory hand-off, and tool routing. High boilerplate with no added benefit for this workload. |

---

## Rationale

1. **Course alignment**: Dr. Segal covered CrewAI Parts A+B explicitly in Lecture 6 PDF materials. Using the lectured technology maximises alignment with grader expectations.
2. **Agent identity semantics**: CrewAI's `role`/`goal`/`backstory` triple maps directly to the Skills layer design — backstory is the natural injection point for `SKILL.md` content.
3. **Sequential process**: `Process.sequential` matches the data-flow exactly: research notes → chapters → edited chapters → LaTeX. No graph-building overhead.
4. **Tool integration**: CrewAI tools map 1:1 to `BaseTool` subclasses; the Gatekeeper wraps each tool call transparently.
5. **Ecosystem**: `crewai` ships with built-in LLM provider abstraction, allowing per-agent model assignment via config — matches our multi-provider bonus objective.

---

## Consequences

- **Positive**: Clean agent definitions in `config/agents.json`; `Process.sequential` eliminates complex routing logic; native task context passing between agents.
- **Negative**: Less flexible for non-linear flows. If a future iteration needs cycles (e.g., editor sends chapters back to writer), we would need to switch to `Process.hierarchical` or introduce a manager agent.
- **Mitigation**: The `ArticleCrew` class is isolated in `crew/article_crew.py`; swapping the process type is a one-line config change.
