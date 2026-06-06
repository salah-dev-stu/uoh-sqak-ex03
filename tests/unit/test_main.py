"""Tests for main entry point and TUI helpers."""
import json
from unittest.mock import patch

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
def minimal_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    for name, data in [
        ("tasks", {"version": "1.00", "tasks": {
            k: {"description": f"{k} {{topic}}", "expected_output": k}
            for k in ["research", "write", "edit", "latex"]
        }}),
        ("agents", {"version": "1.00", "agents": {
            k: {"role": "R", "goal": "G", "backstory": "B",
                "llm": "claude-cli", "skill_ref": f"{k}_skill", "temperature": 0.3}
            for k in ["researcher", "writer", "editor", "latex_producer"]
        }}),
        ("rate_limits", {"version": "1.00", "services": {}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
        ("setup", {"version": "1.00", "workspace_dir": str(tmp_path / "ws"),
                   "output_filename": "test.pdf"}),
        ("latex", {"version": "1.00", "compiler": "lualatex", "biber": "biber",
                   "passes": 4, "main_file": "latex/main.tex"}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return tmp_path


def test_main_calls_run_tui(minimal_config):
    with patch("agent_article.menu.tui.run_tui") as mock_tui:
        import importlib

        import agent_article.main as m
        importlib.reload(m)
        ret = m.main()
    mock_tui.assert_called_once()
    assert ret == 0


def test_tui_run_exits_on_choice_4(minimal_config):
    from agent_article.menu import tui
    with patch.object(tui, "Prompt") as mock_prompt, \
         patch.object(tui, "_header"), \
         patch.object(tui, "ArticleSDK"):
        mock_prompt.ask.return_value = "4"
        tui.run_tui()
    assert mock_prompt.ask.called
