"""Tests for figure_generators module — verifies all 4 PNGs are created."""
from pathlib import Path

import pytest

from agent_article.tools.figure_generators import (
    generate_all,
    generate_heatmap,
    generate_network,
    generate_radar,
    generate_sankey,
)

EXPECTED = ["token_heatmap.png", "framework_radar.png", "token_sankey.png", "agent_network.png"]


def test_generate_all_returns_four_paths(tmp_path):
    paths = generate_all(tmp_path)
    assert len(paths) == 4


@pytest.mark.parametrize("filename,fn", [
    ("token_heatmap.png", generate_heatmap),
    ("framework_radar.png", generate_radar),
    ("token_sankey.png", generate_sankey),
    ("agent_network.png", generate_network),
])
def test_individual_generator_creates_file(tmp_path, filename, fn):
    result = fn(tmp_path)
    assert Path(result).exists()
    assert Path(result).stat().st_size > 10_000


def test_generate_all_files_nonempty(tmp_path):
    paths = generate_all(tmp_path)
    for p in paths:
        assert Path(p).stat().st_size > 10_000, f"Too small: {p}"


def test_generate_all_idempotent(tmp_path):
    paths1 = generate_all(tmp_path)
    paths2 = generate_all(tmp_path)
    assert set(paths1) == set(paths2)
