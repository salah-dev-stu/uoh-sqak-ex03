# PRD — ChartGeneratorTool

## Overview

Python tool that generates a bar chart comparing orchestration frameworks using
`matplotlib` (Agg backend) and saves it as a PNG to `latex/figures/`.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `data` | `list[float]` | Score per framework (0–100) |
| `labels` | `list[str]` | Framework names |
| `title` | `str` | Chart title |
| `output_path` | `str` | Target PNG path (relative to project root) |
| **returns** | `str` | Absolute path of saved PNG |

## Functional Requirements

1. **FR1** — Uses `matplotlib.use('Agg')` before any pyplot import (headless safe).
2. **FR2** — Saves PNG at `output_path`; creates parent directories if needed.
3. **FR3** — Default output: `latex/figures/agent_topology.png` from config.
4. **FR4** — Bar chart with colour per bar, value labels above each bar.
5. **FR5** — Raises `RuntimeError` if `data` and `labels` have different lengths.
6. **FR6** — Chart title, axis labels, and figsize are configurable via constructor kwargs.

## Non-Functional Requirements

1. **NFR1** — File ≤ 150 total lines.
2. **NFR2** — No display window opened (Agg backend mandatory).
3. **NFR3** — DPI ≥ 150 for print-quality inclusion in LaTeX.

## Setup/Configuration

- `config/setup.json` — `figures_dir` (default: `latex/figures/`)
- No API key or external service required.

## Acceptance Criteria

- [ ] `ChartGeneratorTool().run(data, labels, title, path)` creates a PNG file
- [ ] PNG dimensions ≥ 800×480 pixels (checked with PIL or file size)
- [ ] `data` / `labels` length mismatch raises `RuntimeError`
- [ ] Works in a headless environment (CI without display)
- [ ] File is importable without triggering matplotlib display
