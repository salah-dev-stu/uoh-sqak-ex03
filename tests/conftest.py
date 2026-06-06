"""Shared pytest fixtures for unit and integration tests."""
import json

import pytest

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


@pytest.fixture
def config_dir(tmp_path):
    """Create a complete config directory in tmp_path."""
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    tasks = {
        "research": {"description": "Research {topic}.", "expected_output": "notes.md"},
        "write": {"description": "Write chapters about {topic}.", "expected_output": "chapters"},
        "edit": {"description": "Edit all chapters.", "expected_output": "edited chapters"},
        "latex": {"description": "Compile PDF.", "expected_output": "uoh-sqak-article.pdf"},
    }
    agents = {k: {
        "role": f"{k.capitalize()} Agent",
        "goal": "Test goal",
        "backstory": "Test backstory",
        "llm": "claude-cli",
        "skill_ref": f"{k}_skill",
        "temperature": 0.3,
    } for k in ["researcher", "writer", "editor", "latex_producer"]}
    for name, data in [
        ("tasks", {"version": "1.00", "tasks": tasks}),
        ("agents", {"version": "1.00", "agents": agents}),
        ("rate_limits", {"version": "1.00", "services": {}}),
        ("logging_config", {
            "version": "1.00",
            "log_dir": str(tmp_path / "logs"),
            "fifo_files": 5,
            "max_lines_per_file": 100,
            "level": "INFO",
        }),
        ("setup", {
            "version": "1.00",
            "workspace_dir": str(tmp_path / "workspace"),
            "output_filename": "uoh-sqak-article.pdf",
        }),
        ("latex", {
            "version": "1.00",
            "compiler": "lualatex",
            "biber": "biber",
            "passes": 4,
            "main_file": "latex/main.tex",
        }),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    return cfg_dir


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset shared singletons between every test."""
    cfg_mod.reload()
    ApiGatekeeper._instance = None
    yield
    cfg_mod.reload()
    ApiGatekeeper._instance = None
