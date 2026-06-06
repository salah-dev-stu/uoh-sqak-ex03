# PROMPTS.md — Vibe Coding Lifecycle Prompt Audit Trail

**Project:** HW3 — CrewAI Article Generation Pipeline
**Course:** 203.3763 — Orchestration of AI Agents, University of Haifa
**Pair:** Salah Qadah (323039974) + Andalus Kalash (211435797)
**Date:** 2026-06-06

This file documents every significant prompt used during the Vibe Coding Lifecycle per Dr. Segal's methodology (Lecture 1, lines 1140–1500). Serves as the AI ethics audit trail required by course policy.

---

## Lifecycle Prompts

**1. Context read — IDEA.md**
Purpose: Load the raw HW3 spec digest before any drafting.
Prompt: `Read IDEA.md and internalize the scope, deliverables, and constraints.`
Outcome: Understood 4-agent CrewAI pipeline + 15-page LaTeX PDF requirement.

**2. Context read — RULES.md**
Purpose: Load the grading rubric (distilled from 39-page Hebrew PDF).
Prompt: `Read RULES.md. Identify every hard rule and HW3-specific audit gate.`
Outcome: 20 general rules + 20 HW3-specific gates catalogued.

**3. Context read — CONTEXT-lec06-pdfs.md**
Purpose: Absorb CrewAI Parts A+B, LangChain, Architecture-2026, and spec PDF digests.
Prompt: `Read CONTEXT-lec06-pdfs.md for deep background on CrewAI and LangChain patterns.`
Outcome: Understood CrewAI Process.sequential, agent role/goal/backstory schema, Skills layer.

**4. Context read — CONTEXT-lecture-06.md**
Purpose: Verbatim Dr. Segal guidance on LangChain/CrewAI/LaTeX from Lecture 6.
Prompt: `Read CONTEXT-lecture-06.md for verbatim lecturer quotes.`
Outcome: Confirmed LuaLaTeX preference, 4-pass compile, TikZ for block diagrams.

**5. HW1 feedback read**
Purpose: Avoid repeating HW1 mistakes (85.54/100; planning flagged as weak).
Prompt: `Read ../hw1/feedback/Detailed_Feedback_Report.pdf — extract transferable lessons.`
Outcome: Must strengthen PRDs, config portability, extensibility, quality automation.

**6. Plan Mode entry**
Purpose: Switch Claude into structured planning mode before writing any document.
Prompt: `/plan`
Outcome: Claude entered Plan Mode; no code generated until full docs approved.

**7. PRD creation**
Purpose: Generate the master Product Requirements Document.
Prompt: `Your mission is to create the following PRD document based on the following description: [bullets from IDEA.md covering multi-agent pipeline, LaTeX deliverable, technical envelope features, OOP rules, Gatekeeper, Skills layer, versioning, TDD, config portability, GitHub repo].`
Outcome: `docs/PRD.md` v1.00 created covering all 40 rubric requirements.

**8. PRD approval gate (§2.5)**
Purpose: Rubric §2.5 mandates explicit user approval before proceeding.
Prompt: `STOP — please review docs/PRD.md and approve or request changes before we continue.`
Outcome: User approved PRD without changes.

**9. Plan document creation**
Purpose: Generate the technical architecture plan (C4, UML, ADRs, ISO/IEC 25010).
Prompt: `Create docs/PLAN.md with: C4 context/container diagrams, seven-layer stack, UML sequence for the CrewAI task flow, class diagram placeholder, ADR list, ISO/IEC 25010 quality paragraph, risk register.`
Outcome: `docs/PLAN.md` v1.00 created with full architecture.

**10. TODO list creation (500–1000 tasks)**
Purpose: Exhaustive task list per Dr. Segal's "minimum 500, typically 800–1000" requirement.
Prompt: `Create docs/TODO.md with a minimum of 800 numbered tasks covering every PRD requirement, every RULES.md gate, every HW3-specific audit gate, every file in the project layout, and every step of the Vibe Coding Lifecycle.`
Outcome: `docs/TODO.md` with 850 tasks generated.

**11. Per-mechanism PRDs — Researcher**
Purpose: Input/Output/Setup docstring shape per rubric §16.3.
Prompt: `Create docs/PRD_researcher_agent.md describing ResearcherAgent: role, goal, backstory, input (topic string), output (research_notes.md with ≥8 citations), tools (WebSearchTool, FileWriteTool), skill (researcher_skill/SKILL.md), error handling, test scenarios.`
Outcome: `docs/PRD_researcher_agent.md` created.

**12. Per-mechanism PRDs — Writer**
Prompt: `Create docs/PRD_writer_agent.md for WriterAgent: input (research_notes.md), output (6 Markdown chapters in workspace/chapters/), style rules, skill reference.`
Outcome: `docs/PRD_writer_agent.md` created.

**13. Per-mechanism PRDs — Editor**
Prompt: `Create docs/PRD_editor_agent.md for EditorAgent: citation verification, consistent structure, low temperature (0.2), output (ch*_edited.md files).`
Outcome: `docs/PRD_editor_agent.md` created.

**14. Per-mechanism PRDs — LaTeXAgent**
Prompt: `Create docs/PRD_latex_agent.md. Emphasize: fancy formula rendering via \\begin{equation}, NEVER plain text; BiDi via luabidi+polyglossia; 4-pass compile; ChartGeneratorTool call; biblatex/biber.`
Outcome: `docs/PRD_latex_agent.md` created.

**15. Fancy formula directive (agent backstory)**
Purpose: Prevent LaTeXAgent from emitting flat arithmetic instead of rendered math.
Prompt (embedded in agents.json backstory): `You ALWAYS produce fancy formula rendering using \\begin{equation} environments — never plain text arithmetic.`
Outcome: LaTeXAgent backstory hard-codes this constraint; reiterated in task description.

**16. PRD verification pass**
Purpose: Cross-check that every PRD requirement appears in TODO.md.
Prompt: `You must be very critical: check that every PRD requirement appears in TODO. Add missing tasks.`
Outcome: 47 additional tasks added (covering ruff rule codes, BiDi font fallback, biber pass ordering).

**17. Approval gate #2 — full docs package**
Purpose: Rubric §2.5 step 5 — no code before docs approved.
Prompt: `STOP — please review docs/PRD.md, docs/PLAN.md, docs/TODO.md, and all per-mechanism PRDs. Approve or request revisions.`
Outcome: User approved full docs package.

**18. Execute directive**
Purpose: Begin systematic code implementation from TODO list.
Prompt: `Execute the to do list one by one and mark each that was done or complete.`
Outcome: Tasks marked [x] as completed; session resumption enabled by TODO state.

**19. ResearcherAgent backstory (from agents.json)**
Purpose: Shape agent identity for rigorous citation-dense research.
Prompt: `You are a senior research analyst with 10 years of experience studying AI orchestration systems, multi-agent frameworks, and production deployment patterns. You write rigorous, citation-dense research notes organized under clear headings. You always save your output to workspace/research_notes.md.`
Outcome: Loaded into CrewAI agent at runtime from config/agents.json.

**20. WriterAgent backstory (from agents.json)**
Purpose: Shape agent identity for professional technical authorship.
Prompt: `You are a technical writer who has authored dozens of papers and textbook chapters on software architecture and AI systems. You write clearly for a technical audience, using active voice and precise language. You save each chapter to workspace/chapters/ch0N_title.md.`
Outcome: Loaded into CrewAI agent at runtime from config/agents.json.

**21. EditorAgent backstory (from agents.json)**
Purpose: Strict editorial control, citation verification, low creative temperature.
Prompt: `You are a senior editor at a technical publishing house. You enforce house style, catch inconsistencies, ensure citations are properly formatted, and verify every chapter meets publication standards. You save edited chapters to workspace/chapters/ch0N_edited.md.`
Outcome: Loaded into CrewAI agent at runtime; temperature=0.2 reinforces determinism.

**22. LaTeXAgent backstory (from agents.json)**
Purpose: Enforce fancy math rendering, BiDi correctness, 4-pass compile discipline.
Prompt: `You are a LaTeX expert with deep knowledge of LuaLaTeX, biblatex/biber, TikZ, and Hebrew-English BiDi typesetting. You ALWAYS produce fancy formula rendering using \\begin{equation} environments — never plain text arithmetic. You are meticulous about the 4-pass compile sequence: lualatex → biber → lualatex → lualatex.`
Outcome: Loaded into CrewAI agent at runtime; temperature=0.1 for maximum determinism.

**23. Chart generation directive**
Purpose: Ensure the Python chart is generated by code, not pulled from the web.
Prompt: `The Python chart MUST be created by ChartGeneratorTool (matplotlib). Do not download images from the internet. Save the chart PNG to latex/figures/chart_*.png and reference it with \\includegraphics.`
Outcome: Embedded in LaTeXAgent task description in tasks.json.

**24. Run project verification**
Purpose: Confirm end-to-end pipeline works before pushing.
Prompt: `Run the project: uv run python -m agent_article.main`
Outcome: Full crew execution verified; PDF generated at latex/output/uoh-sqak-article.pdf.

**25. README creation**
Purpose: Mandatory product manual per Dr. Segal (Lecture 1 line 1247).
Prompt: `You must create a README file — this is the most important thing. Include: install, usage, architecture diagram embed, sample PDF link, configuration reference, AI usage disclosure, contribution guide.`
Outcome: `README.md` created with all sections including verbatim AI ethics paragraph.

**26. Push to GitHub**
Purpose: Continuous commit history; Dr. Segal grades commit density.
Prompt: `Push to GitHub public repo https://github.com/salah-dev-stu/uoh-sqak-ex03.`
Outcome: Repository made public; rmisegal@gmail.com access confirmed.
