"""Tests for ClaudeCLILLM per-instance model and timeout configuration."""
import json
from unittest.mock import patch

import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper


def _mk_cfg(tmp_path, default_model="claude-haiku-4-5-20251001"):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir(exist_ok=True)
    for name, data in [
        ("setup", {"version": "1.01", "default_model": default_model}),
        ("rate_limits", {"version": "1.01", "services": {"claude_cli": {
            "haiku_timeout_seconds": 300, "sonnet_timeout_seconds": 600}}}),
        ("logging_config", {"version": "1.00", "log_dir": str(tmp_path / "logs"),
                            "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO"}),
    ]:
        (cfg_dir / f"{name}.json").write_text(json.dumps(data))
    cfg_mod.reload()
    cfg_mod._CONFIG_DIR = cfg_dir


def setup_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def teardown_function():
    cfg_mod.reload()
    ApiGatekeeper._instance = None


def test_explicit_model_override(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.shared.claude_cli_llm import ClaudeCLILLM
    llm = ClaudeCLILLM(model="claude-sonnet-4-6")
    assert llm.model == "claude-sonnet-4-6"


def test_default_model_from_config(tmp_path, monkeypatch):
    _mk_cfg(tmp_path, default_model="claude-haiku-4-5-20251001")
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.shared.claude_cli_llm import ClaudeCLILLM
    llm = ClaudeCLILLM()
    assert "haiku" in llm.model


def test_haiku_gets_shorter_timeout(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.shared.claude_cli_llm import ClaudeCLILLM
    haiku = ClaudeCLILLM(model="claude-haiku-4-5-20251001")
    sonnet = ClaudeCLILLM(model="claude-sonnet-4-6")
    assert haiku.timeout == 300
    assert sonnet.timeout == 600


def test_temperature_defaults_to_zero(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.shared.claude_cli_llm import ClaudeCLILLM
    llm = ClaudeCLILLM()
    assert llm.temperature == 0


def test_call_passes_model_flag(tmp_path, monkeypatch):
    _mk_cfg(tmp_path)
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", tmp_path / "config")
    from agent_article.shared.claude_cli_llm import ClaudeCLILLM
    llm = ClaudeCLILLM(model="claude-haiku-4-5-20251001")
    import subprocess
    mock_result = type("R", (), {"returncode": 0, "stdout": "\\chapter{Hi}", "stderr": ""})()
    with patch.object(subprocess, "run", return_value=mock_result) as mock_run:
        llm.call("hello")
    cmd = mock_run.call_args.args[0]
    assert "--model" in cmd
    assert "claude-haiku-4-5-20251001" in cmd
