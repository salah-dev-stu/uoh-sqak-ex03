"""Tests for article task builders."""
import json
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
def full_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    tasks = {
        "research": {
            "description": "Research {topic} thoroughly.",
            "expected_output": "notes.md with coverage",
        },
        "write": {
            "description": "Write chapters about {topic}.",
            "expected_output": "6 chapter files",
        },
        "edit": {"description": "Edit all chapters.", "expected_output": "6 edited files"},
        "latex": {"description": "Compile PDF.", "expected_output": "uoh-sqak-article.pdf"},
    }
    agents = {
        "researcher": {"role": "R", "goal": "G", "backstory": "B",
                       "llm": "claude-cli", "skill_ref": "researcher_skill", "temperature": 0.3},
    }
    for name, data in [
        ("tasks", {"version": "1.00", "tasks": tasks}),
        ("agents", {"version": "1.00", "agents": agents}),
        ("rate_limits", {"version": "1.00", "services": {}}),
        ("logging_config", {
            "version": "1.00", "log_dir": str(tmp_path / "logs"),
            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
        }),
        ("setup", {"version": "1.00", "workspace_dir": str(tmp_path / "ws"),
                   "output_filename": "t.pdf"}),
        ("latex", {"version": "1.00", "compiler": "lualatex", "biber": "biber",
                   "passes": 4, "main_file": "latex/main.tex"}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)

    mock_agent_obj = MagicMock()
    mock_agent_obj.build.return_value = MagicMock()
    return mock_agent_obj


def test_research_task_format_topic(full_config):
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_research_task(full_config, "AI Agents")
    kw = mock_task.call_args.kwargs
    assert "AI Agents" in kw["description"]


def test_write_task_has_context(full_config):
    ctx = [MagicMock()]
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_write_task(full_config, "AI Agents", ctx)
    kw = mock_task.call_args.kwargs
    assert kw["context"] is ctx


def test_edit_task_built(full_config):
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_edit_task(full_config, [])
    assert mock_task.called


def test_latex_task_built(full_config):
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_latex_task(full_config, [])
    assert mock_task.called
