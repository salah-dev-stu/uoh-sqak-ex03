"""Tests for tools/latex_compile.py — LaTeXCompileTool."""
import json
from unittest.mock import patch

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
        "version": "1.00", "compiler": "lualatex", "biber": "biber",
        "passes": 4, "main_file": "latex/main.tex",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod.reload()
    ApiGatekeeper._instance = None
    yield
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def _ok_result():
    return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()


def test_calls_4_subprocesses(tmp_path) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool
    calls = []

    def fake_run(cmd, cwd, capture_output, text, timeout, **kwargs):
        calls.append(cmd[0])
        return _ok_result()

    latex_dir = tmp_path / "latex"
    latex_dir.mkdir()
    with patch("agent_article.tools.latex_compile.subprocess.run", fake_run):
        LaTeXCompileTool(latex_dir=latex_dir).run("main.tex")

    assert len(calls) == 4
    assert calls[0] == "lualatex"
    assert calls[1] == "biber"
    assert calls[2] == "lualatex"
    assert calls[3] == "lualatex"


def test_raises_on_nonzero_returncode(tmp_path) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool

    def fail_run(cmd, cwd, capture_output, text, timeout, **kwargs):
        return type("R", (), {"returncode": 1, "stdout": "", "stderr": "ERROR"})()

    latex_dir = tmp_path / "latex2"
    latex_dir.mkdir()
    with patch("agent_article.tools.latex_compile.subprocess.run", fail_run), \
         pytest.raises(RuntimeError):
        LaTeXCompileTool(latex_dir=latex_dir).run("main.tex")


def test_check_log_warns_on_rerun(tmp_path) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool
    latex_dir = tmp_path / "latex4"
    latex_dir.mkdir()
    log = latex_dir / "main.log"
    log.write_text("Rerun to get cross-references right\nOverfull \\hbox bla", encoding="utf-8")
    tool = LaTeXCompileTool(latex_dir=latex_dir)
    tool._check_log(log)


def test_check_log_missing_file(tmp_path) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool
    latex_dir = tmp_path / "latex5"
    latex_dir.mkdir()
    tool = LaTeXCompileTool(latex_dir=latex_dir)
    tool._check_log(latex_dir / "nonexistent.log")


def test_tool_name(tmp_path) -> None:
    from agent_article.tools.latex_compile import LaTeXCompileTool
    latex_dir = tmp_path / "latex3"
    latex_dir.mkdir()
    assert LaTeXCompileTool(latex_dir=latex_dir).name == "latex_compile"
