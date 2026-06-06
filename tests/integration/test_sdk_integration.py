"""Integration tests — SDK + crew pipeline with mock LLM."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


@pytest.fixture
def full_env(tmp_path, monkeypatch):
    """Full config + workspace environment for integration tests."""
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    ws_dir = tmp_path / "workspace"
    ws_dir.mkdir()
    (ws_dir / "chapters").mkdir()
    tasks = {
        "research": {"description": "Research {topic}.", "expected_output": "notes.md"},
        "write": {"description": "Write {topic}.", "expected_output": "chapters"},
        "edit": {"description": "Edit.", "expected_output": "edited"},
        "latex": {"description": "Compile.", "expected_output": "pdf"},
    }
    agents = {k: {
        "role": f"{k}", "goal": "G", "backstory": "B",
        "llm": "claude-cli", "skill_ref": f"{k}_skill", "temperature": 0.3,
    } for k in ["researcher", "writer", "editor", "latex_producer"]}
    for name, data in [
        ("tasks", {"version": "1.00", "tasks": tasks}),
        ("agents", {"version": "1.00", "agents": agents}),
        ("rate_limits", {"version": "1.00", "services": {}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
        ("setup", {"version": "1.00", "workspace_dir": str(ws_dir),
                   "output_filename": "uoh-sqak-article.pdf"}),
        ("latex", {"version": "1.00", "compiler": "lualatex", "biber": "biber",
                   "passes": 4, "main_file": "latex/main.tex"}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return tmp_path


def test_sdk_generate_returns_result(full_env):
    """SDK.generate() should return a CrewResult regardless of success/failure."""
    from agent_article.sdk.sdk import ArticleSDK
    from agent_article.crew.article_crew import CrewResult
    import agent_article.crew.article_crew as cm
    mock_result = CrewResult(success=True, pdf_path="latex/output/uoh-sqak-article.pdf")
    with patch.object(cm, "ResearcherAgent", return_value=MagicMock()),\
         patch.object(cm, "WriterAgent", return_value=MagicMock()),\
         patch.object(cm, "EditorAgent", return_value=MagicMock()),\
         patch.object(cm, "LaTeXAgent", return_value=MagicMock()),\
         patch.object(cm, "build_research_task", return_value=MagicMock()),\
         patch.object(cm, "build_write_task", return_value=MagicMock()),\
         patch.object(cm, "build_edit_task", return_value=MagicMock()),\
         patch.object(cm, "build_latex_task", return_value=MagicMock()),\
         patch.object(cm, "Crew") as mock_crew:
        mock_crew.return_value.kickoff.return_value = "done"
        sdk = ArticleSDK()
        result = sdk.generate("AI Multi-Agent Systems")
    assert isinstance(result, CrewResult)
    assert result.success is True


def test_sdk_version_is_semver(full_env):
    from agent_article.sdk.sdk import ArticleSDK
    v = ArticleSDK.version()
    parts = v.split(".")
    assert len(parts) == 2
    assert int(parts[0]) >= 1
    assert int(parts[1]) >= 0


def test_sdk_approve_markdown_empty_dir(full_env):
    from agent_article.sdk.sdk import ArticleSDK
    sdk = ArticleSDK()
    result = sdk.approve_markdown(chapters_dir=str(full_env / "workspace" / "chapters"))
    assert result is False


def test_crew_result_captures_errors(full_env):
    from agent_article.crew.article_crew import ArticleCrew
    import agent_article.crew.article_crew as cm
    with patch.object(cm, "ResearcherAgent", side_effect=ValueError("config missing")):
        result = ArticleCrew("test topic").run()
    assert result.success is False
    assert any("config missing" in e for e in result.errors)
