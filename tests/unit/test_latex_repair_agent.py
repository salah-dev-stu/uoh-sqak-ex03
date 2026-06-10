# tests/unit/test_latex_repair_agent.py
"""Tests for crew/latex_repair_agent.py — re-prompt ClaudeCLILLM for unknown errors."""
from unittest.mock import MagicMock, patch

from agent_article.crew.latex_log_parser import LatexError


def _unknown(file="chapters/ch01.tex", line=10):
    return LatexError(file=file, line=line,
                      message="! Some weird error.", kind="unknown")


def test_repair_calls_llm_and_writes_file(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    tex = chapters / "ch01.tex"
    tex.write_text("\\chapter{Hello}\nbroken content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.return_value = "\\chapter{Hello}\nfixed content"

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([_unknown()], tmp_path)

    assert mock_llm.call.called
    prompt = mock_llm.call.call_args[0][0]
    assert "! Some weird error." in prompt
    assert "broken content" in prompt
    assert tex.read_text(encoding="utf-8") == "\\chapter{Hello}\nfixed content"


def test_repair_skips_known_error_kinds(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    known = LatexError(file="chapters/ch04.tex", line=1,
                       message="! Undefined control sequence", kind="undefined_cmd")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([known], tmp_path)
    assert not mock_llm.call.called


def test_repair_skips_missing_file(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    err = LatexError(file="chapters/nonexistent.tex", line=1,
                     message="! error", kind="unknown")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([err], tmp_path)
    assert not mock_llm.call.called


def test_repair_skips_empty_file_field(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    mock_llm = MagicMock()
    err = LatexError(file="", line=0, message="! error", kind="unknown")
    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([err], tmp_path)
    assert not mock_llm.call.called


def test_repair_dedupes_per_file_one_llm_call(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    tex = chapters / "ch01.tex"
    tex.write_text("content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.return_value = "fixed"
    errors = [_unknown(), _unknown()]  # two errors, same file

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair(errors, tmp_path)

    assert mock_llm.call.call_count == 1


def test_repair_tolerates_llm_exception(tmp_path):
    from agent_article.crew.latex_repair_agent import repair
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    (chapters / "ch01.tex").write_text("content", encoding="utf-8")

    mock_llm = MagicMock()
    mock_llm.call.side_effect = RuntimeError("LLM unavailable")

    with patch("agent_article.crew.latex_repair_agent.ClaudeCLILLM",
               return_value=mock_llm):
        repair([_unknown()], tmp_path)  # must not raise
