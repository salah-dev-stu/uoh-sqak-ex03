"""Tests for tools/chart_generator.py — ChartGeneratorTool."""
import json
import pytest

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


@pytest.fixture(autouse=True)
def reset_state(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "rate_limits.json").write_text(json.dumps({"version": "1.00", "services": {}}))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    (cfg_dir / "latex.json").write_text(json.dumps({
        "version": "1.00", "main_file": "latex/main.tex",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod.reload()
    ApiGatekeeper._instance = None
    yield
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def test_creates_png(tmp_path) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out = tmp_path / "figs"
    result = ChartGeneratorTool(output_dir=out).run(
        chart_type="bar",
        title="Test",
        labels=["A", "B"],
        values=[10, 20],
        ylabel="Score",
        filename="test.png",
    )
    assert (out / "test.png").exists()
    assert (out / "test.png").stat().st_size > 0
    assert "test.png" in result


def test_creates_output_dir(tmp_path) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out = tmp_path / "new_dir"
    ChartGeneratorTool(output_dir=out).run("bar", "T", ["X"], [1], "Y", "t.png")
    assert out.exists()


def test_line_chart(tmp_path) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out = tmp_path / "figs2"
    ChartGeneratorTool(output_dir=out).run("line", "L", ["X1", "X2"], [5, 8], "V", "l.png")
    assert (out / "l.png").exists()


def test_tool_name(tmp_path) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    assert ChartGeneratorTool(output_dir=tmp_path).name == "chart_generator"
