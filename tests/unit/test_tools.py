"""Tests for tools: file_rw, web_search, chart_generator, latex_compile."""
import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


@pytest.fixture(autouse=True)
def reset_state():
    cfg_mod.reload()
    ApiGatekeeper._instance = None
    yield
    cfg_mod.reload()
    ApiGatekeeper._instance = None


@pytest.fixture
def tool_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(json.dumps({
        "version": "1.00", "workspace_dir": str(tmp_path / "workspace"),
        "output_filename": "test.pdf",
    }))
    (cfg_dir / "rate_limits.json").write_text(json.dumps({
        "version": "1.00", "services": {}
    }))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    (cfg_dir / "latex.json").write_text(json.dumps({
        "version": "1.00", "compiler": "lualatex", "biber": "biber",
        "passes": 4, "main_file": "latex/main.tex", "output_dir": "latex/output",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return tmp_path


# --- FileWriteTool / FileReadTool ---

def test_file_write_and_read(tool_config) -> None:
    from agent_article.tools.file_rw import FileWriteTool, FileReadTool
    workspace = tool_config / "workspace"
    writer = FileWriteTool(base_dir=workspace)
    reader = FileReadTool(base_dir=workspace)
    writer.run("notes.md", "# Hello\nWorld")
    content = reader.run("notes.md")
    assert content == "# Hello\nWorld"


def test_file_write_creates_parent_dirs(tool_config) -> None:
    from agent_article.tools.file_rw import FileWriteTool
    workspace = tool_config / "workspace"
    writer = FileWriteTool(base_dir=workspace)
    writer.run("chapters/ch01.md", "Chapter 1")
    assert (workspace / "chapters" / "ch01.md").read_text() == "Chapter 1"


def test_file_read_missing_raises(tool_config) -> None:
    from agent_article.tools.file_rw import FileReadTool
    workspace = tool_config / "workspace"
    reader = FileReadTool(base_dir=workspace)
    with pytest.raises(FileNotFoundError):
        reader.run("nonexistent.md")


def test_file_write_returns_written_message(tool_config) -> None:
    from agent_article.tools.file_rw import FileWriteTool
    workspace = tool_config / "workspace"
    writer = FileWriteTool(base_dir=workspace)
    result = writer.run("test.txt", "data")
    assert "Written" in result


def test_file_tool_names(tool_config) -> None:
    from agent_article.tools.file_rw import FileWriteTool, FileReadTool
    workspace = tool_config / "workspace"
    assert FileWriteTool(base_dir=workspace).name == "file_write"
    assert FileReadTool(base_dir=workspace).name == "file_read"


# --- WebSearchTool ---

def test_web_search_returns_formatted_string(tool_config) -> None:
    from agent_article.tools.web_search import WebSearchTool
    mock_results = [{"title": "LangChain", "body": "A framework for LLMs", "href": "https://ex.com"}]

    mock_ddgs_instance = MagicMock()
    mock_ddgs_instance.__enter__ = lambda s: s
    mock_ddgs_instance.__exit__ = MagicMock(return_value=False)
    mock_ddgs_instance.text = MagicMock(return_value=mock_results)

    with patch("duckduckgo_search.DDGS", return_value=mock_ddgs_instance):
        tool = WebSearchTool()
        result = tool.run("LangChain overview")

    assert "LangChain" in result
    assert "https://ex.com" in result


def test_web_search_no_results_message(tool_config) -> None:
    from agent_article.tools.web_search import WebSearchTool

    mock_ddgs_instance = MagicMock()
    mock_ddgs_instance.__enter__ = lambda s: s
    mock_ddgs_instance.__exit__ = MagicMock(return_value=False)
    mock_ddgs_instance.text = MagicMock(return_value=[])

    with patch("duckduckgo_search.DDGS", return_value=mock_ddgs_instance):
        tool = WebSearchTool()
        result = tool.run("nonexistent query xyz")

    assert "No results" in result


# --- ChartGeneratorTool ---

def test_chart_creates_png(tool_config) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out_dir = tool_config / "figures"
    tool = ChartGeneratorTool(output_dir=out_dir)
    result = tool.run(
        chart_type="bar",
        title="Test Chart",
        labels=["A", "B", "C"],
        values=[10, 20, 15],
        ylabel="Score",
        filename="test_chart.png",
    )
    assert (out_dir / "test_chart.png").exists()
    assert (out_dir / "test_chart.png").stat().st_size > 0
    assert "test_chart.png" in result


def test_chart_creates_output_dir(tool_config) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out_dir = tool_config / "new_figures"
    assert not out_dir.exists()
    tool = ChartGeneratorTool(output_dir=out_dir)
    tool.run("bar", "T", ["A"], [1], "Y", "t.png")
    assert out_dir.exists()


def test_chart_line_type(tool_config) -> None:
    from agent_article.tools.chart_generator import ChartGeneratorTool
    out_dir = tool_config / "figures2"
    tool = ChartGeneratorTool(output_dir=out_dir)
    tool.run("line", "Line Chart", ["X1", "X2"], [5, 8], "Value", "line.png")
    assert (out_dir / "line.png").exists()


# --- LaTeXCompileTool ---

def test_latex_compile_calls_4_subprocesses(tool_config) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool
    call_log = []

    def fake_run(cmd, cwd, capture_output, text, timeout):
        call_log.append(cmd[0])
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    with patch("agent_article.tools.latex_compile.subprocess.run", fake_run):
        latex_dir = tool_config / "latex"
        latex_dir.mkdir()
        tool = LaTeXCompileTool(latex_dir=latex_dir)
        tool.run("main.tex")

    assert len(call_log) == 4
    assert call_log[0] == "lualatex"
    assert call_log[1] == "biber"
    assert call_log[2] == "lualatex"
    assert call_log[3] == "lualatex"


def test_latex_compile_raises_on_error(tool_config) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool

    def fail_run(cmd, cwd, capture_output, text, timeout):
        return type("R", (), {"returncode": 1, "stdout": "", "stderr": "ERROR"})()

    with patch("agent_article.tools.latex_compile.subprocess.run", fail_run):
        latex_dir = tool_config / "latex2"
        latex_dir.mkdir()
        tool = LaTeXCompileTool(latex_dir=latex_dir)
        with pytest.raises(RuntimeError):
            tool.run("main.tex")
