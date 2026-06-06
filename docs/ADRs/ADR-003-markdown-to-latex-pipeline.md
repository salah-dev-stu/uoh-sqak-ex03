# ADR-003: Markdown-First Intermediate Workflow (Agents → .md → .tex)

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

The four CrewAI agents must collaborate to produce a LaTeX document. A key design question is: should agents write LaTeX directly, or write Markdown and let the LaTeXAgent convert? The spec (H12) says "Markdown→LaTeX intermediate workflow recommended."

---

## Decision

Agents 1–3 (Researcher, Writer, Editor) write **Markdown** (`.md`). Only LaTeXAgent produces `.tex` files. Conversion is via a `MarkdownToLatexConverter` utility inside the LaTeXAgent's tool chain.

---

## Alternatives Considered

| Approach | Description | Rejected Reason |
|---|---|---|
| Direct LaTeX | Writer/Editor produce `.tex` directly | LLM hallucination rate on raw LaTeX is high; debugging corrupted LaTeX is painful |
| Pandoc pipeline | Shell out to `pandoc -f markdown -t latex` | External binary dependency; Pandoc's LaTeX output needs heavy post-processing for BiDi/biblatex compatibility |
| Markdown-first (chosen) | Agent writes clean Markdown; LaTeXAgent converts with full control | Clean separation; Writer/Editor focus on content; LaTeXAgent owns all typesetting decisions |

---

## Rationale

1. **LLM reliability**: GPT-class and Claude-class models produce far more reliable Markdown than LaTeX. Markdown syntax errors are trivially correctable; LaTeX syntax errors can cascade into uncompilable documents.
2. **Separation of concerns**: ResearcherAgent and WriterAgent focus on content quality; LaTeXAgent is the sole typesetting expert. This aligns with the course's "single responsibility" OOP requirement.
3. **Human checkpoint**: The `SDK.approve_markdown()` gate fires after EditorAgent finishes, before any `.tex` is generated. Users can read and approve Markdown far more easily than raw LaTeX.
4. **Formula injection**: LaTeXAgent receives a structured directive: "any line starting with `FORMULA:` must be rendered as `\\begin{equation}...\\end{equation}` — never plain text." Markdown makes this convention visible and easy to enforce.
5. **BiDi injection**: Hebrew paragraphs are marked in Markdown with a `<!-- RTL -->` HTML comment. LaTeXAgent detects these and wraps them with `\begin{RTL}...\end{RTL}` from `luabidi`.

---

## Consequences

- **Positive**: Each agent can be tested independently; unit tests mock LLM responses with valid Markdown without needing a LaTeX installation.
- **Positive**: Intermediate files (`workspace/chapters/`) serve as human-readable audit artifacts.
- **Negative**: Two-pass workflow (Markdown generation → LaTeX conversion) adds latency. Acceptable for an article generation pipeline where total runtime is minutes, not seconds.
- **Converter scope**: `MarkdownToLatexConverter` handles headings (H1→`\chapter`, H2→`\section`, H3→`\subsection`), bold/italic, code blocks, tables (`tabularx`), and custom comment directives. It is unit-tested independently.
