"""Tests for ArticleCrew._compile_with_repair() — 3-attempt repair loop."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import agent_article.shared.config as cfg_mod


def test_succeeds_on_first_attempt(tmp_path, config_dir, monkeypatch):
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", config_dir)
    from agent_article.crew.article_crew import ArticleCrew
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")
    mock_tool = MagicMock()
    mock_tool.run.return_value = fake_pdf
    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool):
        result = crew._compile_with_repair()
    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 1


def test_retries_after_known_error_and_succeeds(tmp_path, config_dir, monkeypatch):
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", config_dir)
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")
    mock_tool = MagicMock()
    mock_tool.run.side_effect = [RuntimeError("fail1"), fake_pdf]
    fake_errors = [LatexError(
        file="chapters/ch04.tex", line=10,
        message="! Undefined control sequence.", kind="undefined_cmd",
    )]
    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=1) as mock_patch, \
         patch("agent_article.crew.latex_repair_agent.repair") as mock_repair:
        result = crew._compile_with_repair()
    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 2
    assert mock_patch.call_count == 1
    assert mock_repair.call_count == 0


def test_calls_agent_repair_on_attempt_2_unknown(tmp_path, config_dir, monkeypatch):
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", config_dir)
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")
    fake_pdf = str(tmp_path / "main.pdf")
    mock_tool = MagicMock()
    mock_tool.run.side_effect = [RuntimeError("fail1"), RuntimeError("fail2"), fake_pdf]
    fake_errors = [LatexError(
        file="chapters/ch01.tex", line=5,
        message="! Weird unknown error.", kind="unknown",
    )]
    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=0), \
         patch("agent_article.crew.latex_repair_agent.repair") as mock_repair:
        result = crew._compile_with_repair()
    assert result == Path(fake_pdf)
    assert mock_tool.run.call_count == 3
    assert mock_repair.call_count == 1


def test_returns_none_after_all_attempts_exhausted(tmp_path, config_dir, monkeypatch):
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", config_dir)
    from agent_article.crew.article_crew import ArticleCrew
    from agent_article.crew.latex_log_parser import LatexError
    crew = ArticleCrew("Test")
    mock_tool = MagicMock()
    mock_tool.run.side_effect = RuntimeError("always fail")
    fake_errors = [LatexError(
        file="chapters/ch01.tex", line=5,
        message="! Unknown.", kind="unknown",
    )]
    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse",
               return_value=fake_errors), \
         patch("agent_article.crew.latex_patcher.apply", return_value=0), \
         patch("agent_article.crew.latex_repair_agent.repair"):
        result = crew._compile_with_repair()
    assert result is None
    assert mock_tool.run.call_count == 3


def test_stops_early_when_log_has_no_errors(tmp_path, config_dir, monkeypatch):
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", config_dir)
    from agent_article.crew.article_crew import ArticleCrew
    crew = ArticleCrew("Test")
    mock_tool = MagicMock()
    mock_tool.run.side_effect = RuntimeError("fail with empty log")
    with patch("agent_article.tools.latex_compile.LaTeXCompileTool",
               return_value=mock_tool), \
         patch("agent_article.crew.latex_log_parser.parse", return_value=[]):
        result = crew._compile_with_repair()
    assert result is None
    assert mock_tool.run.call_count == 1
