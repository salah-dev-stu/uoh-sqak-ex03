"""Tests for ArticleCrew assembly and run."""
import json
from unittest.mock import MagicMock, patch

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


def _mk_cfg(tmp_path, *, default_model="claude-haiku-4-5-20251001"):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    agents_cfg = {k: {"role": "R", "goal": "G", "backstory": "B",
                      "llm": "claude-cli", "skill_ref": f"{k}_skill", "temperature": 0}
                  for k in ["researcher", "writer", "editor", "latex_producer"]}
    for name, data in [
        ("tasks", {"version": "1.03", "tasks": {
            "research": {"description": "R {topic}", "expected_output": "n"},
            "write":    {"description": "W {topic}", "expected_output": "c"},
            "edit":     {"description": "E", "expected_output": "e"},
        }}),
        ("agents", {"version": "1.00", "agents": agents_cfg}),
        ("rate_limits", {"version": "1.01", "services": {"claude_cli": {
            "haiku_timeout_seconds": 300, "sonnet_timeout_seconds": 600}}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
        ("setup", {"version": "1.01", "workspace_dir": str(tmp_path / "ws"),
                   "output_filename": "test.pdf", "default_model": default_model}),
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


def test_crew_run_success(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.crew.article_crew as cm
    from agent_article.crew.article_crew import ArticleCrew

    mock_task = MagicMock()
    with patch.object(cm, "ResearcherAgent", return_value=_mock_agent()), \
         patch.object(cm, "WriterAgent", return_value=_mock_agent()), \
         patch.object(cm, "EditorAgent", return_value=_mock_agent()), \
         patch.object(cm, "build_research_task", return_value=mock_task), \
         patch.object(cm, "build_write_task", return_value=mock_task), \
         patch.object(cm, "build_edit_task", return_value=mock_task), \
         patch.object(cm, "build_latex_tasks", return_value=[mock_task]), \
         patch.object(cm, "Crew") as mock_crew_cls:
        mock_crew_cls.return_value.kickoff.return_value = "done"
        crew = ArticleCrew("Test Topic")
        with patch.object(crew, "_run_latex_phase_parallel", return_value=[]), \
             patch.object(crew, "_compile_pdf", return_value=None):
            result = crew.run()
    assert result.success is True
    assert result.pdf_path.endswith("test.pdf")


def test_crew_run_failure(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    import agent_article.crew.article_crew as cm
    from agent_article.crew.article_crew import ArticleCrew

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


def test_clean_latex_strips_fences():
    from agent_article.crew.article_crew import _clean_latex
    raw = "```latex\n\\chapter{Hello}\n```\nSome trailing text."
    result = _clean_latex(raw)
    assert result.startswith("\\chapter{Hello}")
    assert "```" not in result
    assert "trailing" not in result


def test_clean_latex_passthrough():
    from agent_article.crew.article_crew import _clean_latex
    raw = "\\chapter{Hello}\n\\section{World}"
    assert _clean_latex(raw) == raw


def test_run_latex_phase_parallel_calls_all_tasks(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.crew.article_crew import ArticleCrew

    crew = ArticleCrew("test")
    called = []
    with patch.object(crew, "_run_single_latex_task", side_effect=lambda t: called.append(t) or ""):
        tasks = [MagicMock() for _ in range(7)]
        crew._run_latex_phase_parallel(tasks)
    assert len(called) == 7
