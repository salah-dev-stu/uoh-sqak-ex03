"""Tests for ArticleSDK public interface."""
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
def full_config(tmp_path, monkeypatch):
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


def test_sdk_version():
    from agent_article.sdk.sdk import ArticleSDK
    assert ArticleSDK.version() == "1.14"


def test_sdk_generate_delegates_to_crew(full_config):
    from agent_article.crew.article_crew import CrewResult
    from agent_article.sdk.sdk import ArticleSDK
    mock_result = CrewResult(success=True, pdf_path="latex/output/test.pdf")
    with patch("agent_article.sdk.sdk.ArticleCrew") as mock_crew_cls:
        mock_crew_cls.return_value.run.return_value = mock_result
        sdk = ArticleSDK()
        result = sdk.generate("AI Agents")
    assert result.success is True
    mock_crew_cls.assert_called_once_with("AI Agents")


def test_sdk_config_summary(full_config):
    from agent_article.sdk.sdk import ArticleSDK
    summary = ArticleSDK.config_summary()
    assert "workspace_dir" in summary
    assert "output_filename" in summary


def test_sdk_spend_report(full_config):
    from agent_article.sdk.sdk import ArticleSDK
    sdk = ArticleSDK()
    report = sdk.spend_report()
    assert isinstance(report, dict)


def test_sdk_approve_markdown_no_chapters(full_config, tmp_path):
    from agent_article.sdk.sdk import ArticleSDK
    sdk = ArticleSDK()
    result = sdk.approve_markdown(chapters_dir=str(tmp_path / "no_such_dir"))
    assert result is False
