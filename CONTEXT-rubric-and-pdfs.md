# Rubric & Materials Digest — HW3 Edition

This file is intentionally slim because **the underlying rubric PDF (`software_submission_guidelines-V3.pdf`) has not changed since HW1 or HW2.** Reuse the digest the orchestrator wrote for HW2:

- **`../hw2/CONTEXT-rubric-and-pdfs.md`** (63 KB) — full rubric breakdown, all 20 sections of the source PDF, verbatim grading-agent terminology, ISO/IEC 25010 Hebrew↔English term pairs

What's NEW for HW3 (covered already in `RULES.md` Section "HW3-specific scorecard"):

| Source | Digested in |
|---|---|
| HW3 spec PDF (`materials/hw3-spec-main-L06-summary-and-ex03-definition.pdf`) | `IDEA.md` + `RULES.md` (verbatim quotes from §13.1 + §13.2) + `IDEA-raw.txt` (raw pdftotext output) |
| Lec 06 PDFs (5 files in `materials/lecture-06-*.pdf`) | `CONTEXT-lec06-pdfs.md` (deep digest by orchestrator subagent) |
| Lec 06 video transcript | `CONTEXT-lecture-06.md` (placeholder; updates when whisper finishes ~110 min from setup time) |

## What changed in the rubric for HW3 vs HW1+HW2

**Nothing in the underlying rubric**, but the HW3 spec adds these audit gates explicitly:

1. **15-page PDF target** with Hebrew bonus
2. **LaTeX project committed** alongside Python code
3. **CrewAI multi-agent team** (≥4 roles)
4. **Skill layer** per agent (file-based instruction packages)
5. **"On the envelope" PDF check**: links work, citations clickable, BiDi correct, tables fit, formulas fancy

See `RULES.md` H1-H25 for the full list with audit methodology.

## How to use the inherited HW2 digest

When writing `docs/PRD.md` or `docs/PLAN.md`:
- The "ISO/IEC 25010" section requires verbatim Hebrew/English term pairs — copy from `../hw2/CONTEXT-rubric-and-pdfs.md` §A10.
- The "ApiGatekeeper class signature" template (rubric §5.1) — copy verbatim from `../hw2/CONTEXT-rubric-and-pdfs.md` §A4.
- The "Building-Block docstring shape" — copy from `../hw2/CONTEXT-rubric-and-pdfs.md` §A13.
- The "Hebrew terminology cheat sheet for grading-agent pattern match" — copy from `../hw2/CONTEXT-rubric-and-pdfs.md` §A23.

Don't re-discover what HW2 already established. Reuse and credit.
