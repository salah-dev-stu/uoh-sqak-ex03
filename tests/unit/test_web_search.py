"""Tests for tools/web_search.py — WebSearchTool."""
import json
from unittest.mock import MagicMock, patch
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
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    cfg_mod.reload()
    ApiGatekeeper._instance = None
    yield
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def _make_ddgs(results):
    m = MagicMock()
    m.__enter__ = lambda s: s
    m.__exit__ = MagicMock(return_value=False)
    m.text = MagicMock(return_value=results)
    return m


def test_returns_formatted_string() -> None:
    from agent_article.tools.web_search import WebSearchTool
    mock_results = [{"title": "LangChain", "body": "A framework", "href": "https://ex.com"}]
    with patch("duckduckgo_search.DDGS", return_value=_make_ddgs(mock_results)):
        result = WebSearchTool().run("LangChain overview")
    assert "LangChain" in result
    assert "https://ex.com" in result


def test_no_results_returns_message() -> None:
    from agent_article.tools.web_search import WebSearchTool
    with patch("duckduckgo_search.DDGS", return_value=_make_ddgs([])):
        result = WebSearchTool().run("xyz123")
    assert "No results" in result


def test_tool_name() -> None:
    from agent_article.tools.web_search import WebSearchTool
    assert WebSearchTool().name == "web_search"
