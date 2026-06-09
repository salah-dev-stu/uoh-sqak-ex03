"""Tests for article task builders."""
import json
from unittest.mock import MagicMock, patch

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


def _mk_cfg(tmp_path, *, default_model="claude-haiku-4-5-20251001"):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir(exist_ok=True)
    ch05_task = {
        "model": "claude-sonnet-4-6",
        "description": "BiDi chapter LaTeX",
        "expected_output": "tex",
    }
    tasks_data = {
        "research": {"description": "Research {topic} thoroughly.", "expected_output": "notes"},
        "write": {"description": "Write chapters about {topic}.", "expected_output": "6 files"},
        "edit": {"description": "Edit all chapters.", "expected_output": "6 edited"},
        "latex_ch01": {"description": "Ch1 LaTeX", "expected_output": "tex"},
        "latex_ch02": {"description": "Ch2 LaTeX", "expected_output": "tex"},
        "latex_ch03": {"description": "Ch3 LaTeX", "expected_output": "tex"},
        "latex_ch04": {"description": "Ch4 LaTeX", "expected_output": "tex"},
        "latex_ch05": ch05_task,
        "latex_ch06": {"description": "Ch6 LaTeX", "expected_output": "tex"},
        "latex_bib": {"description": "Bib", "expected_output": "bib"},
    }
    agents = {"latex_producer": {
        "role": "L", "goal": "G", "backstory": "B",
        "llm": "claude-cli", "skill_ref": "latex_skill", "temperature": 0,
    }}
    for name, data in [
        ("tasks", {"version": "1.03", "tasks": tasks_data}),
        ("agents", {"version": "1.00", "agents": agents}),
        ("rate_limits", {"version": "1.01", "services": {"claude_cli": {
            "haiku_timeout_seconds": 300, "sonnet_timeout_seconds": 600}}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
        ("setup", {"version": "1.01", "workspace_dir": str(tmp_path / "ws"),
                   "output_filename": "t.pdf", "default_model": default_model}),
        ("latex", {"version": "1.00", "compiler": "lualatex", "biber": "biber",
                   "passes": 4, "main_file": "latex/main.tex"}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    cfg_mod.reload()
    cfg_mod._CONFIG_DIR = cfg_dir
    return tmp_path


def setup_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def teardown_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def _mock_agent():
    m = MagicMock()
    m.build.return_value = MagicMock()
    return m


def test_research_task_format_topic(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_research_task(_mock_agent(), "AI Agents")
    kw = mock_task.call_args.kwargs
    assert "AI Agents" in kw["description"]


def test_write_task_has_context(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    ctx = [MagicMock()]
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_write_task(_mock_agent(), "AI Agents", ctx)
    kw = mock_task.call_args.kwargs
    assert kw["context"] is ctx


def test_edit_task_built(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.tasks.article_tasks as at
    with patch.object(at, "Task", return_value=MagicMock()) as mock_task:
        at.build_edit_task(_mock_agent(), [])
    assert mock_task.called


def test_build_latex_tasks_returns_eight(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.tasks.article_tasks as at
    with patch("agent_article.agents.latex_agent.LaTeXAgent") as mock_la, \
         patch.object(at, "Task", return_value=MagicMock()):
        mock_la.return_value = _mock_agent()
        tasks = at.build_latex_tasks([MagicMock()])
    assert len(tasks) == 8  # ch01–ch07 + bib


def test_build_latex_tasks_ch05_uses_sonnet(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.tasks.article_tasks as at
    models_used = []

    def fake_latex_agent(model=None):
        models_used.append(model)
        return _mock_agent()

    with patch("agent_article.agents.latex_agent.LaTeXAgent", side_effect=fake_latex_agent), \
         patch.object(at, "Task", return_value=MagicMock()):
        at.build_latex_tasks([MagicMock()])

    assert "claude-sonnet-4-6" in models_used


def test_build_latex_tasks_default_uses_haiku(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.tasks.article_tasks as at
    models_used = []

    def fake_latex_agent(model=None):
        models_used.append(model)
        return _mock_agent()

    with patch("agent_article.agents.latex_agent.LaTeXAgent", side_effect=fake_latex_agent), \
         patch.object(at, "Task", return_value=MagicMock()):
        at.build_latex_tasks([MagicMock()])

    # ch01–ch04, ch06, ch07, bib should be haiku; only ch05 is sonnet
    haiku_count = sum(1 for m in models_used if m == "claude-haiku-4-5-20251001")
    assert haiku_count == 7
