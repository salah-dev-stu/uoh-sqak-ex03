# PRD — Bibliography

## Overview

BibTeX bibliography management using `biblatex` + `biber`. All citations in [AuthorYear]
format resolve to clickable links in the final PDF.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `references.bib` | File | BibTeX file in `latex/bib/` with ≥5 entries |
| `biber main` | Command | Processes `.bcf` → `.bbl` (pass 2 of 4) |
| **citation links** | PDF feature | Clicking `[AuthorYear]` jumps to bibliography |

## Functional Requirements

1. **FR1** — `latex/bib/references.bib` committed to repo with ≥5 well-formed entries.
2. **FR2** — `biblatex` style `authoryear` with `hyperref=true` for clickable citations.
3. **FR3** — `biber` (not bibtex) as backend; `biber main` run as pass 2.
4. **FR4** — All citations in `.tex` files use `\parencite{Key}` or `\cite{Key}`.
5. **FR5** — No undefined citations in the final PDF `.log` (all keys in `.bib`).
6. **FR6** — Bibliography section appears in Table of Contents (`heading=bibintoc`).

## Non-Functional Requirements

1. **NFR1** — All BibTeX keys follow `FirstAuthorYear` convention (e.g. `CrewAI2024`).
2. **NFR2** — Unicode characters in titles/authors use UTF-8 encoding.
3. **NFR3** — `\addbibresource{bib/references.bib}` in style file, not in main.tex.

## Setup/Configuration

- `latex/style/article.sty` — `\usepackage[backend=biber, style=authoryear]{biblatex}`
- `latex/Makefile` — `biber --input-directory=output --output-directory=output main` (pass 2)

## Acceptance Criteria

- [ ] `biber main` exits 0 with "Writing ... .bbl" message
- [ ] PDF bibliography section has ≥5 entries
- [ ] Clicking any `(AuthorYear)` citation in the PDF jumps to bibliography
- [ ] `latex/output/main.log` contains no "Citation ... undefined" warnings
- [ ] `references.bib` has entries for all 4 main frameworks (LangChain, CrewAI, LangGraph, AutoGen)
