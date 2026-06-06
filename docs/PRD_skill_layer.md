# PRD: Skill Layer

**Component**: `src/agent_article/skills/` + `src/agent_article/shared/base_skill.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

The Skill layer provides each CrewAI agent with a file-based "onboarding packet" — the
procedure manuals, checklists, and domain knowledge the agent needs beyond its raw LLM
capability. It is conceptually distinct from Tools: a **Tool** is an action capability (web
search, file write); a **Skill** is instructional context (how to evaluate a source, how to
structure a citation, how to emit BiDi-safe LaTeX). Skills are defined by `SKILL.md` files
with YAML frontmatter and are loaded by `BaseSkill` at agent instantiation.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `skill_dir` | `Path` | Root directory of the skill, e.g. `skills/researcher_skill/` |
| **Input** `skill_md_path` | `Path` | `SKILL.md` inside `skill_dir`; must exist |
| **Output** `skill_content` | `str` | Full rendered Markdown body (frontmatter stripped) |
| **Output** `skill_meta` | `dict` | Parsed YAML frontmatter (`name`, `description`, optional fields) |
| **Output** `injected_context` | `str` | String inserted into agent's `backstory` or task context |

---

## Functional Requirements

1. **FR-SK-01**: Define `BaseSkill(ABC)` in `src/agent_article/shared/base_skill.py`.
   It must expose:
   - `load() -> None` — parses `SKILL.md`, splits YAML frontmatter from Markdown body.
   - `get_content() -> str` — returns the Markdown body for LLM context injection.
   - `get_meta() -> dict` — returns the parsed frontmatter dict.
   - Abstract property `skill_name: str` — concrete subclasses provide the display name.

2. **FR-SK-02**: Implement four concrete skill classes, one per agent role:
   - `ResearcherSkill(BaseSkill)` at `skills/researcher_skill/`
   - `WriterSkill(BaseSkill)` at `skills/writer_skill/`
   - `EditorSkill(BaseSkill)` at `skills/editor_skill/`
   - `LaTeXSkill(BaseSkill)` at `skills/latex_skill/`
   Each class adds no logic beyond overriding `skill_name` and any role-specific
   helper that parses files in the skill's `references/` subdirectory.

3. **FR-SK-03**: Each `SKILL.md` must follow this schema:
   ```markdown
   ---
   name: <skill-name>
   description: <one-sentence description>
   version: "1.00"
   ---
   # <Skill Title>
   <Markdown body — instructions, checklists, examples>
   ```
   The `version` key must be present so the `SkillRegistry` can detect stale skills.

4. **FR-SK-04**: Implement `SkillRegistry` as a module-level singleton dict that maps
   agent role keys (e.g. `"researcher"`) to their `BaseSkill` subclass. Registering a new
   skill requires only adding a directory under `skills/` and adding one entry to the registry
   dict — no changes to existing agent files.

5. **FR-SK-05**: `BaseSkill.load()` must raise `SkillLoadError` (a custom exception in
   `shared/exceptions.py`) if `SKILL.md` is missing, the YAML frontmatter is malformed,
   or the required `name`/`description`/`version` keys are absent.

6. **FR-SK-06**: Each skill directory may contain a `references/` subdirectory with supporting
   Markdown files (style guides, glossaries, citation format examples). These are loaded
   lazily by `BaseSkill.get_reference(filename: str) -> str` when the agent or task needs them.

---

## Non-Functional Requirements

- **NFR-SK-01 Extensibility**: Adding a fifth agent skill requires only: create
  `skills/new_skill/SKILL.md`, subclass `BaseSkill`, register in `SkillRegistry`. Zero
  changes to existing skills or agents.
- **NFR-SK-02 Testability**: `BaseSkill` must accept a `skill_dir: Path` constructor argument
  so tests can point it at a temporary directory with fixture `SKILL.md` files.
- **NFR-SK-03 Separation of Concerns**: Skills contain no executable Python logic beyond
  parsing their own `SKILL.md`. Business logic stays in agents; domain knowledge stays in
  `SKILL.md` files.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `agents.*.skill_ref` | `config/agents.json` | Relative path from `src/` to the skill directory |
| `skill.version` | Each `SKILL.md` frontmatter | Must match `"1.00"` at project launch |

No environment variables are used by the Skill layer.

---

## SKILL.md Files Required

| File | Path | Contents summary |
|---|---|---|
| `researcher_skill/SKILL.md` | `skills/researcher_skill/` | Source evaluation checklist, reference format, search strategy |
| `writer_skill/SKILL.md` | `skills/writer_skill/` | Style guide, tone instructions, citation embedding rules |
| `editor_skill/SKILL.md` | `skills/editor_skill/` | Grammar checklist, formula-marker rules, BiDi validation steps |
| `latex_skill/SKILL.md` | `skills/latex_skill/` | LaTeX/BiDi recipe, biblatex pattern, formula → equation mapping |

---

## Acceptance Criteria

- [ ] `BaseSkill.load()` successfully parses a well-formed `SKILL.md` fixture and returns
      correct `name`, `description`, and `version` from frontmatter.
- [ ] `BaseSkill.load()` raises `SkillLoadError` when `SKILL.md` is missing.
- [ ] `SkillRegistry["researcher"]` returns the `ResearcherSkill` class (not an instance).
- [ ] All four `SKILL.md` files exist, are valid YAML-frontmatter Markdown, and contain
      a `version: "1.00"` key.
- [ ] `ruff check` returns 0 on all files in `src/agent_article/skills/` and
      `src/agent_article/shared/base_skill.py`.
- [ ] Each skill file has ≤ 150 logical lines.
