# ADR-002: LuaLaTeX over XeLaTeX for Hebrew BiDi Typesetting

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

The HW3 spec requires a Hebrew-English BiDi section (H8) with correct right-to-left text flow, proper font rendering, and linked bibliography. Two engines support Unicode and BiDi in modern TeX distributions: **LuaLaTeX** and **XeLaTeX**. Both support `polyglossia` and `fontspec`. The spec PDF recommends LuaLaTeX and Dr. Segal confirmed this preference in Lecture 6.

---

## Decision

Use **LuaLaTeX** as the sole compilation engine. Compile sequence: `lualatex → biber → lualatex → lualatex` (4 passes).

---

## Alternatives Considered

| Engine | BiDi Support | Hebrew Fonts | Lua Scripting | Notes |
|---|---|---|---|---|
| **LuaLaTeX** | `luabidi` package | GNU FreeFont, David CLM | Yes | Dr. Segal's stated preference |
| **XeLaTeX** | `bidi` package | Same fonts via fontspec | No | Slightly faster compile |
| **pdfLaTeX** | None | None | No | ASCII only; eliminated immediately |

---

## Rationale

1. **`luabidi` vs `bidi`**: `luabidi` integrates BiDi at the engine level using Lua callbacks, which handles mixed Hebrew/English inline more robustly than the XeLaTeX `bidi` package, particularly around punctuation placement and paragraph direction switching.
2. **Lua scripting hooks**: LuaLaTeX exposes `luatex` callbacks that allow programmatic manipulation of token lists — used by the LaTeXAgent to auto-insert `\begin{RTL}` wrappers around Hebrew-detected content.
3. **`polyglossia`**: Both engines support `polyglossia` for language switching (`\setmainlanguage{hebrew}`, `\setotherlanguage{english}`). Under LuaLaTeX, `polyglossia` + `luabidi` is the tested reference combination.
4. **GNU FreeFont**: `FreeSans`, `FreeSerif`, `FreeMono` provide complete Unicode coverage including Hebrew block (U+0590–U+05FF) and are available in TeXLive without extra downloads.
5. **Spec alignment**: The spec PDF's LaTeX template example uses `\usepackage{luabidi}`, establishing LuaLaTeX as the reference implementation.

---

## Consequences

- **Positive**: Correct right-to-left paragraph flow, proper glyph shaping, clean BiDi without manual `\RL{}`/`\LR{}` wrapping in most cases.
- **Negative**: Compile is ~20–30% slower than XeLaTeX on large documents. Acceptable for a ≤20-page article.
- **Font dependency**: TeXLive on the grader's machine must include `fonts-freefont`. The `Makefile` checks for the font and fails fast with a clear error message if absent.
- **Mitigation**: `.env-example` documents `LUALATEX_BIN` path; `Makefile` has `$(shell which lualatex)` guard.
