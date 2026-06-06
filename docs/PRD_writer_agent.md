# PRD: WriterAgent

**Component**: `src/agent_article/agents/writer_agent.py`
**Version**: 1.00 | **Course**: 203.3763 — University of Haifa HW3

---

## Overview

`WriterAgent` is the second agent in the sequential pipeline. It reads
`workspace/research_notes.md` produced by `ResearcherAgent`, then writes one Markdown file
per chapter (e.g. `workspace/chapters/chapter_01.md`) and a `workspace/outline.md` summary.
One chapter must be designated as the BiDi chapter (`HebrewChapter`) — containing Hebrew text
with correct RTL context markers. The agent uses `skills/writer_skill/SKILL.md` for style
guidance and citation format conventions.

---

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| **Input** `research_notes_path` | `Path` | Path to `workspace/research_notes.md` |
| **Input** `chapter_titles` | `list[str]` | Ordered list from `config/tasks.json` |
| **Input** `target_pages` | `int` | Target page count (default 15); from `config/setup.json` |
| **Input** `hebrew_chapter_index` | `int` | Which chapter index is the BiDi chapter; from config |
| **Input** `skill_path` | `Path` | Path to `skills/writer_skill/SKILL.md` |
| **Output** `chapter_*.md` | `str` | One Markdown file per chapter in `workspace/chapters/` |
| **Output** `outline.md` | `str` | High-level outline with word counts per chapter |

---

## Functional Requirements

1. **FR-WA-01**: Load `role`, `goal`, and `backstory` from `config/agents.json::agents.writer`;
   none of these strings may appear in source code.

2. **FR-WA-02**: Produce exactly `len(chapter_titles)` Markdown files named
   `chapter_01.md … chapter_N.md` inside `workspace/chapters/`. Each file must begin with a
   `# Chapter N: {title}` heading.

3. **FR-WA-03**: Insert `[AuthorYear]`-style citation markers in the prose whenever a fact is
   drawn from a source in `research_notes.md`. These markers must match keys in
   `latex/bib/references.bib`; the EditorAgent verifies them.

4. **FR-WA-04**: The chapter at index `hebrew_chapter_index` (read from config) must contain
   at least 200 Hebrew words and demonstrate Hebrew–English code-switching at least once.
   Mark it with a `<!-- BiDi chapter -->` HTML comment on line 1 so downstream agents can
   detect it.

5. **FR-WA-05**: Distribute content to meet `target_pages` (≈ 300 words/page LaTeX-estimated).
   Include at least one `[NEEDS_FORMULA]` marker in a suitable chapter for the EditorAgent to
   process.

6. **FR-WA-06**: Write a brief `workspace/outline.md` listing each chapter title, estimated
   word count, and the citation keys used.

7. **FR-WA-07**: Use `FileWriteTool` (via `ApiGatekeeper`) to write all output files; do not
   use bare `open()` calls in agent task logic.

---

## Non-Functional Requirements

- **NFR-WA-01 Style Consistency**: All chapters must use the same Markdown heading hierarchy
  (`#` for chapter, `##` for section, `###` for subsection).
- **NFR-WA-02 Hebrew Quality**: The BiDi chapter must not contain Arabic script (Dr. Segal's
  explicit requirement: Hebrew or English, not Arabic). Enforced by a post-task validator.
- **NFR-WA-03 Testability**: `WriterAgent` accepts an injected `FileWriteTool` so unit tests
  can capture written content without touching the filesystem.

---

## Setup / Configuration

| Key | File | Description |
|---|---|---|
| `agents.writer.role` | `config/agents.json` | CrewAI `role` string |
| `agents.writer.goal` | `config/agents.json` | CrewAI `goal` string |
| `agents.writer.backstory` | `config/agents.json` | CrewAI `backstory` string |
| `agents.writer.llm` | `config/agents.json` | LLM model key |
| `agents.writer.skill_ref` | `config/agents.json` | Relative path to `SKILL.md` |
| `tasks.write.chapter_titles` | `config/tasks.json` | Ordered list of chapter title strings |
| `setup.target_pages` | `config/setup.json` | Integer; default 15 |
| `setup.hebrew_chapter_index` | `config/setup.json` | Zero-based index of the BiDi chapter |

---

## Acceptance Criteria

- [ ] With `MockLLM`, `WriterAgent` produces exactly 6 Markdown files in `workspace/chapters/`
      (one per chapter plus `outline.md`).
- [ ] Chapter at `hebrew_chapter_index` starts with `<!-- BiDi chapter -->` comment.
- [ ] At least one `[NEEDS_FORMULA]` marker appears somewhere across the chapter files.
- [ ] Citation markers matching `[AuthorYear]` pattern are present in at least 3 chapters.
- [ ] The Hebrew chapter contains no Arabic Unicode block characters (U+0600–U+06FF).
- [ ] `ruff check` returns 0; file has ≤ 150 logical lines.
