"""Tests for tools/file_rw.py — FileWriteTool and FileReadTool."""
import json
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
def workspace(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    ws = tmp_path / "workspace"
    (cfg_dir / "setup.json").write_text(json.dumps({
        "version": "1.00", "workspace_dir": str(ws), "output_filename": "test.pdf",
    }))
    (cfg_dir / "rate_limits.json").write_text(json.dumps({"version": "1.00", "services": {}}))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return ws


def test_write_and_read(workspace) -> None:
    from agent_article.tools.file_rw import FileWriteTool, FileReadTool
    FileWriteTool(base_dir=workspace).run("notes.md", "# Hello\nWorld")
    assert FileReadTool(base_dir=workspace).run("notes.md") == "# Hello\nWorld"


def test_write_creates_parent_dirs(workspace) -> None:
    from agent_article.tools.file_rw import FileWriteTool
    FileWriteTool(base_dir=workspace).run("chapters/ch01.md", "Chapter 1")
    assert (workspace / "chapters" / "ch01.md").read_text() == "Chapter 1"


def test_read_missing_raises(workspace) -> None:
    from agent_article.tools.file_rw import FileReadTool
    with pytest.raises(FileNotFoundError):
        FileReadTool(base_dir=workspace).run("nonexistent.md")


def test_write_returns_confirmation(workspace) -> None:
    from agent_article.tools.file_rw import FileWriteTool
    result = FileWriteTool(base_dir=workspace).run("test.txt", "data")
    assert "Written" in result


def test_tool_names(workspace) -> None:
    from agent_article.tools.file_rw import FileWriteTool, FileReadTool
    assert FileWriteTool(base_dir=workspace).name == "file_write"
    assert FileReadTool(base_dir=workspace).name == "file_read"
