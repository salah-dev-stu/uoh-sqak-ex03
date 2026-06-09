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
