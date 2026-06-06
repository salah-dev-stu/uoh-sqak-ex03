"""Tests for agents — config loading, skill injection, tool wiring."""
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
def agent_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    agents = {
        "researcher": {"role": "R", "goal": "G", "backstory": "B",
                       "llm": "claude-cli", "skill_ref": "researcher_skill", "temperature": 0.3},
        "writer": {"role": "R", "goal": "G", "backstory": "B",
                   "llm": "claude-cli", "skill_ref": "writer_skill", "temperature": 0.7},
        "editor": {"role": "R", "goal": "G", "backstory": "B",
                   "llm": "claude-cli", "skill_ref": "editor_skill", "temperature": 0.2},
        "latex_producer": {
            "role": "R", "goal": "fancy formula, not plain text", "backstory": "B",
            "llm": "claude-cli", "skill_ref": "latex_skill", "temperature": 0.1,
        },
    }
    (cfg_dir / "agents.json").write_text(json.dumps({"version": "1.00", "agents": agents}))
    (cfg_dir / "rate_limits.json").write_text(json.dumps({"version": "1.00", "services": {}}))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    (cfg_dir / "setup.json").write_text(json.dumps({
        "version": "1.00", "workspace_dir": str(tmp_path / "ws"), "output_filename": "t.pdf",
    }))
    (cfg_dir / "latex.json").write_text(json.dumps({
        "version": "1.00", "compiler": "lualatex", "biber": "biber",
        "passes": 4, "main_file": "latex/main.tex",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return tmp_path


def test_researcher_builds_crewai_agent(agent_config) -> None:
    from agent_article.agents.researcher_agent import ResearcherAgent
    with patch("agent_article.agents.base_agent.Agent") as mock_agent:
        mock_agent.return_value = MagicMock()
        ResearcherAgent().build()
    mock_agent.assert_called_once()
    kw = mock_agent.call_args.kwargs
    assert kw["role"] == "R"
    assert "B" in kw["backstory"]


def test_latex_agent_goal_has_fancy_formula(agent_config) -> None:
    goal = cfg_mod.get_config("agents")["agents"]["latex_producer"]["goal"]
    assert "fancy formula, not plain text" in goal


def test_all_4_agents_build_without_error(agent_config) -> None:
    from agent_article.agents.editor_agent import EditorAgent
    from agent_article.agents.latex_agent import LaTeXAgent
    from agent_article.agents.researcher_agent import ResearcherAgent
    from agent_article.agents.writer_agent import WriterAgent
    with patch("agent_article.agents.base_agent.Agent", return_value=MagicMock()):
        ResearcherAgent().build()
        WriterAgent().build()
        EditorAgent().build()
        LaTeXAgent().build()


def test_skill_content_injected_into_backstory(agent_config) -> None:
    from agent_article.agents.researcher_agent import ResearcherAgent
    with patch("agent_article.agents.base_agent.Agent") as mock_agent:
        mock_agent.return_value = MagicMock()
        ResearcherAgent().build()
    backstory = mock_agent.call_args.kwargs["backstory"]
    assert "citation" in backstory.lower()
