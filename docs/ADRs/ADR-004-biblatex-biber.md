# ADR-004: biblatex + biber over Legacy bibtex/natbib

**Status:** Accepted
**Date:** 2026-06-06
**Authors:** Salah Qadah, Andalus Kalash (pair uoh-sqak)
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa

---

## Context

The article requires a bibliography with linked citations (H9): clicking a `[AuthorYear]` citation in the PDF must jump to the reference entry. Three bibliography approaches were evaluated: legacy `bibtex` + `natbib`, `biblatex` + `bibtex` backend, and `biblatex` + `biber` backend.

---

## Decision

Use **`biblatex`** (authoryear style) with **`biber`** as the processing backend.

---

## Alternatives Considered

| Approach | Unicode | Authoryear | hyperref links | Hebrew bib entries |
|---|---|---|---|---|
| `bibtex` + `natbib` | No | Yes (natbib) | Partial | Broken (8-bit) |
| `biblatex` + `bibtex` backend | Partial | Yes | Yes | Limited |
| `biblatex` + `biber` (chosen) | Full UTF-8 | Yes | Full | Native |

---

## Rationale

1. **Unicode bibliography**: Biber is a full Unicode-aware replacement for BibTeX. Hebrew author names and titles in `.bib` entries render correctly without escaping or transliteration hacks.
2. **authoryear citation style**: `\autocite{key}` produces `[Smith 2023]` inline and a matching entry in the bibliography. This is the style required by the rubric's "linked citations" gate (H9).
3. **`hyperref` deep integration**: `biblatex` + `biber` produces `\hyperlink`-backed citations automatically when `hyperref` is loaded. Clicking `[AuthorYear]` in the PDF viewer navigates to the bibliography entry. This meets H9 without any manual `\hyperlink` markup.
4. **`biber` sort control**: Biber's `sortlocale` option handles Hebrew collation correctly. The `.bib` file can mix Hebrew and English entries in one file.
5. **Modern maintenance**: `bibtex` is effectively unmaintained for Unicode workloads. `biber` is actively developed and is the reference backend for `biblatex`.

---

## Compile Sequence

```
lualatex main.tex   # pass 1 — generates .bcf file for biber
biber main          # processes references.bib → main.bbl
lualatex main.tex   # pass 2 — inserts bibliography
lualatex main.tex   # pass 3 — resolves cross-references and hyperlinks
```

This 4-pass sequence is hardcoded in `latex/Makefile` and documented in `latex/README.tex`.

---

## Consequences

- **Positive**: All citations are clickable hyperlinks; bibliography is Unicode-clean; authoryear format matches academic norms.
- **Negative**: `biber` must be installed alongside `lualatex`. TeXLive full installs include `biber`; the `Makefile` checks `$(shell which biber)` and fails fast if absent.
- **`.bib` schema**: All entries must use `author = {Last, First}` BibLaTeX syntax. The ResearcherAgent's output template enforces this format in its `SKILL.md` reference section.
