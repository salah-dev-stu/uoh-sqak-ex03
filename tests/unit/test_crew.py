"""Tests for ArticleCrew assembly and run."""
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
        "research": {"description": "R {topic}", "expected_output": "notes"},
        "write": {"description": "W {topic}", "expected_output": "chapters"},
        "edit": {"description": "E", "expected_output": "edited"},
        "latex": {"description": "L", "expected_output": "pdf"},
    }
    agents_cfg = {k: {"role": "R", "goal": "G", "backstory": "B",
                      "llm": "claude-cli", "skill_ref": f"{k}_skill", "temperature": 0.3}
                  for k in ["researcher", "writer", "editor", "latex_producer"]}
    for name, data in [
        ("tasks", {"version": "1.00", "tasks": tasks}),
        ("agents", {"version": "1.00", "agents": agents_cfg}),
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


def _mock_agent():
    m = MagicMock()
    m.build.return_value = MagicMock()
    return m


def test_crew_run_success(full_config):
    from agent_article.crew.article_crew import ArticleCrew
    import agent_article.crew.article_crew as cm
    mock_kickoff = MagicMock(return_value="done")
    with patch.object(cm, "ResearcherAgent", return_value=_mock_agent()), \
         patch.object(cm, "WriterAgent", return_value=_mock_agent()), \
         patch.object(cm, "EditorAgent", return_value=_mock_agent()), \
         patch.object(cm, "LaTeXAgent", return_value=_mock_agent()), \
         patch.object(cm, "build_research_task", return_value=MagicMock()), \
         patch.object(cm, "build_write_task", return_value=MagicMock()), \
         patch.object(cm, "build_edit_task", return_value=MagicMock()), \
         patch.object(cm, "build_latex_task", return_value=MagicMock()), \
         patch.object(cm, "Crew") as mock_crew_cls:
        mock_crew_cls.return_value.kickoff = mock_kickoff
        result = ArticleCrew("Test Topic").run()
    assert result.success is True
    assert result.pdf_path.endswith("test.pdf")


def test_crew_run_failure(full_config):
    from agent_article.crew.article_crew import ArticleCrew
    import agent_article.crew.article_crew as cm
    with patch.object(cm, "ResearcherAgent", side_effect=RuntimeError("boom")):
        result = ArticleCrew("Test Topic").run()
    assert result.success is False
    assert len(result.errors) == 1


def test_crew_result_defaults():
    from agent_article.crew.article_crew import CrewResult
    r = CrewResult()
    assert r.success is False
    assert r.errors == []
    assert r.pdf_path == ""
