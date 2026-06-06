# ADR-006: File-Based Skill Layer (SKILL.md Injected into Agent Backstory)

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

The HW3 spec (H20) requires a "Skills layer" where each CrewAI agent is augmented by a `SKILL.md` file and associated references. The rubric audits for this in the repo structure. The design question is: how should skill content reach the agent at runtime?

---

## Decision

Each agent skill lives in a dedicated directory (`skills/<agent>_skill/`) containing a `SKILL.md` file and optional `references/` subdirectory. At agent construction time, `FileSkill.load()` reads the `SKILL.md` content and appends it to the agent's `backstory` string.

---

## Alternatives Considered

| Approach | Notes | Rejected Reason |
|---|---|---|
| Hardcoded backstory strings | Simplest; everything in `agents.json` | Not extensible; no skill versioning; fails H20 repo audit |
| Database-backed skills | Skills stored in SQLite/JSON-DB | Overcomplicated for 4 agents; no clear benefit |
| Vector-store RAG injection | Embed SKILL.md; retrieve relevant chunks per query | Interesting but adds embedding API dependency; over-engineered for fixed-domain agents |
| File-based (chosen) | `SKILL.md` → `FileSkill.load()` → appended to backstory | Simple, auditable, versionable in git, meets H20 |

---

## Structure

```
skills/
├── researcher_skill/
│   ├── SKILL.md           ← domain knowledge + research methodology guidelines
│   └── references/        ← example .bib entries, citation format guide
├── writer_skill/
│   ├── SKILL.md           ← chapter structure templates, tone guidelines
│   └── references/
├── editor_skill/
│   ├── SKILL.md           ← house style guide, consistency rules
│   └── references/
└── latex_skill/
    ├── SKILL.md           ← LaTeX cookbook: equation envs, BiDi directives, biblatex syntax
    └── references/        ← minimal working examples for BiDi, TikZ, tabularx
```

## Runtime Injection

```python
class FileSkill(BaseSkill):
    def load(self) -> str:
        return (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")

# In AgentFactory:
skill_content = FileSkill(skill_ref).load()
backstory = f"{base_backstory}\n\n## Domain Expertise\n{skill_content}"
```

---

## Rationale

1. **H20 compliance**: The grader audits the repo for `SKILL.md` files. File-based approach makes compliance visible.
2. **Git versioning**: Skill content evolves independently of code. Commits to `SKILL.md` are meaningful and auditable.
3. **Separation of expertise from orchestration**: Agent coordination logic (`article_crew.py`) is independent of domain knowledge (`SKILL.md`). Swapping domain expertise does not require code changes.
4. **Extensibility**: New agents can be added by creating a new `<name>_skill/` directory and registering in `config/agents.json`. No Python changes required.

---

## Consequences

- **Positive**: Clear H20 compliance; skill content is human-readable and editable without touching Python.
- **Positive**: `FileSkill` is unit-testable independently of the LLM.
- **Negative**: Backstory strings grow longer (SKILL.md content is injected). Monitor that combined backstory + task description stays within LLM context window. For claude-sonnet-4-x this is not a concern (200k token context).
