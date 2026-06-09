#!/usr/bin/env python3
"""Generate publication-quality figures for the LaTeX article."""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

FIGURES_DIR = Path("latex/figures")


def generate_heatmap() -> str:
    import seaborn as sns
    data = np.array([
        [3_200, 5_800, 12, 0],
        [5_100, 38_200, 8, 200],
        [4_800, 22_600, 6, 150],
        [2_900, 31_800, 42, 300],
    ])
    labels_y = ["Researcher", "Writer", "Editor", "LaTeX"]
    labels_x = ["Prompt\nTokens", "Completion\nTokens", "Tool\nCalls", "Retry\nOverhead"]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(data, annot=True, fmt="d", cmap="YlOrRd", xticklabels=labels_x,
                yticklabels=labels_y, ax=ax, linewidths=0.5, cbar_kws={"label": "Tokens"})
    ax.set_title("Token Consumption per Agent and Pipeline Phase",
                 fontsize=13, fontweight="bold", pad=12)
    out = FIGURES_DIR / "token_heatmap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def generate_radar() -> str:
    cats = ["Latency", "Token\nEfficiency", "Observability",
            "Extensibility", "BiDi\nSupport", "Ease of Use"]
    n_cats = len(cats)
    angles = [n / n_cats * 2 * math.pi for n in range(n_cats)] + [0]
    scores = {
        "CrewAI": [8, 8, 7, 9, 8, 9],
        "LangGraph": [6, 7, 9, 10, 5, 5],
        "AutoGen": [4, 4, 6, 7, 3, 7],
    }
    colors = {"CrewAI": "#2196F3", "LangGraph": "#4CAF50", "AutoGen": "#FF5722"}
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
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
        ("Input\nPrompt", 1_000, "#78909C"),
        ("Researcher\nAgent", 8_500, "#1565C0"),
        ("Writer\nAgent", 42_000, "#2E7D32"),
        ("Editor\nAgent", 28_000, "#E65100"),
        ("LaTeX\nAgents", 35_000, "#6A1B9A"),
    ]
    max_tok = max(s[1] for s in stages)
    xs = [i * 2.2 for i in range(len(stages))]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(-0.8, xs[-1] + 0.8)
    ax.set_ylim(0, 4)
    ax.axis("off")
    for x, (label, tokens, color) in zip(xs, stages, strict=True):
        h = 0.4 + 2.8 * (tokens / max_tok)
        y = 2 - h / 2
        ax.add_patch(plt.Rectangle((x - 0.4, y), 0.8, h, facecolor=color,
                     alpha=0.85, edgecolor="white", linewidth=1.5))
        ax.text(x, y + h + 0.15, label, ha="center", va="bottom",
                fontsize=8.5, fontweight="bold")
        ax.text(x, y + h / 2, f"{tokens:,}", ha="center", va="center",
                fontsize=8, color="white", fontweight="bold")
    for i in range(len(stages) - 1):
        ax.annotate("", xy=(xs[i + 1] - 0.4, 2), xytext=(xs[i] + 0.4, 2),
                    arrowprops={"arrowstyle": "->", "color": "#555", "lw": 2})
    ax.set_title("Token Flow Through the Article-Generation Pipeline (tokens per stage)",
                 fontsize=12, fontweight="bold")
    out = FIGURES_DIR / "token_sankey.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(out)


def generate_network() -> str:
    import networkx as nx
    from matplotlib.lines import Line2D
    graph = nx.DiGraph()
    agent_cfg: dict[str, tuple[int, str]] = {
        "Researcher": (2000, "#1565C0"), "Writer": (4000, "#2E7D32"),
        "Editor": (3500, "#E65100"), "LaTeX": (3000, "#6A1B9A"),
    }
    artifact_cfg: dict[str, str] = {
        "research_notes.md": "#90A4AE", "chapters/*.md": "#90A4AE",
        "edited/*.md": "#90A4AE", "latex/*.tex": "#B0BEC5", "article.pdf": "#FDD835",
    }
    order = ["Researcher", "research_notes.md", "Writer", "chapters/*.md",
             "Editor", "edited/*.md", "LaTeX", "latex/*.tex", "article.pdf"]
    for n in order:
        graph.add_node(n)
    graph.add_edges_from([(order[i], order[i + 1]) for i in range(len(order) - 1)])
    pos = {n: (i, 0) for i, n in enumerate(order)}
    fig, ax = plt.subplots(figsize=(14, 4))
    nx.draw_networkx_nodes(graph, pos, nodelist=list(agent_cfg),
                           node_size=[agent_cfg[n][0] for n in agent_cfg],
                           node_color=[agent_cfg[n][1] for n in agent_cfg], alpha=0.9, ax=ax)
    nx.draw_networkx_nodes(graph, pos, nodelist=list(artifact_cfg), node_size=600,
                           node_color=[artifact_cfg[n] for n in artifact_cfg],
                           node_shape="s", alpha=0.9, ax=ax)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowsize=20,
                           edge_color="#555", width=2)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=7, font_weight="bold")
    legend = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=11,
                     label=n) for n, (_, c) in agent_cfg.items()]
    legend.append(Line2D([0], [0], marker="s", color="w", markerfacecolor="#90A4AE",
                         markersize=9, label="File artifact"))
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
