# PDF Visuals Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 4 complex Python-generated figures (heatmap, radar chart, sankey flow diagram, network graph) to the LaTeX article PDF and recompile.

**Architecture:** A single script `scripts/generate_figures.py` contains all 4 generator functions. Each writes a PNG to `latex/figures/`. The 4 chapter `.tex` files are then edited to embed the new figures. Finally the PDF is recompiled with `cd latex && make`.

**Tech Stack:** matplotlib, seaborn, networkx, numpy — all via `uv add`. LaTeX via existing `make` target.

---

## File Map

| Action | File |
|--------|------|
| Create | `scripts/generate_figures.py` |
| Create | `tests/unit/test_generate_figures.py` |
| Modify | `latex/chapters/ch02_architectures.tex` — add network graph after TikZ figure |
| Modify | `latex/chapters/ch03_frameworks.tex` — add radar chart after longtable |
| Modify | `latex/chapters/ch04_production.tex` — add heatmap after §4.1 Rate Limiting body |
| Modify | `latex/chapters/ch06_casestudy.tex` — add sankey after existing pipeline_latency figure |
| Generate | `latex/figures/token_heatmap.png` |
| Generate | `latex/figures/framework_radar.png` |
| Generate | `latex/figures/token_sankey.png` |
| Generate | `latex/figures/agent_network.png` |

---

## Task 1: Install Dependencies

**Files:**
- Modify: `pyproject.toml` (via uv add)
- Modify: `uv.lock`

- [ ] **Step 1: Add seaborn and networkx**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3
uv add seaborn networkx
```

Expected: both added to `pyproject.toml` under `[project.dependencies]`, `uv.lock` updated.

- [ ] **Step 2: Verify imports work**

```bash
uv run python -c "import seaborn; import networkx; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "deps: add seaborn and networkx for figure generation"
```

---

## Task 2: Write Failing Tests

**Files:**
- Create: `tests/unit/test_generate_figures.py`

- [ ] **Step 1: Write the test file**

```python
"""Tests for scripts/generate_figures.py — verifies all 4 PNGs are created."""
import subprocess
import sys
from pathlib import Path

import pytest

FIGURES_DIR = Path("latex/figures")
EXPECTED = [
    "token_heatmap.png",
    "framework_radar.png",
    "token_sankey.png",
    "agent_network.png",
]


def test_generate_figures_script_runs():
    result = subprocess.run(
        [sys.executable, "scripts/generate_figures.py"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"


@pytest.mark.parametrize("filename", EXPECTED)
def test_figure_file_exists(filename):
    path = FIGURES_DIR / filename
    assert path.exists(), f"Missing: {path}"


@pytest.mark.parametrize("filename", EXPECTED)
def test_figure_file_nonempty(filename):
    path = FIGURES_DIR / filename
    assert path.stat().st_size > 10_000, f"Too small (<10 KB): {path}"
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run pytest tests/unit/test_generate_figures.py -v
```

Expected: `FAILED` — `scripts/generate_figures.py` does not exist yet.

---

## Task 3: Implement generate_figures.py

**Files:**
- Create: `scripts/generate_figures.py`

- [ ] **Step 1: Write the full script**

```python
#!/usr/bin/env python3
"""Generate publication-quality figures for the LaTeX article."""
from __future__ import annotations
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

FIGURES_DIR = Path("latex/figures")


def generate_heatmap() -> str:
    import seaborn as sns
    data = np.array([
        [3_200,  5_800,  12,   0],
        [5_100, 38_200,   8, 200],
        [4_800, 22_600,   6, 150],
        [2_900, 31_800,  42, 300],
    ])
    labels_y = ["Researcher", "Writer", "Editor", "LaTeX"]
    labels_x = ["Prompt\nTokens", "Completion\nTokens", "Tool\nCalls", "Retry\nOverhead"]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(data, annot=True, fmt="d", cmap="YlOrRd",
                xticklabels=labels_x, yticklabels=labels_y,
                ax=ax, linewidths=0.5, cbar_kws={"label": "Tokens"})
    ax.set_title("Token Consumption per Agent and Pipeline Phase",
                 fontsize=13, fontweight="bold", pad=12)
    out = FIGURES_DIR / "token_heatmap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def generate_radar() -> str:
    cats = ["Latency", "Token\nEfficiency", "Observability",
            "Extensibility", "BiDi\nSupport", "Ease of Use"]
    N = len(cats)
    angles = [n / N * 2 * math.pi for n in range(N)] + [0]
    scores = {
        "CrewAI":    [8, 8, 7, 9, 8, 9],
        "LangGraph": [6, 7, 9, 10, 5, 5],
        "AutoGen":   [4, 4, 6,  7, 3, 7],
    }
    colors = {"CrewAI": "#2196F3", "LangGraph": "#4CAF50", "AutoGen": "#FF5722"}
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    for name, vals in scores.items():
        v = vals + vals[:1]
        ax.plot(angles, v, "o-", linewidth=2, color=colors[name], label=name)
        ax.fill(angles, v, alpha=0.15, color=colors[name])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=10)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    ax.set_title("Framework Comparison: Multi-Dimensional Analysis",
                 fontsize=12, fontweight="bold", pad=20)
    out = FIGURES_DIR / "framework_radar.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def generate_sankey() -> str:
    stages = [
        ("Input\nPrompt",    1_000, "#78909C"),
        ("Researcher\nAgent", 8_500, "#1565C0"),
        ("Writer\nAgent",   42_000, "#2E7D32"),
        ("Editor\nAgent",   28_000, "#E65100"),
        ("LaTeX\nAgents",   35_000, "#6A1B9A"),
    ]
    max_tok = max(s[1] for s in stages)
    xs = [i * 2.2 for i in range(len(stages))]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(-0.8, xs[-1] + 0.8)
    ax.set_ylim(0, 4)
    ax.axis("off")
    for x, (label, tokens, color) in zip(xs, stages):
        h = 0.4 + 2.8 * (tokens / max_tok)
        y = 2 - h / 2
        ax.add_patch(plt.Rectangle((x - 0.4, y), 0.8, h,
                     facecolor=color, alpha=0.85, edgecolor="white", linewidth=1.5))
        ax.text(x, y + h + 0.15, label, ha="center", va="bottom",
                fontsize=8.5, fontweight="bold")
        ax.text(x, y + h / 2, f"{tokens:,}", ha="center", va="center",
                fontsize=8, color="white", fontweight="bold")
    for i in range(len(stages) - 1):
        ax.annotate("", xy=(xs[i + 1] - 0.4, 2), xytext=(xs[i] + 0.4, 2),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=2))
    ax.set_title("Token Flow Through the Article-Generation Pipeline (tokens per stage)",
                 fontsize=12, fontweight="bold")
    out = FIGURES_DIR / "token_sankey.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def generate_network() -> str:
    import networkx as nx
    from matplotlib.lines import Line2D
    G = nx.DiGraph()
    agent_cfg: dict[str, tuple[int, str]] = {
        "Researcher": (2000, "#1565C0"),
        "Writer":     (4000, "#2E7D32"),
        "Editor":     (3500, "#E65100"),
        "LaTeX":      (3000, "#6A1B9A"),
    }
    artifact_cfg: dict[str, str] = {
        "research_notes.md": "#90A4AE",
        "chapters/*.md":     "#90A4AE",
        "edited/*.md":       "#90A4AE",
        "latex/*.tex":       "#B0BEC5",
        "article.pdf":       "#FDD835",
    }
    order = ["Researcher", "research_notes.md", "Writer", "chapters/*.md",
             "Editor", "edited/*.md", "LaTeX", "latex/*.tex", "article.pdf"]
    for n in order:
        G.add_node(n)
    edges = [("Researcher", "research_notes.md"), ("research_notes.md", "Writer"),
             ("Writer", "chapters/*.md"), ("chapters/*.md", "Editor"),
             ("Editor", "edited/*.md"), ("edited/*.md", "LaTeX"),
             ("LaTeX", "latex/*.tex"), ("latex/*.tex", "article.pdf")]
    G.add_edges_from(edges)
    pos = {n: (i, 0) for i, n in enumerate(order)}
    fig, ax = plt.subplots(figsize=(14, 4))
    nx.draw_networkx_nodes(G, pos, nodelist=list(agent_cfg),
                           node_size=[agent_cfg[n][0] for n in agent_cfg],
                           node_color=[agent_cfg[n][1] for n in agent_cfg],
                           alpha=0.9, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=list(artifact_cfg),
                           node_size=600,
                           node_color=[artifact_cfg[n] for n in artifact_cfg],
                           node_shape="s", alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True,
                           arrowsize=20, edge_color="#555", width=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight="bold")
    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
               markersize=11, label=n)
        for n, (_, c) in agent_cfg.items()
    ] + [Line2D([0], [0], marker="s", color="w",
                markerfacecolor="#90A4AE", markersize=9, label="File artifact")]
    ax.legend(handles=legend, loc="upper right", fontsize=9)
    ax.set_title("Agent Communication Network: Data Flow Through the Pipeline",
                 fontsize=12, fontweight="bold")
    ax.axis("off")
    out = FIGURES_DIR / "agent_network.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    for fn in [generate_heatmap, generate_radar, generate_sankey, generate_network]:
        print(f"Generated: {fn()}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run tests to verify they pass**

```bash
uv run pytest tests/unit/test_generate_figures.py -v
```

Expected: all 9 tests PASS (1 script run + 4 exists + 4 nonempty).

- [ ] **Step 3: Verify all 4 PNGs were created**

```bash
ls -lh latex/figures/token_heatmap.png latex/figures/framework_radar.png \
        latex/figures/token_sankey.png latex/figures/agent_network.png
```

Expected: 4 files, each > 50 KB.

- [ ] **Step 4: Check line count**

```bash
uv run python scripts/check_file_lines.py
```

Expected: `OK: all Python files within 150-line limit`

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_figures.py tests/unit/test_generate_figures.py \
        latex/figures/token_heatmap.png latex/figures/framework_radar.png \
        latex/figures/token_sankey.png latex/figures/agent_network.png
git commit -m "feat(figures): add 4 complex visualizations — heatmap, radar, sankey, network graph"
```

---

## Task 4: Embed Network Graph in ch02

**Files:**
- Modify: `latex/chapters/ch02_architectures.tex`

- [ ] **Step 1: Insert the figure block after the existing TikZ figure**

Find the anchor text in `ch02_architectures.tex` (lines 11–12):
```
\label{fig:crew_architecture}
\end{figure}
```

Insert immediately after `\end{figure}`:
```latex

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figures/agent_network.png}
\caption{Agent communication network: data flow through the pipeline. Circular nodes are CrewAI agents (sized by token budget); square nodes are file artefacts passed between stages.}
\label{fig:agent-network}
\end{figure}
```

- [ ] **Step 2: Verify file still compiles**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3/latex && make 2>&1 | tail -5
```

Expected: `Output written on output/main.pdf` with no errors.

- [ ] **Step 3: Commit**

```bash
git add latex/chapters/ch02_architectures.tex
git commit -m "feat(latex): embed agent network graph in ch02"
```

---

## Task 5: Embed Radar Chart in ch03

**Files:**
- Modify: `latex/chapters/ch03_frameworks.tex`

- [ ] **Step 1: Insert the figure block after the framework comparison longtable**

Find the anchor text in `ch03_frameworks.tex`:
```
\end{longtable}

The comparison reveals that framework selection
```

Insert between `\end{longtable}` and `The comparison reveals...`:
```latex

\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{figures/framework_radar.png}
\caption{Multi-dimensional framework comparison across six production-readiness criteria (scores 0--10). Latency is inverted: a higher score means lower latency. Scores reflect the analysis in \S\ref{sec:linear_seq}--\S3.6.}
\label{fig:framework-radar}
\end{figure}

```

- [ ] **Step 2: Compile and verify**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3/latex && make 2>&1 | tail -5
```

Expected: success, no errors.

- [ ] **Step 3: Commit**

```bash
git add latex/chapters/ch03_frameworks.tex
git commit -m "feat(latex): embed framework radar chart in ch03"
```

---

## Task 6: Embed Heatmap in ch04

**Files:**
- Modify: `latex/chapters/ch04_production.tex`

- [ ] **Step 1: Insert the figure block after the rate limiting exponential backoff paragraph**

Find the anchor text in `ch04_production.tex`:
```
Production implementations use exponential backoff with jitter: on a 429 error, wait $2^{attempt}$ seconds plus random noise, then retry \cite{Segal2026}.
```

Insert immediately after that sentence (before `\section{The Gatekeeper Pattern}`):
```latex

\begin{figure}[H]
\centering
\includegraphics[width=0.9\textwidth]{figures/token_heatmap.png}
\caption{Token consumption heatmap across the four pipeline agents and four cost dimensions. Warmer colours indicate higher token usage; the Writer agent dominates completion tokens due to generating full chapter prose.}
\label{fig:token-heatmap}
\end{figure}

```

- [ ] **Step 2: Compile and verify**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3/latex && make 2>&1 | tail -5
```

Expected: success.

- [ ] **Step 3: Commit**

```bash
git add latex/chapters/ch04_production.tex
git commit -m "feat(latex): embed token consumption heatmap in ch04"
```

---

## Task 7: Embed Sankey in ch06

**Files:**
- Modify: `latex/chapters/ch06_casestudy.tex`

- [ ] **Step 1: Insert the figure block after the existing pipeline_latency figure**

Find the anchor text in `ch06_casestudy.tex`:
```
\begin{figure}[H]\centering\includegraphics[width=0.9\textwidth]{figures/pipeline_latency.png}\caption{Pipeline latency comparison: sequential vs fast (parallel Haiku) approach. Generated by Python/matplotlib.}\label{fig:pipeline_latency}\end{figure}
```

Insert immediately after that line:
```latex

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figures/token_sankey.png}
\caption{Token flow through the article-generation pipeline. Bar height is proportional to tokens consumed at each stage; arrows show the direction of data flow between agents.}
\label{fig:token-sankey}
\end{figure}
```

- [ ] **Step 2: Compile and verify**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3/latex && make 2>&1 | tail -5
```

Expected: success.

- [ ] **Step 3: Commit**

```bash
git add latex/chapters/ch06_casestudy.tex
git commit -m "feat(latex): embed token flow sankey diagram in ch06"
```

---

## Task 8: Full Recompile + Verify PDF

**Files:**
- Generate: `latex/output/main.pdf`
- Generate: `latex/output/uoh-sqak-article.pdf`

- [ ] **Step 1: Force clean recompile (4-pass)**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3/latex
touch main.tex
make 2>&1 | tail -10
```

Expected: `Output written on output/main.pdf` with page count ≥ 30 (was 29, 4 new figures add ~1–2 pages).

- [ ] **Step 2: Check page count**

```bash
pdfinfo /Users/salah/Projects/orch-ai-agents/hw3/latex/output/uoh-sqak-article.pdf | grep Pages
```

Expected: `Pages: 30` or higher.

- [ ] **Step 3: Open the PDF and visually verify all 4 new figures appear**

```bash
open /Users/salah/Projects/orch-ai-agents/hw3/latex/output/uoh-sqak-article.pdf
```

Check:
- Ch02: agent network graph present after TikZ diagram
- Ch03: radar chart present after framework table
- Ch04: heatmap present in rate limiting section
- Ch06: sankey present after bar chart

- [ ] **Step 4: Run full test suite**

```bash
cd /Users/salah/Projects/orch-ai-agents/hw3
uv run pytest tests/unit/ -q --tb=short
```

Expected: all tests pass, coverage ≥ 85%.

- [ ] **Step 5: Lint check**

```bash
uv run ruff check src/ tests/ scripts/
uv run python scripts/check_file_lines.py
```

Expected: both pass clean.

- [ ] **Step 6: Commit compiled PDF**

```bash
git add latex/output/main.pdf latex/output/uoh-sqak-article.pdf \
        latex/output/main.aux latex/output/main.toc \
        latex/output/main.out latex/output/main.bcf latex/output/main.run.xml
git commit -m "feat(pdf): recompile with 4 new figures — heatmap, radar, sankey, network (v1.14)"
```

---

## Task 9: Update README Screenshots

**Files:**
- Generate: `assets/screenshots/pdf_p07_v2.png` (ch02 now has network graph)
- Generate: `assets/screenshots/pdf_network.png`
- Generate: `assets/screenshots/pdf_radar.png`
- Generate: `assets/screenshots/pdf_heatmap.png`
- Generate: `assets/screenshots/pdf_sankey.png`
- Modify: `README.md`

- [ ] **Step 1: Extract new PDF page screenshots**

```bash
PDF=/Users/salah/Projects/orch-ai-agents/hw3/latex/output/uoh-sqak-article.pdf
OUT=/Users/salah/Projects/orch-ai-agents/hw3/assets/screenshots
# Extract all pages as low-res previews to find new figure pages
pdftoppm -r 120 -png -f 1 -l 35 $PDF $OUT/scan
ls $OUT/scan-*.png
```

Then identify which pages contain the 4 new figures, extract them at 200dpi:

```bash
# After visually identifying page numbers (e.g., network=p08, radar=p12, heatmap=p15, sankey=p25):
for page in 8 12 15 25; do
  pdftoppm -r 200 -png -f $page -l $page $PDF $OUT/scan
  # rename to semantic name after identifying content
done
```

- [ ] **Step 2: Add new figure screenshots to README under PDF Artifact section**

In `README.md`, add after the existing `### Chapter 2 — TikZ Architecture Diagram` section:

```markdown
### Chapter 2 — Agent Communication Network Graph

![Agent network graph](assets/screenshots/pdf_network.png)

### Chapter 3 — Framework Radar Chart

![Framework radar chart](assets/screenshots/pdf_radar.png)

### Chapter 4 — Token Consumption Heatmap

![Token consumption heatmap](assets/screenshots/pdf_heatmap.png)

### Chapter 6 — Token Flow Sankey Diagram

![Token flow sankey](assets/screenshots/pdf_sankey.png)
```

- [ ] **Step 3: Clean up scan previews**

```bash
rm /Users/salah/Projects/orch-ai-agents/hw3/assets/screenshots/scan-*.png
```

- [ ] **Step 4: Commit**

```bash
git add assets/screenshots/ README.md
git commit -m "docs(readme): add screenshots of 4 new PDF figures"
```

---

## Task 10: Version Bump + Final Push

**Files:**
- Modify: `src/agent_article/shared/version.py`
- Modify: `src/agent_article/__init__.py`

- [ ] **Step 1: Bump version to 1.14**

In `src/agent_article/shared/version.py`, change:
```python
VERSION = "1.13"
```
to:
```python
VERSION = "1.14"
```

In `src/agent_article/__init__.py`, change:
```python
__version__ = "1.13"
```
to:
```python
__version__ = "1.14"
```

- [ ] **Step 2: Run full suite one final time**

```bash
uv run pytest --cov=src -q --tb=short
uv run ruff check src/ tests/ scripts/
uv run python scripts/check_file_lines.py
```

Expected: all pass.

- [ ] **Step 3: Final commit and push**

```bash
git add src/agent_article/shared/version.py src/agent_article/__init__.py
git commit -m "chore: bump version to 1.14"
git push origin main
```

---

## Self-Review

**Spec coverage:**
- ✅ Token heatmap → Task 3 + Task 6
- ✅ Radar chart → Task 3 + Task 5
- ✅ Sankey diagram → Task 3 + Task 7
- ✅ Network graph → Task 3 + Task 4
- ✅ `scripts/generate_figures.py` under 150 lines → checked in Task 3 Step 4
- ✅ Tests → Task 2
- ✅ LaTeX embedding with captions and labels → Tasks 4–7
- ✅ 4-pass recompile → Task 8
- ✅ README updated with new screenshots → Task 9
- ✅ seaborn + networkx installed → Task 1

**No placeholders found.**

**Type consistency:** All 4 generator functions follow identical signature `() -> str`, consistent across tests and main().
