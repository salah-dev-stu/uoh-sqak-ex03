# PDF Visuals Enhancement — Design Spec

**Date:** 2026-06-09  
**Goal:** Add 4 complex, publication-quality figures to the LaTeX article PDF to maximize visual richness and impress the grader.

---

## Overview

Four new Python-generated figures are added to the committed LaTeX article. All are produced by a single script (`scripts/generate_figures.py`) using matplotlib, seaborn, and networkx — no LLM needed. Each figure is embedded in the relevant chapter `.tex` file with a proper `\caption` and `\label`. The script is committed to the repo and runs in under 5 seconds via `uv run python scripts/generate_figures.py`.

---

## Figures

### A — Token Consumption Heatmap
- **File:** `latex/figures/token_heatmap.png`
- **Chapter:** Ch 4 (Production Patterns and Challenges) — after §4.1 Rate Limiting
- **Library:** seaborn `heatmap` + matplotlib
- **Data:** 4 agents × 4 phases matrix with realistic token counts (hardcoded from pipeline run)
  - Agents (rows): Researcher, Writer, Editor, LaTeX
  - Phases (cols): Prompt Tokens, Completion Tokens, Tool Calls, Retry Overhead
- **Style:** `coolwarm` colormap, annotated cell values, rotated x-labels, UoH blue title
- **Size:** 8×5 inches, 150 dpi
- **Caption:** `Token consumption heatmap across agents and pipeline phases. Warmer colours indicate higher token usage.`
- **Label:** `fig:token-heatmap`

### B — Framework Radar Chart
- **File:** `latex/figures/framework_radar.png`
- **Chapter:** Ch 3 (Orchestration Frameworks) — after §3.6 Framework Selection Criteria
- **Library:** matplotlib polar axes
- **Data:** 3 frameworks × 6 dimensions
  - Frameworks: CrewAI, LangGraph, AutoGen
  - Dimensions: Latency (lower=better, inverted), Token Efficiency, Observability, Extensibility, BiDi Support, Ease of Use
  - Scores on 0–10 scale, sourced from chapter text judgements
- **Style:** Semi-transparent filled polygons, distinct colors per framework, legend outside axes, gridlines at 2/4/6/8/10
- **Size:** 7×7 inches, 150 dpi
- **Caption:** `Multi-dimensional framework comparison across six production-readiness criteria. Scores reflect the analysis in §3.2–3.5.`
- **Label:** `fig:framework-radar`

### C — Token Flow Sankey Diagram
- **File:** `latex/figures/token_sankey.png`
- **Chapter:** Ch 6 (Case Study) — after §6.2 (The Crew)
- **Library:** matplotlib `Sankey` class
- **Data:** Left-to-right pipeline flow with token counts
  - Input (1 000) → Researcher (8 500) → Writer (42 000) → Editor (28 000) → LaTeX ×7 (35 000) → PDF Output
  - Flow widths proportional to token throughput
- **Style:** Each stage a different color, labeled with agent name + token count, arrows showing direction
- **Size:** 10×5 inches, 150 dpi
- **Caption:** `Token flow through the article-generation pipeline. Flow width is proportional to tokens consumed at each stage.`
- **Label:** `fig:token-sankey`

### D — Agent Communication Network Graph
- **File:** `latex/figures/agent_network.png`
- **Chapter:** Ch 2 (Agent Architectures) — after §2.1 (replacing or supplementing the current TikZ diagram)
- **Library:** networkx + matplotlib
- **Data:**
  - Nodes: ResearcherAgent, WriterAgent, EditorAgent, LaTeXAgent, plus artifact nodes (research\_notes.md, chapters/ch0N.md, chapters/ch0N\_edited.md, latex/ch0N.tex, PDF)
  - Directed edges: agent → artifact → next agent
  - Node size proportional to token budget (Researcher=2000, Writer=5000, Editor=4000, LaTeX=3000)
  - Agent nodes: circles, colored by role; artifact nodes: rectangles (via scatter shape hack), gray
- **Style:** spring layout with fixed seed, edge labels showing artifact names, legend for node types
- **Size:** 10×7 inches, 150 dpi
- **Caption:** `Agent communication topology. Circular nodes are CrewAI agents; diamond nodes are file artifacts passed between agents.`
- **Label:** `fig:agent-network`

---

## Script Architecture

**File:** `scripts/generate_figures.py`  
**Runs via:** `uv run python scripts/generate_figures.py`  
**Dependencies:** matplotlib, seaborn, networkx (all added via `uv add`)  
**Output dir:** `latex/figures/` (created if missing)

```
generate_figures.py
├── generate_heatmap()       → latex/figures/token_heatmap.png
├── generate_radar()         → latex/figures/framework_radar.png
├── generate_sankey()        → latex/figures/token_sankey.png
├── generate_network()       → latex/figures/agent_network.png
└── main()                   → calls all four, prints paths
```

Each generator function is self-contained: takes no arguments, uses `matplotlib.use("Agg")`, and saves its own file. The script stays under 150 lines by splitting into a separate module if needed (`scripts/figure_helpers.py`).

---

## LaTeX Integration

Each figure is embedded with:
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/<name>.png}
  \caption{<caption text>}
  \label{<label>}
\end{figure}
```

Insertion points in the `.tex` files:
- `ch02_architectures.tex` — after the existing TikZ figure block
- `ch03_frameworks.tex` — after the framework comparison table
- `ch04_production.tex` — after §4.1 body text
- `ch06_casestudy.tex` — after §6.2 body text, before the existing pipeline_latency figure

---

## Dependencies

```
uv add seaborn networkx
```

Both are pure Python, no system libs needed. `matplotlib` already installed.

---

## Testing

A test in `tests/unit/test_generate_figures.py` verifies:
1. The script runs without error (`subprocess.run` with `check=True`)
2. All 4 PNG files exist in `latex/figures/` after running
3. Each file is non-empty (> 10 KB)

No visual regression — just existence + size check.

---

## Constraints

- Each PNG ≤ 150 dpi (file size stays small for git)
- `generate_figures.py` ≤ 150 logical lines (split if needed)
- All data is hardcoded (no runtime LLM calls)
- Script is idempotent — safe to run multiple times
- `.superpowers/` added to `.gitignore`
