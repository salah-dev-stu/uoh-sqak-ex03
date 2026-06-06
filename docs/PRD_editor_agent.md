# PRD: EditorAgent

**Component**: `src/agent_article/agents/editor_agent.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`EditorAgent` is the third agent in the sequential pipeline. It reads all chapter Markdown
files from `workspace/chapters/`, performs prose editing, validates that every
`[AuthorYear]` citation marker has a matching entry in `latex/bib/references.bib`, and
resolves `[NEEDS_FORMULA]` markers into actual LaTeX formula stubs. Edited chapters are
written back to `workspace/chapters_edited/`. The agent uses
`skills/editor_skill/SKILL.md` for style and grammar guidelines.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `chapters_dir` | `Path` | `workspace/chapters/` — raw Markdown from WriterAgent |
| **Input** `bib_path` | `Path` | `latex/bib/references.bib` — validated citation keys |
| **Input** `skill_path` | `Path` | Path to `skills/editor_skill/SKILL.md` |
| **Input** `style_rules` | `dict` | Style parameters loaded from `config/agents.json` |
| **Output** `chapters_edited/` | `Path` | Edited Markdown files, one per chapter |
| **Output** `edit_report.md` | `str` | Summary of changes, unresolved markers, and citation gaps |

---

## Functional Requirements

1. **FR-EA-01**: Load `role`, `goal`, and `backstory` from `config/agents.json::agents.editor`;
   none of these strings may appear in source code.

2. **FR-EA-02**: For every `[NEEDS_FORMULA]` marker found in any chapter file, replace it with
   a LaTeX formula stub of the form `$$ \text{formula placeholder} $$` and add a note to
   `edit_report.md` identifying the chapter and line. The replacement must use `amsmath`-
   compatible syntax so that the LaTeXAgent can render it as a "fancy formula, not plain text"
   (per spec §13.2).

3. **FR-EA-03**: Parse every `[AuthorYear]` citation marker and verify it against the keys
   present in `latex/bib/references.bib` (via `FileReadTool`). Any unmatched marker must be
   listed in `edit_report.md` under a `## Unresolved Citations` section. The EditorAgent does
   NOT silently drop or auto-correct unresolved keys — it flags them for human review.

4. **FR-EA-04**: Apply prose improvements: fix passive-voice overuse, enforce consistent
   terminology (glossary loaded from `skills/editor_skill/references/glossary.md`), and ensure
   each chapter has an introductory paragraph and a closing summary paragraph.

5. **FR-EA-05**: Verify the BiDi chapter (detected by `<!-- BiDi chapter -->` comment) has at
   least one English-in-Hebrew and one Hebrew-in-English code-switch. If absent, add a
   flag `[BIDI_INCOMPLETE]` and log it in `edit_report.md`.

6. **FR-EA-06**: Write all edited chapters to `workspace/chapters_edited/` using `FileWriteTool`;
   preserve original filenames (`chapter_01.md`, etc.).

7. **FR-EA-07**: Write `workspace/edit_report.md` summarising: files processed, marker
   replacements, citation validation results, and any flags raised.

---

## Non-Functional Requirements

- **NFR-EA-01 Idempotency**: Running `EditorAgent` twice on the same input produces identical
  output (no random UUIDs or timestamps in edited files).
- **NFR-EA-02 Auditability**: `edit_report.md` must be human-readable and sufficient for a
  reviewer to understand every change made without seeing the diff.
- **NFR-EA-03 Fault Isolation**: A single chapter failing validation must not abort processing
  of the remaining chapters; errors are collected and reported in bulk.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `agents.editor.role` | `config/agents.json` | CrewAI `role` string |
| `agents.editor.goal` | `config/agents.json` | CrewAI `goal` string |
| `agents.editor.backstory` | `config/agents.json` | CrewAI `backstory` string |
| `agents.editor.llm` | `config/agents.json` | LLM model key |
| `agents.editor.skill_ref` | `config/agents.json` | Relative path to `SKILL.md` |
| `agents.editor.style_rules` | `config/agents.json` | Inline style config dict |

---

## Acceptance Criteria

- [ ] A chapter with `[NEEDS_FORMULA]` is transformed to contain `$$…$$` amsmath syntax in
      the edited output.
- [ ] A `[AuthorYear]` marker not in `references.bib` appears under `## Unresolved Citations`
      in `edit_report.md` and is NOT silently removed.
- [ ] A valid `[AuthorYear]` marker (present in `references.bib`) does NOT appear in
      `## Unresolved Citations`.
- [ ] All edited chapters are written to `workspace/chapters_edited/`; no chapter from
      `workspace/chapters/` is left unprocessed.
- [ ] `ruff check` returns 0; file has ≤ 150 logical lines.
