# Lecture 06 — "LangChain, CrewAI & LaTeX Article Production" — HW3 Authoritative Digest

**Source:** `/Users/salah/Projects/orch-ai-agents/lectures/lecture-06-langchain-crewai.txt` (1860 lines, ~128 KB, transcribed by whisper.cpp from the recorded Spring 2026 lecture). SRT (timestamped) co-located at `lecture-06-langchain-crewai.srt`. Lecture spans roughly **00:17:40 → 02:28:09** (~2h 10min of actual content after whisper's 17:40 silence-skip).

> **The lecture is the absolute authority.** Per Dr. Segal's own framing in HW2 lec-05, and reinforced in this lecture's spec-delivery portion (line 1409–1601): the recording is what binds; the 5 Lec-06 PDFs are downstream. **Where they disagree, this digest (and the underlying transcript) override the PDF.** Most disagreements here are softening or scope-clarifying, not reversing — but they are graded.
>
> **Reading map (text-file line numbers; timestamps approximate):**
> - L1–500 / 00:17:40 → 01:06 → Architecture-2026 backdrop: Harness, Provider vs On-Prem vs Cloud, Ollama+HuggingFace, MCP/A2A, agent security, Code Agents, observability.
> - L500–760 / 01:06 → 01:22 → Break + Q&A about how license / IPC vs framework / open-source risk fits the production picture.
> - L760–1160 / 01:22 → 01:46 → LangChain deep-dive: Harness definition, RAG-HR worked example, LCEL pipeline, agent vs chain, LangGraph, AI economy positive/negative.
> - L1160–1408 / 01:46 → 02:02 → CrewAI conceptual model: Agent / Task / Crew / Process, Context-as-glue, Sequential vs Hierarchical, 9-step pseudocode walkthrough on Researcher→Writer→Reviewer.
> - **L1409–1601 / 02:02 → 02:13 → THE HW3 ASSIGNMENT spoken aloud (most important section in the whole file).**
> - L1601–1859 / 02:13 → 02:28 → **Student Q&A on HW3 specifics — page count, English/Hebrew, XeTeX vs LuaLaTeX, reusing existing research, what gets graded.** This is where most of the "ambiguity resolutions" below come from.

---

## 1. 🚨 CONTRADICTIONS with the spec PDF — apply these to IDEA.md immediately

### 1.1 Page count is **15, NOT 30** — confirmed by live negotiation in the room

The spec PDF §13.1.1 says *"כ-15 עמודים (סוכם בכיתה)"* — "~15 pages, agreed in class". The IDEA.md currently treats 15 as soft. **The transcript proves 15 is the *result* of an explicit haggle, not a default Dr. Segal pulled out of thin air, and his initial number was very different.**

Lines 1421–1428 (≈ 02:03:00) — Dr. Segal's *initial* spec:
> *"מאמר של סדר גודל של, אם זה בעברית, אז עד 30 עמוד, לא צריך יותר, עד 30 עמוד. אם זה באנגלית אפשר להגיע גם ל-50."*
>
> *"An article of order of magnitude — if in Hebrew, **up to 30 pages**, no more than 30 pages. If in English, can reach 50."*

A student then asks (L1678) if page count is a hard requirement. Dr. Segal expresses dilemma — too many = too many tokens — and explicitly opens a negotiation (L1687):

> *"בוא נעשה משא ומתן, כמה עמודים אתה רוצה?"*
> *"Let's negotiate — how many pages do you want?"*

The student says "5". Dr. Segal: *"אנחנו נעשה 25. יופי של תשובה"* ("we'll do 25, great answer"). Then another student references conference norms — and the lecturer SETTLES (L1702):

> *"טוב, יאללה, שיהיה חמש עשרה. סגרנו."*
> *"Fine, let's say **fifteen**. Done."*

**Final binding number: 15 pages.** The PDF's "~15" wording is correct, but the **lecture explicitly says "סגרנו" ("done/sealed")** — meaning this is not a soft target. The student who pushed for 5 was rebuked as "greedy". Plan for 13–17 pages; anything under 12 will look like skipping the bargain.

**Update to IDEA.md:** decision #10 → "15 pages is the negotiated floor; the *Hebrew bonus path* was originally a 30-page ask, so a 15-page Hebrew article is on the floor for that variant, not over-delivery." Strict on the floor side; soft (~17) acceptable on the upside.

### 1.2 Hebrew is **not required** — only one BiDi *chapter* matters

The spec PDF §13.1.5 and the IDEA.md treat "Hebrew is harder and more appreciated" as if writing the whole article in Hebrew is the best play. **The transcript reveals that what Dr. Segal actually grades is one BiDi *chapter*, and a full-English article is explicitly permitted** as long as that chapter exists.

Lines 1613–1631 (≈ 02:14) — student Roi says he only wants to write in English. Dr. Segal:
> *"העניין הוא שאני רוצה לראות שאתה מתמודד עם מסמך מורכב בעברית, משלב בפנים ימין-שמאל ושמאל-ימין... תעשה את כל המסמך באנגלית, תכין פרק אחד במסמך, תערבב לי שם עברית ואנגלית."*
>
> *"The point is I want to see you handle a complex Hebrew document, mixing right-to-left and left-to-right inside... **make the whole document in English, prepare ONE chapter in the document, mix Hebrew and English there.**"*
>
> *"אני רוצה לראות שאתה תומך בימין-שמאל, שמאל-ימין, כל הבלאגן הזה."*
> *"I want to see you support RTL, LTR, all the formatting balagan."*

Student confirms: *"הבנתי, את הפורמטינג בלאגן"* ("Got it — the formatting balagan").
Dr. Segal: *"בדיוק, זה מה שחשוב לי לראות."* ("Exactly, that's what matters to me.")

**Implication for HW3:** writing in Hebrew is still a *bonus* path, but if Salah & Andalus go English-default, they only need to commit to a single Hebrew↔English mixed chapter — typically 1–2 pages of Hebrew prose with English technical terms (and vice versa) inside an otherwise-English article.

**Update to IDEA.md:** decision #1 ("article topic") and "What you must NOT do" section — Hebrew is rewarded but NOT mandatory. A full-English article with one solid BiDi chapter satisfies §13.1.5.

**Recommendation update:** the orchestrator should now actively neutralize the "Hebrew = always better" stance. If Salah is more confident in English technical writing, **English with one Hebrew chapter is the safer high-floor strategy.** Hebrew-throughout remains a ceiling-raise but only if writing-quality holds up.

### 1.3 LaTeX compiler — **XeLaTeX is FULLY permitted, no penalty**

The PDF and IDEA.md treat LuaLaTeX as recommended-with-XeLaTeX-allowed but the IDEA.md notes "XeLaTeX allowed but worse Hebrew kerning". The transcript is much more permissive.

Line 1704–1706 (≈ 02:18) — student asks if it matters whether they compile with xelatex or lualatex:
> *"יורם, זה משנה אם אני מקמפיין עם xe.tech ולא lua.tech?"*
> *"לא, לא משנה לי, ממש לא."*
>
> *"Yoram, does it matter if I compile with xe.tex and not lua.tex?"*
> *"**No, it doesn't matter to me, not at all.**"*

Earlier (L1581–1589) Dr. Segal explains his LuaLaTeX preference is personal experience-driven, not normative: *"זה לא חובה, זה לא דרישת חובה או משהו... אני, יש לי ניסיון מאוד טוב עם הקומפיילר הזה בעברית, שילוב עם אנגלית."*

**Update to IDEA.md:** decision #5 → "Either LuaLaTeX or XeLaTeX is fine, no scoring difference. LuaLaTeX is Dr. Segal's personal preference, not a rule. Pick whichever is easier to install on macOS." (On macOS via TeX Live both ship; no install cost difference.)

### 1.4 The article must visibly contain a **block-schematic / TikZ diagram of YOUR Crew architecture**

The spec PDF mentions TikZ for graphics generically. The transcript escalates this — Dr. Segal explicitly says the README/article should SHOW the Crew architecture diagram, and TikZ is the suggested tool.

Lines 1708–1714 (≈ 02:19):
> *"אתם צריכים להראות לי את הארכיטקטורה ולהראות לי את ה-Crew AI, מה עשיתם, איך זה עובד, מה זה. מי שמגדיל ראש גם מראה לי את הארכיטקטורה של ה-Object Oriented וכן הלאה."*
>
> *"You need to **show me the architecture** and show me the Crew AI — what you did, how it works, what it is. **Whoever goes the extra mile also shows me the OOP architecture** and so on."*
>
> *"אני מצפה לראות שתעשו סכמות, בלוקים למשל, בתוך ה-PDF... תיקוץ, באיזה ספרייה זה, מה זה? — טיקסי, זה של להט"ך."*
>
> *"I expect you to make schematics, block diagrams for example, **INSIDE the PDF**... what library is it? — **TikZ, it's LaTeX's.**"*

**Implication:** the PDF must contain at minimum ONE block diagram of the Crew architecture (Researcher → Writer → Editor → LaTeX-Producer + dotted Process arrow). TikZ is the recommended tool but PNG via Python is also fine since the spec's §13.1.4 image requirement is separate. **Going the extra mile = also include an OOP class diagram in TikZ.**

**Update to IDEA.md:** mandatory addition to "Mandatory engineering requirements" — H21 "Article PDF contains a Crew architecture block diagram (TikZ preferred)." Bonus H22: "Article PDF also contains an OOP class diagram (TikZ)."

### 1.5 The **OOP class diagram** is now article-content, not just doc/-content

HW1+HW2 had the class diagram living under `docs/diagrams/`. The transcript above moves it INSIDE the article PDF as bonus territory. **Update to docs/PLAN.md plan:** the same class diagram exported as TikZ goes into one of the article chapters titled "Architecture of the production pipeline" (e.g. chapter 5 of the article).

### 1.6 Bibliography compile-loop is **exactly 4 passes**, confirmed by Dr. Segal personally

PDF says "~4". Lecture confirms it's exactly 4 and explains why (L1661–1674, ≈ 02:15):

> *"חבר'ה, בגלל, הלוא כשאתם עושים ציטוטים, הם מופיעים בגוף המסמך... הציטוט מופיע ברשימת בביליוגרפיה. עכשיו בלת"ך, הקומפיילר, צריך לקמפייל, אז ברגע שיש גם את הקבצי ביב, ששם הציטוטים, וגם את הקבצי טט... אז בשביל שהוא יעדכן את הכול, **הוא חייב להתקמפל ארבע פעמים. ארבע פעמים יוצא לו להתקמפל**."*
>
> *"Folks, because when you do citations they appear in the body of the document... the citation appears in the bibliography list. Now in LaTeX, the compiler — when you have both `.bib` files (where the citations are) and `.tex` files... so that it updates everything, **it must compile FOUR TIMES. Four times.**"*

> *"לפעמים, אם אתם תראו שאתם לוחצים על הרפרנס והוא לא קופץ למטה לציטוט, זה בגלל שהוא לא עשה ארבע פעמים את הקומפילציה."*
>
> *"Sometimes, if you click a reference and it doesn't jump to the citation, **it's because it didn't compile four times.**"*

Note also (L1672): *"קלוד יודע את זה לבד, הוא חוזר עושה את זה לבד"* ("Claude knows this and repeats it on its own"). This is a hint: when Claude is the agent driving compilation, it should automatically loop until refs resolve, rather than requiring a Makefile.

**Update to docs/PRD_bibliography.md (or the LaTeX-Producer agent's PRD):** the compile sequence is `lualatex → biber → lualatex → lualatex → lualatex` (4 lualatex calls between biber). The agent should *verify* the cross-ref resolution by parsing the `.log` for "Rerun to get cross-references right" warnings, not just always-4-and-pray.

---

## 2. ✅ AMBIGUITY RESOLUTIONS for the 10 open decisions in IDEA.md

### Decision 1 — Article topic (Free choice)

**Status: NOT RESOLVED — confirmed open by lecturer.**

Lines 1413–1418: *"אתם שוב בוחרים נושא שבא לכם... יש כמה רמות, כמו תמיד אצלי."*  ("Again you pick a topic you like... there are several levels, as always with me.")

Lines 1768–1810 (≈ 02:22) — student asks if he can use his own research paper as the seed. Dr. Segal: *"אני מאוד מעריך את זה... מי שמצליח גם למצוא שימושים מהחיים היום שלכם... זה לטובתכם, כי זה באמת באמת כלי מטורף על לעבוד עם לאט"ח, זה משדרג אתכם."* — *"I really appreciate when people find uses from your day-to-day lives... this is for your benefit, it's truly a crazy tool to work with LaTeX, it upgrades you."* **Encouragement for personal-life / real-work topics.** Strong hint: a recursive/meta topic (the Crew that wrote the article) is also welcome by his vibe-coding philosophy.

**Recommendation for IDEA.md decision #1:** keep open with a steer toward something the user has personal stake in OR the meta-pick ("CrewAI as orchestration layer — building this article"). Reject "fake research filler" — lecture L1844–1850 makes clear chapters need topical coherence.

### Decision 2 — LLM provider for CrewAI

**Status: NOT directly resolved; but DEFAULT lean is reinforced.**

Architecture section (L70–122) reiterates the three-way Provider / On-Prem / Cloud choice but Dr. Segal explicitly says for early POC: **always start at Provider** (L118–121: *"אני מאוד ממליץ לכם כשאתם מתחילים פרויקט הוכחת היתכנות ראשונית רק לראות שיש היגיון במה שאתם עושים עדיף להתחיל עם הפרוביידר."*).

HW3 is a one-shot POC. Therefore **default = Provider = Claude (via Claude CLI login)** stays correct. Different provider per agent (HW2 lec-05's "encouraged" stance for the debate) is NOT mentioned for HW3 — because here the agents COOPERATE rather than ARGUE, so a single provider is fine.

**Recommendation for IDEA.md decision #2:** keep Claude default (CLI login preferred, API key fallback). The "mix providers for bonus" from HW2 no longer applies cleanly to HW3 — drop that bonus framing.

### Decision 3 — Different LLM per agent

**Status: REVISED — drop this as a bonus path.**

In HW2 (debate) mixed providers were credited as "creating disagreement". In HW3 (cooperative writing) the dynamic flips: a single LLM keeps the article voice consistent. The lecturer mentions different LLMs only in the context of his own LangChain-component examples (e.g., `ChatOllama` vs `ChatOpenAI` showing modularity, L948), not as an HW3 grading lever.

**Recommendation for IDEA.md decision #3:** "Same provider across all agents. Vary `temperature` and `role`/`backstory` per agent instead. Mixing providers offers no bonus credit here and risks tone inconsistency in the prose."

### Decision 4 — Sequential vs Hierarchical Process

**Status: STRONGLY resolved → sequential.**

Lines 1245–1265 — Dr. Segal walks through sequential first as the *default* CrewAI shape. Lines 1261–1274 introduce Hierarchical only as an aside, with the verbal pitch: *"זה כמובן מתאים לתהליכים פתוחים יותר, משתנים או מורכבים, זה כמובן משהו הרבה יותר מורכב."* ("Suitable for more open, variable or complex processes — much more complex.")

Article writing is a closed, linearly-staged process. Hierarchical adds complexity for no grade upside under the envelope-only grading.

**Recommendation for IDEA.md decision #4:** Confirmed **Process.sequential** as default. Hierarchical is NOT a bonus path; it's just extra risk. Mention in the article's "Future work" section but do not implement.

### Decision 5 — LaTeX compiler

**Status: RESOLVED — see §1.3 above. XeLaTeX OR LuaLaTeX, no preference enforced.** Update IDEA.md to drop the "worse Hebrew kerning" comment about XeLaTeX since the lecturer explicitly said it doesn't matter to him.

### Decision 6 — Markdown-first workflow

**Status: RESOLVED — explicitly recommended (Dr. Segal explains his own workflow).**

Lines 1644–1660 (≈ 02:15) — student asks why not LaTeX direct:
> *"המרקדאון יותר מהיר, ומהניסיון שלי... נורא קשה לדבק כשאתה כל הזמן עובד על PDF, כי כל פעם הוא צריך לקמפייל, וכשיש לך רפרנסים וביב, צריך לעשות איזה ארבע קומפילציות בשביל שהוא יעבור על כולם. צריך לחזור ארבע פעמים. אז זה המון זמן לוקח."*
>
> *"Markdown is faster, and from my experience... it's really hard to debug when you constantly work on PDF, because each time it has to compile — and with `.bib` references it has to do about four compilations to go through all of them. Four times. That takes a lot of time."*
>
> *"אז אני רוצה קודם כל לראות שבמרקדאון הכל בסדר, הכל יש לי, התמונות במקום, הנוסחאות, זה, זה, זה, הכל בסדר. עכשיו אני, זה שיטת עבודה שלי, אתה מבין?"*
>
> *"So first I want to see that in Markdown everything is OK — images in place, formulas, everything. **It's my working method.**"*

Confirmed: produce content in Markdown, convert to `.tex` only at the end. Dr. Segal explicitly calls this "his working method."

**Recommendation for IDEA.md decision #6:** Confirmed YES. **Pipeline shape:** Researcher → Writer → Editor produce/edit Markdown. The LaTeX-Producer agent takes the final approved Markdown and converts it. The Markdown intermediate files MUST be committed (they're the trace evidence).

### Decision 7 — Web search provider

**Status: NOT directly resolved for HW3 (HW2 said "must exist"; HW3 lecture didn't restate).**

The HW3 lecture portion doesn't explicitly demand a web-search tool. But the spec PDF's 9-step CrewAI pseudocode (Step 1) uses `SerperDevTool` as the example. And the Researcher agent's logical purpose IS web search.

There is an interesting workaround student-discussed (L1768–1800): bringing your own pre-existing research into the project. Dr. Segal accepts that — *"זה לגיטימי"* — but stresses (L1779–1788): *"בסוף צריך, אני צריך להיות מסוגל לשחזר את התוצאה שלך. אז אם לא תשים את ה...אז אם אתה לוקח מאמר, ויש לך תוצאות של ניסויים, ויש לך טבלאות, ויש לך דברים, ואתה לא רוצה לשים את זה פה בפרויקט, וזה לגיטימי, אז אתה צריך לבחור משהו אחר."* — **the source material must be in the project, or pick a different topic. Reproducibility is the criterion.**

**Recommendation for IDEA.md decision #7:** Have a search tool **AND** allow fallback to a local-knowledge mode. For a topic the agents already know (e.g., "CrewAI architecture"), web search is optional; for fresh topics, it's required. **Default:** include a `web_search.py` tool (DuckDuckGo Lite via `duckduckgo-search` — no API key needed, no Serper costs), but the Researcher's prompts also encourage "use your own training knowledge first; search to verify and find citations."

### Decision 8 — Chart library

**Status: NOT resolved; lecturer doesn't care.**

The spec just says "graph generated in Python code". No library named. matplotlib is the safest default (universal, no plotly extra-deps, exports clean PNGs).

**Recommendation:** Keep matplotlib default. Optional bonus: also use `pgfplots` for a TikZ-native chart that satisfies BOTH the "Python-generated" requirement (if the .py file produces .tex via `pgf` backend) AND lives natively in the document. But this is over-engineering — start with matplotlib + PNG.

### Decision 9 — Cover sheet design

**Status: NOT directly addressed, but lecturer paints the picture (L1436–1442):**

> *"אני מצפה לראות הדרים ופוטרים, אתם יודעים שיהיה כזה מכובד, יהיה איזה קאבר-שיט, יהיה איזה דף קאבר-שיט ששם יהיה כתוב מה נושא, השם של הכותב, שזה אתם, תאריך, אוקיי? משהו בסגנון הזה, בקורס זה וזה, אצל המרצה הזה והזה, מין קאבר-שיט כזה יפה."*
>
> *"I expect to see headers and footers — you know, something dignified, there will be a cover sheet, a cover-sheet page where the topic is written, the author's name (which is you), the date, OK? Something in this style — in such-and-such course, with such-and-such instructor. A nice cover sheet."*

Key adjective is **מכובד / יפה** = "dignified / pretty". Not "minimalist". Not "academic-plain". Some visual care expected.

**Recommendation for IDEA.md decision #9:** TikZ-framed cover sheet (border, possibly a small logo/seal area) with all 5 fields large and centered. The course code (203.3763) and lecturer's title (ד"ר יורם סגל / Dr. Yoram Segal) should be explicitly present.

### Decision 10 — Page count strictness

**Status: RESOLVED — see §1.1 above. 15 is the negotiated floor. Plan 14–17.**

---

## 3. ➕ ADDITIONS — requirements/clarifications Dr. Segal said orally but aren't in the spec PDF or slide PDFs

### 3.1 (Most important) Grading is on the **TECHNICAL ENVELOPE** — content correctness explicitly NOT graded

The spec PDF has this in §13.1 evaluation paragraph; the lecture HAMMERS it into a verbatim dictum. Student Yair asks directly (L1815):

> *"האם אנחנו נמדדים על נכונות במאמר, והאם זה אמיתי או שכן?"*
> *"Are we graded on correctness in the article, and whether it's real or not?"*

Dr. Segal (L1815–1835):
> *"לא, אני לא קורא את המאמר. המאמר כמאמר, אני לא קורא אותו. מבחינת, אני כן מצפה לראות שהלינקים מחוברים, שהציטוטים הם קיימים, אבל אני לא קורא את המאמר. הנושא שלי הוא לא המאמר, אני לא בעל, הנושא פה הוא **המעטפת**."*
>
> *"**No, I do not read the article. The article as article, I don't read it.** I do expect to see that the links are connected, that the citations exist, but I don't read the article. My topic is not the article — the topic here is **the envelope.**"*

And again (L1828–1835):
> *"אין לי בעיה שאני לוקח את הטקסט שייצר לך ג'מנאי או ייצר לך מישהו, ואתה רק מעביר אותו בצנואר הזה. מה שאותי מעניין, שהבדיקה היא בדיקה טכנית, לא על המהות. **אני לא בודק אם כתבת שמדינת ישראל נוסרה ב-1949 במקום ב-1948**, אני לא בודק את זה. זה לא המהות שלי, של התרגיל הזה בכלל."*
>
> *"I have no problem with you taking text Gemini generated or someone else generated and just passing it through this pipe. What I care about is that the check is a technical check, not on substance. **I don't check whether you wrote Israel was founded in 1949 instead of 1948** — I don't check that. That's not my substance, not for this exercise at all."*

**Implication for HW3 strategy:**
- **Do not waste tokens on citation verification or fact-checking.** Plausible-sounding `.bib` entries are fine.
- **Do waste effort on link plumbing.** Every `\ref{}`/`\cite{}` must resolve. Run a link-resolution test as part of the build.
- **Tables must fit the page.** Add a post-compile audit step that grep's the `.log` for "Overfull \hbox" warnings on tables specifically.
- **Formulas must be fancy.** See §3.2.

But also (L1844–1850) — coherence WITHIN the article still matters:
> *"אתה לא יכול סתם לזרוק מילים. בסדר? אתה לא יכול, נגיד, שפרק א' ידבר על גידול חסה ופרק ב' ידבר על משוואות האהבה. זה צריך להיות איזה משהו הגיוני בנושא."*
>
> *"You can't just throw words. You can't, e.g., have chapter 1 about lettuce farming and chapter 2 about love equations. **There needs to be SOMETHING coherent in the topic.**"*

So the rule is: **factual claims uncheckable; topical coherence audible at a 30-second skim is the bar.** A reader should be able to flip through, see the same theme, and not laugh.

### 3.2 "Fancy formula" pitfall — Dr. Segal's personal pain point

This is in the spec PDF but the lecture (L1734–1758) describes the FAILURE MODE in unusual detail:

> *"בהתחלה עלול לצאת לכם נוסחאות, מה שנקרא, שטוחות, plain text, כי הוא פשוט יכתוב לכם את הלהט"ך, אז אתם תראו סלאש זה, סלאש זה. אתם אמורים לקבל **פנסי, פורמולה**, תבקשו ממנו **fancy formula, המילה פנסי, מפואר**, אתם רוצים נוסחאות מפוארות, אתם לא רוצים plain text."*

> *"מה שקורה הרבה פעמים, קרה לי הרבה פעמים, שבגלל כל מיני שטויות שלו, בגלל עברית-אנגלית, בגלל כל מיני פונקציות שעטפו אותו וכן הלאה, הוא פתאום כותב לך באמצע המסמך plain text. **קרה לי. באגים, זה באגים בקוד**, זה באגים בדברים. ואז אתה אומר ל-ל.ל.ם והוא מתקן את זה."*

Translation: "**Happened to me. These are bugs in the code, bugs in things. Then you tell the LLM and he fixes it.**"

**Implication for HW3:** the LaTeX-Producer agent's prompt MUST include the verbatim phrase **"fancy formula, not plain text"** (English; Dr. Segal said exactly the English phrase). Post-compile audit: a regex over the .tex looking for math-region indicators like `$$...$$`, `\begin{equation}`, `\frac{}`, `\sum_`, `\int_` etc. — if NONE of these appear but `^2` or `_i` does, formula is plain-text and must be re-prompted.

### 3.3 LaTeX is **mandatory** — overleaf is NOT acceptable

Lines 1472–1479 — a student suggests Overleaf:
> Student: *"יורם, אבל אפשר גם באוברליפט, למי ש..."*
> Dr. Segal: *"לא, לא, ממש לא. לא, לא, לא, לא. **אני מתעקש על זה.**"*
> Student: *"אבל זה, אנחנו לא נחטוף את הקוד. כמו, זה agent יעשה."*
> Dr. Segal: *"ודאי, ודאי, ודאי, אתם, חבר'ה, אתם לא כותבים, אתם **בווייב קודינג** פה, בקורס הזה, בסדר? אתם אמורים, מה שאתם אמורים להגיד לו, אתם **צריכים לייצר לעצמכם טול שיודע** [להמיר ל-LaTeX]."*

**Translation:** "No, really not. **I insist on this.**" Student: "But we won't write the code, the agent will do it." Dr. Segal: "Sure, sure, sure — you're not writing code, you're **vibe-coding**. You're supposed to **build yourself a tool** [that knows LaTeX]."

**Implication:** Overleaf SaaS is forbidden. The toolchain must be local (LuaLaTeX or XeLaTeX installed via TeX Live/MiKTeX), driven by the Python CrewAI script. The LaTeX-Producer agent is a CODE agent that calls `lualatex`/`biber` as subprocess — not a wrapper around Overleaf's API.

### 3.4 A `tex`-producer agent must be a **deliberate node in the CrewAI chain**

Line 1527–1532 (≈ 02:09):
> *"אתם בעצם בשרשרת שאני הוספתי לכם, שימו לב שאתם **צריכים להוסיף שם איזשהו סוכן שייצר לכם מלת"ח**, כן, את קבצי הנקודה [tex], הוא צריך, אתם צריכים להמיר את..."*
>
> *"In the chain I added for you, note that **you need to add some agent there that generates LaTeX for you** — the `.tex` files, you need to convert..."*

So the architecture for HW3 is **a 4th agent extension to the canonical 3-agent Researcher→Writer→Reviewer chain**. The 4th agent owns the `Markdown → LaTeX → PDF` conversion.

**Layout (matches IDEA.md already):** Researcher → Writer → Editor (= Reviewer in PDF) → LaTeX-Producer. The LaTeX-Producer Agent owns the call to the compiler tool. This is the *official* HW3 architecture per the lecture verbalization.

### 3.5 Bibliography is **explicitly part of the deliverable** (oral confirmation)

Line 1512–1514:
> *"לא לשכוח, בסוף הספר צריכה להיות **רשימת ביבליוגרפיה**. בסדר? בסוף הספר יש רשימת ביבליוגרפיה."*
>
> *"Don't forget — **there must be a bibliography list** at the end of the book. OK? At the end of the book there is a bibliography list."*

L1517–1525 explains the `.bib` format and `biber` compiler — "all comes with MiKTeX". Same on macOS with TeX Live.

### 3.6 The lecturer himself uses this exact pipeline to produce course material — the "pipe is the deliverable" rationale

Lines 1505–1507:
> *"כל הקבצים שאתם רואים פה שאני מספק לכם במודל ואני שם לכם, ככה אני מייצר אותם, אוקיי? זאת אומרת, זה בדיוק מה שאנחנו עושים, הולכים לעשות עכשיו."*
>
> *"All the files I provide on Moodle — **this is how I produce them**. So this is exactly what we're going to do now."*

Lines 1837–1838 (assignment close):
> *"אני מאוד מקווה שאתם תשמרו אחר כך את הפייפ הזה, ותוכלו להשתמש בו אחר כך בכל מקום שבו תהיו. יהיה לכם **פייפ מוכן לייצור מסמכים**."*
>
> *"I really hope you'll keep this pipe afterwards and use it wherever you go. You'll have a **ready document-production pipe.**"*

L1807–1814:
> *"כל מקום עבודה, מחר תצטרכו לייצר חשבוניות, תוכלו לעשות עם לאט"ך. יהיה לכם מסמכי PDF שקיבלתם, תצטרכו לערוך אותם עם לאט"ך. אתם פשוט לוקחים PDF, ממירים אותו ל-TX, עורכים אותו, ומחזירים אותו בחזרה."*
>
> *"Every workplace — tomorrow you'll need to produce invoices, you can do it with LaTeX. You'll have PDFs you received and need to edit with LaTeX. You just take a PDF, convert it to `.tex`, edit it, and return it. You can now do with PDFs what you could do with Word — better and at a higher level."*

**Implication for the README:** frame the project explicitly as a *document-production pipeline*, not as a one-off article generator. The README should explain how to swap in a different topic + run end-to-end — that's what makes the pipe reusable. README should also include a "Why LaTeX over Word" mini-section echoing the lecturer's reasoning.

### 3.7 Project layout for LaTeX: subdirectory inside the GitHub repo

Lines 1548–1554:
> *"מה שאתם אמורים להגיש בתוך הגיטאב זה **פרויקט שיש בו גם קרוא AI**, שאיתו, זה הבסיס שלכם, יש לכם **קוד פייתון**, כמובן, שעושה את כל הדברים, ויש לכם שם בפנים, **תקראו לזה תת-תיקייה, או תת-פרויקט, או משהו**, ששם יהיה כל המיני פרויקטון הקטן הזה של הלטקס."*
>
> *"What you need to submit on GitHub is a **project that has both CrewAI** (which is your base), **Python code** (of course) doing all the things, and inside it — **call it a sub-directory or sub-project or something** — there will be that little LaTeX project."*

**Confirms IDEA.md layout:** `latex/` subdirectory at repo root. The Python project is the parent; LaTeX is a child.

### 3.8 Whoever shows the OOP architecture in addition gets extra credit (the "ראש גדול" / "big head" bonus)

L1709–1714 verbatim:
> *"מי שמגדיל ראש גם מראה לי את הארכיטקטורה של ה-Object Oriented וכן הלאה."*
> *"**Whoever goes the extra mile** also shows me the **Object-Oriented architecture** [in the article], and so on."*

Combined with rubric R2 (mandatory class diagram), the "extra mile" path = put the same class diagram (TikZ) inside the article AND in `docs/diagrams/`. Salah & Andalus should pick this up — it's free-credit territory aligned with the grading style.

### 3.9 Reference syntax for the bibliography (Dr. Segal's exact words)

L1518–1521:
> *"יש לו פורמט שנקרא ביב, שזה הפורמט של הקבצים, זה מין XML כזה שמחזיק בפנים איך נראה כל ציטוט, כל מאמר, ואז יש קומפיילר שנקרא **ביבר**, וכל זה מגיע עם המיקטקסט."*
>
> *"It has a format called `bib`, which is the file format — kind of XML that holds what each citation looks like, each article. Then there's a compiler called **biber**, all comes with MiKTeX."*

He specifically names `biber` (modern) — not `bibtex` (legacy). **Use biber + `biblatex` package, not `\bibliography{}` + `bibtex`.** This rules out `\bibliographystyle{...}\bibliography{refs}` for HW3. Use:

```latex
\usepackage[backend=biber, style=numeric-comp, sorting=none]{biblatex}
\addbibresource{refs.bib}
...
\printbibliography
```

### 3.10 TikZ is the right tool for system diagrams (vs PNG)

L1731–1733:
> *"הספרייה הזאת שכתבתי לכם פה היא... זה לאיורים? זה בדיוק, **זה לגרפיקה, לסכמות בלוק**. אז זה בלי U. זה בלי U. זה טעות שלי, סליחה, אני עם הספלינג שלי."*
>
> *(Student): "It's for illustrations?"*
> *Dr. Segal: "Exactly — **it's for graphics, for block schematics**. So it's [TikZ] without a U." (His typo earlier was "TikUz".)*

**Implication:** TikZ for the Crew block diagram. matplotlib PNG for the data chart. Two different artifacts; don't conflate.

### 3.11 Math package — must be loaded explicitly

L1734–1736:
> *"שימו לב שאתם תצטרכו בשביל הנוסחאות, אתם צריכים לבקש, כמו בפייתון, **צריך להוסיף חבילה של מתמטיקה**, כן? חבילה בשביל לייצר את הנוסחאות."*

**Implication:** `\usepackage{amsmath, amssymb, amsthm}` in the LaTeX preamble is mandatory. The LaTeX-Producer agent must know to add this.

---

## 4. 🎬 LIVE DEMOS / EXAMPLES Dr. Segal walked through

| Demo | Lines | Approx time | HW3 use |
|---|---|---|---|
| Perplexity used as web-search engine for prep of this lecture's slides | 183–198 | 00:42 | Worth replicating: tell the Researcher agent "search with Perplexity-style breadth, then summarize". |
| Gemini Deep Research used to do the lecture's content research | 199–204 | 00:43 | Inspired pattern — Researcher agent could mimic "Deep Research" style via multi-step search loops. |
| Manus.im used to generate the slide deck itself ("Meta's AI presentation tool") | 203–204 | 00:43 | Not directly relevant for HW3 but signals "use AI all the way through the pipeline". |
| MCP/A2A architecture sketch (Cloud-as-MCP-client, dual-protocol server) | 263–373 | 00:50 | Background — neither MCP nor A2A is required for HW3. |
| Architecture deck — multi-agent system as "router → retrieval → context → reason → output → evaluation" loop | 207–216 | 00:46 | Echoes IDEA.md "Crew architecture diagram" — confirms the visualization style for the article. |
| LangChain RAG-HR worked example (PDF loader → splitter → embeddings → vector store → retriever → prompt template → ChatModel → StrOutputParser) | 866–957 | 01:27 | RAG is NOT required for HW3 (no oral mention). This is reference architecture only. |
| LCEL pipeline block diagram | 982–998 | 01:34 | The block-diagram visual style is what the article's Crew architecture diagram should mimic. |
| **9-step CrewAI walkthrough on Researcher / Writer / Reviewer building an article (the HW3 reference architecture itself)** | 1290–1406 | 01:57 | **Direct HW3 template.** The 9 steps in code match the §12.2 PDF pseudocode. Worker should clone this skeleton and extend with LaTeX-Producer (step 4) + LaTeX compilation. |
| `crew.kickoff(inputs={"topic": ...})` walkthrough — how `topic` flows through all Task descriptions | 1398–1406 | 02:01 | Implementation pattern: the `kickoff()` is called from a CLI/menu with topic as argument. |
| Live demo of an existing LaTeX project on Dr. Segal's screen (the lecture summary PDF's project structure with `main.tex` + per-chapter sub-files + `.bbl/.log/.aux` artifacts) | 1556–1577 | 02:11 | Confirms the project layout we plan: `main.tex` + per-chapter `.tex` files in subdirectory. He likes one file per chapter. |
| Drawing the word "lualatex" on screen as the recommended compiler name | 1578–1580 | 02:12 | Verbal confirmation it's `lualatex` (not `lualuatex` or other variants). |

---

## 5. ❓ STUDENT Q&A — clarifications binding for HW3

| # | Q from | Lines | Question | Answer summary |
|---|---|---|---|---|
| 1 | Amit | 502–518 | Should I implement orchestration myself using gRPC/processes (HW2-style), or use a framework like LangChain? | "For PoC and small systems, your custom IPC approach is fine. For something destined for production / wider distribution / reliability — use platforms like LangChain/CrewAI. You're not required to use the platform for HW2 — but HW3 you are." |
| 2 | Roi | 660–673 | For HW2 — do I pick the debate topic, or do you choose? | "You pick. If you let me pick, that bumps difficulty a bit and could raise the grade slightly, but it's not required." *(HW2 context — not directly HW3.)* |
| 3 | (unattributed) | 674–728 | About HuggingFace models — license issues, virus risk? | "Excellent point. Always check the license; check community reputation. Use Perplexity to research the package's reception." Not HW3-directly-binding but background. |
| 4 | Maor | 728–757 | If I use the API key (not Claude CLI login), is the `.claude/agents/` structure irrelevant? Do I just provide System Prompt directly? | "Yes — when you work with API keys you must manage Context Window, RAG, etc. yourself. That's exactly what LangChain helps you with. When you log into the CLI, the agents folder is alive; with API key, you manage everything via your code." |
| 5 | **Yair** | **1601–1602, 1675–1702** | **What's the page count requirement?** | **Negotiated live to 15 pages.** See §1.1 above. |
| 6 | **Roi** | **1613–1631** | **Do I have to write in Hebrew? It's hard for me — I'd prefer English only.** | **"You may write the whole document in English; just include ONE chapter mixing Hebrew and English to demonstrate BiDi."** See §1.2 above. |
| 7 | **Roi (cont'd)** | **1631–1633** | **Is there a template you prefer? Banners?** | **"No, use what you want — even from your other work. I encourage personal reuse."** |
| 8 | **Roi** | **1644–1660** | **Why not write directly in LaTeX? Markdown also needs compilation.** | **Markdown is faster to iterate; LaTeX recompile is slow especially with `.bib` (4 passes). Get content right in Markdown first, convert to LaTeX as a final step. "This is my working method."** |
| 9 | **(student)** | **1704–1706** | **Does it matter if I use `xelatex` vs `lualatex`?** | **"No, it doesn't matter to me at all."** |
| 10 | **(student)** | **1715–1731** | **Confirming the library name for block schematics?** | **TikZ (he initially mis-spelled "TikUz" and corrected himself). It's a LaTeX library, not Python.** |
| 11 | **(student)** | **1760–1810** | **Can I use my existing research paper as the seed?** | **"You can — but the project must be self-contained and reproducible. If you have results/tables and don't want to commit them to the repo, that's legitimate but then you need to pick a different topic. The reproducibility-from-the-repo rule is binding."** |
| 12 | **Yair** | **1815–1835** | **Are we graded on correctness of the article? Whether the claims are true?** | **"No, I do not read the article. I check the technical envelope — links resolve, citations exist, tables fit. Plausible-looking text is fine; even AI-generated body is fine. I don't check if you wrote 'Israel founded 1949 instead of 1948'."** SEE §3.1 — this is the load-bearing grading statement. |
| 13 | **(student)** | **1839–1850** | **Does my topic choice matter, or just the formatting?** | **"Formatting is what matters technically, but there must be logical coherence in the topic — you can't have chapter 1 on lettuce farming and chapter 2 on equations of love. The article must look like an article."** |

---

## 6. 📅 DEADLINES, SCOPE, GRADING — from the lecture itself

### 6.1 Deadline confirmation

Line 1605–1607 (≈ 02:13):
> *"כמובן שאני אפרסם לכם מקום במודל ושם תוכלו להגיש, כרגיל, עם אותו נוהל שתמיד מגישים, **עבודה בזוגות, תמיד מהיום שאני מפרסם, שבועיים הגשה**, כל הדברים הרגילים."*
>
> *"I'll publish a location on Moodle where you'll submit — same procedure as always — **pairs**, always **two weeks from the day I publish**, all the usual."*

**Calendar check:** This lecture is dated 29 May 2026 (per the spec PDF). Two weeks later = **12 June 2026**. The orchestrator's HW3 deadline of **Friday 2026-06-12 23:59** is **confirmed**. ✅

### 6.2 Pairs work; solo not mentioned

Line 1605: *"עבודה בזוגות"* — pair work. Same as HW2. Salah + Andalus configuration unchanged.

### 6.3 Attendance check

Line 1608–1611:
> *"בדיקת הנוכחות, מי ששאל זה רשימת המשתמשים פה בזום."*
> *"Attendance check — whoever's on the Zoom user list."*

Just a reminder; not HW3-binding.

### 6.4 Grade weight & scoring philosophy (technical envelope)

Reconfirmed verbatim (L1823–1835). See §3.1.

**Specific things he'll look for (from the lecture):**
1. Hyperlinked references that actually jump (`hyperref` + 4 compilations).
2. Citations resolve (no `[?]` in the PDF).
3. BiDi chapter renders correctly (Hebrew RTL, English LTR, mixed paragraphs flow logically).
4. Tables don't overflow the page.
5. Formulas are "fancy" (math-mode rendered, not plain text).
6. Cover sheet has all 5 fields, is "dignified".
7. Headers and footers exist (`fancyhdr` or similar).
8. Table of Contents is present.
9. Chapter structure is visible.
10. Bibliography exists at the end.
11. ≥1 image, ≥1 Python-chart, ≥1 table, ≥1 formula.
12. README explains the Crew architecture.
13. The pipe is reusable (can swap topic and re-run).

**Specific things he'll NOT look for:**
- Whether claims are true (L1832 — verbatim quoted above).
- Page count above 15 (L1702 — 15 is settled; above is fine but not credit-bearing).
- LuaLaTeX vs XeLaTeX (L1704–1706).
- Hebrew vs English in the body (L1622–1629, English fine with BiDi chapter).
- Whether the agents argue / cooperate / use specific Skills (no oral mention; Skills feature is from the spec PDF Appendix A, not from this lecture's oral spec).

---

## 7. 🧠 PHILOSOPHY threads for the worker to internalize

### 7.1 "Senior architect, not junior coder" — the OOP-as-management mindset

Lines 989–1035 (≈ 01:36) — extended monologue:
> *"כשאתם רוצים לנהל פרויקט, הדרך לנהל היא לבנות את הפרויקט בקוביות כאלה... זה נקרא **ניהול ארגוני**, כי בעצם אתם מגדירים מה בכניסה, אתם מגדירים מה ביציאה, ופה למטה אתם מגדירים איזה סט-אפ, איזה קונפיגורציה."*
>
> *"When you want to manage a project, the way to manage is to build it in such cubes... It's called **organizational management**. You define what's at the input, what's at the output, and below — what setup, what configuration."*
>
> *"אתם יודעים שהיום בתעשייה לא מגייסים ג'וניורים... היא מחפשת רק סיניורים. וסיניור — זה מה שאנחנו מנסים ללמוד פה בקורס. בעצם, אתם לומדים לנהל צוותים. הצוותים שלכם זה הסוכני AI. אתם לומדים לחשוב לא כתכנתים, אלא **כארכיטקטים של תוכנה**."*
>
> *"You know that today the industry doesn't hire juniors. It only wants seniors. And a senior is what we're trying to learn here. You're learning to manage teams — your teams are the AI agents. You're learning to think not as programmers but **as software architects**."*

**Implication for HW3:** the docs/PRD must explicitly frame the user as "architect of the writing crew", not as "programmer of an automation script". This is also why `docs/PLAN.md` must include the ISO/IEC 25010 paragraph (HW2 pattern) and the C4 model — those are senior-level artifacts.

### 7.2 "Divide and conquer is the philosophical secret" — modular task breakdown

Lines 226–245 (≈ 00:48):
> *"מי שלא יודע, מישהו יודע איך פותרים בעיה מסובכת? **מפרקים אותה לבעיות יותר קטנות**... תמיד ניגשים אליה בצורה נורא פשוטה, אומרים תשמע את כל הדברים האחרים נניח שפתרתי את זה, עובדים בסופר-פוזיציה... מי שמקפידה בגישה הזאת, יש לכם סיכוי אדיר בזמן קצר להגיע לתוצאות איכותיות."*
>
> *"How do you solve a complex problem? **You break it into smaller problems.** You always approach it simply — assume the other things are solved, work in superposition, then solve the small piece. Whoever sticks to this approach has a tremendous chance of reaching quality results quickly."*

**Implication:** the TODO.md should reflect this — each task tackles ONE small piece. Sub-tasks for "compile pipeline" should be granular: install deps → run lualatex once → run biber → check log for missing refs → run lualatex N+1 → grep for warning patterns → produce PDF.

### 7.3 Positive vs Negative AI Economy — the Human-in-the-Loop dictum

Lines 1085–1102 (≈ 01:43):
> *"חבר'ה, תזכרו משפט. אנחנו קוראים, יש **כלכלת AI חיובית ושלילית**. כלכלת AI חיובית זה כשיש אדם בלופ. אין מצב שהסוכן אוטונומי לחלוטין. תמיד יש נקודות בקרה. כלכלת AI שלילית זה שהסוכנים עובדים בלולאה ללא בקרה."*
>
> *"Folks, remember this sentence. There is **positive and negative AI economy**. Positive AI economy is when there's a human in the loop. There's no case where the agent is fully autonomous. There are always control points. Negative AI economy is when agents work in a loop with no control."*
>
> *"אחד הדברים הראשונים שאתם אמורים לעשות כשתגיעו לארגון שלכם, לחפש מקומות שהסוכנים עובדים בלולאה ללא בקרה. **זה מצב חמור ביותר**."*

**Implication for HW3:** the CrewAI pipeline must have at least ONE human-in-the-loop checkpoint, ideally between the Editor agent's approval and the LaTeX-Producer's commit-to-compile step. Implementation: pause in the menu CLI asking "Approve final Markdown? [y/N]" before compiling. This earns "production discipline" credit without significant cost.

### 7.4 Versioning is sacred — everything has a version

Lines 1117–1138 (≈ 01:45):
> *"מכיוון שאנחנו מדברים על דברים מודולריים... המודול הזה צריך לקבל ורסיות, והמודול הזה גם עובד עם סט-אפים, **והקונפיגורציות עצמן צריכות לקבל גרסאות**. זאת אומרת, ואם אתם עובדים עם בסיסי נתונים בכלל, ועם רגים בפרט, **חייבה להיות גרסה**. גרסה לסכמה, גרסה כל הזמן... הפרויקט שלכם חייב להכיל אוסף של גרסאות. אין דבר כזה להחזיק רק גרסה אחת."*

**Implication for HW3:** the `__version__` constant carries from HW1/HW2; new in HW3 — version every config file (`config/agents.json: {"version": "1.00"}`), version the LaTeX template, version the bibliography style. Document the version-bump policy in PLAN.md.

### 7.5 PoC ≠ Production — explicit gap

Lines 148–173 (≈ 00:38):
> *"כל מה שאתם עושים פה בקורס זה ברמת Proof of Concept. כי אין לכם שום הוכחה שאם נריץ את זה עשרת אלפים פעם התוצאות יהיו עקביות... ה-PoC לא שווה כלום, ה-PoC זה רק הוכחה. אתם חייבים להריץ אותו המון כי אל תשכחו כל האג'נט הוא **מודל הסתברותי**."*

**Implication:** the README's "Limitations" section should explicitly state: "This is a PoC. We tested with N runs; for production deployment, see §X for the runbook to scale to 10⁴ runs/day." Even a one-paragraph nod earns the maturity-signal credit.

### 7.6 Observability is mandatory, not optional

Lines 426–438 (≈ 01:02):
> *"זה observation. Observation, observation, זה ניטור, ניטור, ניטור... חייב להיות מעקב מלא כדי לדעת מדוע סוכן בחר בפעולה כמה היא עלתה ומה השתבש."*
>
> *"That's observation. Observation, observation — monitoring, monitoring, monitoring... There must be full tracking to know why the agent chose an action, how much it cost, and what went wrong."*

**Implication:** every CrewAI agent invocation must be logged with timestamp, tokens used, cost, and outcome to a structured log. FIFO log rotation (HW2 default of 20 files × 500 lines) applies here too.

### 7.7 "Modular = production-ready; hardcoded = dead on arrival"

Lines 479–493 (≈ 01:05):
> *"מודולריות. הפייפ שלכם חייב להיות מודולרי. זאת אומרת, אין דבר כזה שאני תלוי באיזה מודל מסוים. אני צריך בקונפיגורציה להחליף את המודל... זה הכל בסט-אפ. **זה לא משהו שצריך להיות hard-coded**."*

**Implication:** zero hardcoded LLM provider strings, model names, temperatures, page counts, page-margins, font names. All from `config/*.json`. Carries over the HW2 rule.

### 7.8 The recommended Markdown-first workflow IS the philosophy

L1644–1660 above. The point of Markdown-first isn't speed alone — it's that **debugging is faster on legible artifacts**. This generalizes: in agent pipelines, always have a stage that produces a human-readable artifact even if the final output is a binary/PDF.

### 7.9 Bonus heuristic — "going the extra mile" earns visible credit

Three explicit uses of *"מי שמגדיל ראש"* / "the one who enlarges his head" / "extra mile":
- L1709: extra OOP architecture diagram inside the article
- L1714: extra block schematics in the PDF
- (HW1/HW2 lectures had similar phrasing)

The pattern: **identifying and EXECUTING one nice-to-have beyond the spec is the cleanest way to push grade above the floor.** For HW3, candidate extras:
- TikZ class diagram inside the article body
- A "How we built this" appendix narrating the pipeline (meta)
- A cost analysis section with token-count tables (echoes the lecturer's "spec sheet" idea, L463–468)
- A 2nd Python-generated chart (bonus, not mandated)
- A `Makefile` that does end-to-end `make pdf` reproducibly (this is honestly table-stakes for a "production" pipe)

---

## 8. 📊 LECTURE STRUCTURE — where to find verbatim quotes

| Section | Lines | Approx time | Topics covered |
|---|---|---|---|
| **A. Opening framing** | 1–37 | 00:17:40 → 00:21 | Course arc retrospective: deep learning → transformers → agents → IPC → production. Promises today: presentation overview + LangChain + CrewAI if time + HW3 spec. Mention that final project occurs during exam period in two submission windows. |
| **B. Agent Architectures 2026 — backdrop** | 38–245 | 00:21 → 00:48 | 2026 agentic turning point. Harness components (planner/memory/RAG/tools/MCP/observability). LangChain vs LangGraph one-line diff. Provider vs On-Prem vs Cloud trade-offs. Ollama-as-VLC analogy. HuggingFace as "movie library". GPU memory > GPU itself ("write in white letters"). $50k server cost example (Bank Leumi project). Three-options decision matrix. |
| **C. Code Agents and Sandboxing** | 125–173 | 00:36 → 00:43 | Smolagents pattern (Python instead of JSON IPC). Windows Sandbox + WSL. PoC ≠ Production dictum. Memory/PoC bug-multiplication. |
| **D. MCP / A2A protocols** | 246–373 | 00:48 → 00:58 | MCP as "Skill wrapping Tool, for advanced users". MCP server vs client. Dual protocol architecture (client+server on both ends). A2A for agent-to-agent comm. Vendor-lock warning if not using open protocols. |
| **E. Agent Security** | 374–461 | 00:58 → 01:05 | OWASP Top 10 for agentic apps: prompt injection, tool misuse, identity abuse, memory poisoning. IBM-co-developed system "schooled" by a gifted teen with a few prompts (anecdote, L439–457). Red Team mandate. |
| **F. Spec Sheets and TCO** | 462–478 | 01:05 → 01:06 | Cost of agent ≠ just tokens. Latency, memory, throughput as a "Spec Sheet". When buying AI services — these are the questions to ask. |
| **G. Modularity, scalability, permissions, measurement** | 479–495 | 01:06 → 01:06 | Summary mantra: modular pipeline, swap models via config, version everything, observability everywhere. |
| **H. Break and Q&A** | 495–760 | 01:06 → 01:22 | Q from Amit on custom IPC vs LangChain (custom is fine for PoC, framework for production). Q on Gemma 3 inference time discrepancy (Dr. Segal's PhD anecdote about ChatGPT discovering EfficientNet for small images — L611–656). Q on choosing debate topic for HW2. Q on HuggingFace license/virus risk. Q on CLI vs API differences. |
| **I. LangChain Deep Dive (Harness defined)** | 760–960 | 01:22 → 01:32 | LangChain = Model + Harness. Harness as "the whole human, LLM is just the brain". RAG-HR worked example walkthrough (Document Loader → Splitter → Embeddings → Vector Store → Retriever → PromptTemplate → ChatOpenAI/ChatOllama → StrOutputParser). NotebookLM as a real-world version of this. LCEL (LangChain Expression Language) as the connecting tissue. |
| **J. Senior-architect monologue** | 989–1035 | 01:36 → 01:38 | The block/cube management metaphor. "Industry doesn't hire juniors — you're learning to be seniors / software architects, not programmers." |
| **K. LCEL benefits and Agent vs Chain** | 1036–1083 | 01:38 → 01:42 | Modular composition. Agent picks tools dynamically; Chain is linear. The more dynamic the task, the higher Agent's value. Human-in-the-Loop intro. |
| **L. Positive / Negative AI Economy** | 1084–1103 | 01:42 → 01:43 | The dictum: "Positive = human-in-loop; Negative = unmonitored loop is a SERIOUS condition." |
| **M. LangChain summary + limitations** | 1104–1149 | 01:43 → 01:46 | Why orgs pick LangChain: modularity, speed, integrations. Risks: complexity, versions (acute!), debugging, answer quality. "Versions versions versions" sermon. |
| **N. CrewAI introduction** | 1150–1230 | 01:46 → 01:51 | Pivot to CrewAI. "Crew turns one prompt into a team." Four building blocks: Agent, Task, Crew, Process. Each agent has role / goal / backstory / tools. Tasks have description / expected_output / agent / context. Crew connects them. Process = sequential vs hierarchical. |
| **O. CrewAI: Sequential and Hierarchical** | 1244–1287 | 01:51 → 01:55 | Sequential = each task waits for previous (researcher → writer → reviewer). Hierarchical = Manager Agent decides what runs when. Context = the glue. `verbose=True` to see runs. |
| **P. 9-step CrewAI pseudocode walkthrough** | 1288–1406 | 01:55 → 02:01 | Step-by-step: Tool → 3 Agents (researcher / writer / reviewer) → 3 Tasks → Crew → kickoff. `inputs={"topic": ...}` flows through Task descriptions. Result is the final article + token tracking. |
| **Q. HW3 ASSIGNMENT (oral, the binding spec)** | 1407–1601 | 02:02 → 02:13 | "You need to write an article — choose a topic. There are levels. In Hebrew up to 30 pages, English up to 50 — Hebrew harder so I'll extend it more. BiDi (bidirectional) chapter required. PDF deliverable with cover sheet, headers/footers, ToC, chapters. ≥1 image, ≥1 Python-chart, ≥1 table, ≥1 formula. LaTeX mandatory (Overleaf forbidden — "I insist"). MiKTeX/TeX Live, LuaLaTeX recommended for Hebrew. TikZ for diagrams. Math package for formulas. **Fancy formula, not plain text**. Markdown-first workflow. 4 compilations for cross-refs. Submit on GitHub: Python project + `latex/` sub-project. Two weeks deadline." |
| **R. HW3 Q&A (the resolution-rich section)** | 1601–1855 | 02:13 → 02:27 | All the bindings above: page count negotiated to 15. English fine with BiDi chapter. XeLaTeX OK. Use existing research IF source committed. Template free. Topic must be coherent. **"I don't read the article — I check the envelope."** **"Israel founded 1949 not 1948 — I don't check."** "Keep this pipe — it's a document-production tool for any workplace." Closing salutations. |
| **S. Closing pleasantries** | 1856–1859 | 02:27 → 02:28 | "תודה רבה לכם, שבת שלום." |

---

## 9. ⚡ CRITICAL SUMMARY — apply these to IDEA.md immediately

The 14 changes the worker must make:

| # | Change | Source | Severity |
|---|---|---|---|
| 1 | Page count = 15 (settled in class), plan 14–17 | §1.1 / L1702 | High |
| 2 | English article + 1 BiDi chapter is fully acceptable | §1.2 / L1622–1629 | High — neutralizes "Hebrew everywhere" pressure |
| 3 | XeLaTeX equal to LuaLaTeX; no preference difference | §1.3 / L1706 | Medium |
| 4 | Article PDF must contain a TikZ Crew architecture block diagram | §1.4 / L1708–1714 | High |
| 5 | Bonus: also include OOP class diagram inside the PDF | §1.5 / L1709 | Medium (extra-mile credit) |
| 6 | Bibliography compile loop is EXACTLY 4 passes (with biber); failure mode is broken hyperlinks | §1.6 / L1670–1674 | High |
| 7 | LaTeX is mandatory; Overleaf forbidden ("I insist") | §3.3 / L1473 | High |
| 8 | LaTeX-Producer agent is a separate node in the chain, owns the compile call | §3.4 / L1527–1532 | High — affects architecture diagram |
| 9 | Use `biblatex` + `biber`, not legacy `bibtex` | §3.9 / L1524 | Medium |
| 10 | Math package (`amsmath`) mandatory in preamble | §3.11 / L1734–1736 | Low |
| 11 | LaTeX-Producer prompt must include verbatim **"fancy formula, not plain text"** | §3.2 / L1742–1748 | High — common failure mode |
| 12 | Skip web-search-tool mandate from HW2 (no oral mention here); make it optional / use DDG fallback | §2.7 / no oral mention | Medium |
| 13 | Same LLM provider across all agents (no bonus for mixing) | §2.3 | Medium |
| 14 | Sequential Process is correct default; Hierarchical NOT a bonus path (just risk) | §2.4 / L1273 | Medium |

Plus the four philosophical anchors for the README and docs/PLAN:
- **A. Pipe is the deliverable** (§3.6) — frame the README around "this is a reusable document-production pipeline".
- **B. Senior architect mindset** (§7.1) — PLAN.md must explicitly frame Salah & Andalus as architects.
- **C. Envelope, not content** (§3.1) — token budget should NOT be spent on fact-checking; should be spent on link/table/formula plumbing.
- **D. Human-in-loop checkpoint** (§7.3) — one menu-driven pause before final compile.

---

## 10. 📚 Hebrew → English glossary (HW3-specific terms from this lecture)

| Hebrew | English | Domain meaning in HW3 |
|---|---|---|
| הרנס / Harness | Harness | Whole agent runtime (LLM + prompt + context + tools + memory) |
| לטקס / לאט"ך / לתך | LaTeX | THE document typesetting language |
| מיקטקס | MiKTeX | LaTeX distribution (Win); on macOS use MacTeX/TeX Live |
| לולה טקס | LuaLaTeX | Compiler engine, good Hebrew support, Dr. Segal's preference |
| ביב | `.bib` / BibTeX format | Bibliography file format |
| ביבר | biber | Modern bibliography compiler (use this, not bibtex) |
| טיקסי | TikZ | LaTeX package for diagrams/schematics |
| פנסי פורמולה | fancy formula | Math-mode-rendered equation (vs. plain text) |
| BD / B-Directional | BiDi | Bidirectional text (Hebrew RTL + English LTR mixing) |
| ימין-שמאל | RTL | Right-to-Left |
| שמאל-ימין | LTR | Left-to-Right |
| הבלאגן | the formatting balagan | Roi's word for "the BiDi typesetting headache" |
| קאבר-שיט | Cover Sheet | Title page |
| תוכן עניינים | Table of Contents | `\tableofcontents` |
| חלוקה לפרקים | Chapter division | `\section{}` or `\chapter{}` |
| הדרים ופוטרים | Headers and Footers | `fancyhdr` package output |
| ביבליוגרפיה | Bibliography | `.bib` + `\printbibliography` |
| ציטוטים מקושרים | Linked citations | `hyperref`-enabled cite refs |
| המעטפת | The envelope | What Dr. Segal grades (vs. content) |
| הפייפ | The pipe(line) | What Dr. Segal wants Salah to keep & reuse |
| ראש גדול / להגדיל ראש | Big head / Extra mile | The bonus-credit move |
| מאמר | Article | The deliverable |
| ספר | Book | Synonym for article in HW3 context (Dr. Segal uses interchangeably, L1510) |
| צוות | Crew / Team | CrewAI top-level container |
| סוכן | Agent | CrewAI Agent class |
| משימה | Task | CrewAI Task class |
| תהליך | Process | CrewAI Process enum |
| תפקיד / רול | Role | Agent `role=` |
| מטרה / גול | Goal | Agent `goal=` |
| סיפור רקע / בק סטורי | Backstory | Agent `backstory=` (acts as system prompt) |
| כלי / טול | Tool | Agent `tools=[]` |
| מומחיות | Specialization | Sometimes refers to skills, sometimes to role |
| הקשר / קונטקסט | Context | Task `context=[prev_task]` — Dr. Segal calls this "the glue" |
| סקוונשל | Sequential | `Process.sequential` |
| היררכי | Hierarchical | `Process.hierarchical` |
| מנג'ר אייג'נט | Manager Agent | Hierarchical mode's dispatcher |
| קומפיילר | Compiler | LaTeX engine |
| קומפילציה | Compilation | One pass through the engine |
| ייצור / פרודקשן | Production | Live system (vs. PoC) |
| הוכחת היתכנות / PoC | Proof of Concept | What HW3 actually is |
| פלייר (וידאו) | Player (VLC analogy) | Ollama, in Dr. Segal's metaphor |
| הזיות | Hallucinations | LLM errors |
| ניטור / Observation | Monitoring | Logging, tracing, evals — mandatory |
| פלאג-אין | Plug-in | Modular swap-ability |
| מגירה | Drawer | Module — Dr. Segal's "swap a drawer in and out" image |
| מודולריות | Modularity | The core principle |
| גרסה / ורסיה | Version | Must be on every module + config |
| כלכלת AI חיובית/שלילית | Positive/Negative AI Economy | With/without Human-in-the-Loop |
| אדם בלולאה | Human-in-the-Loop | Control point in pipeline |

---

## 11. 📍 PROOF OF FILE WRITE

This file written to:
`/Users/salah/Projects/orch-ai-agents/hw3/CONTEXT-lecture-06.md`

Source transcript:
`/Users/salah/Projects/orch-ai-agents/lectures/lecture-06-langchain-crewai.txt` (1860 lines, 128 KB)

Timestamped source for verbatim quotes:
`/Users/salah/Projects/orch-ai-agents/lectures/lecture-06-langchain-crewai.srt` (1860 caption blocks, spans 00:17:40 → 02:28:09)

Mirror pattern (HW2 analog):
`/Users/salah/Projects/orch-ai-agents/hw2/CONTEXT-lecture-05.md`

Worker instructions in this directory:
`/Users/salah/Projects/orch-ai-agents/hw3/CLAUDE.md` — points the worker at IDEA.md / RULES.md / CONTEXT-lec06-pdfs.md / this file as the read-order spine.

— end of digest —
