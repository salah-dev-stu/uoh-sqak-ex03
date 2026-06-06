"""Tests for shared/gatekeeper.py."""
import json
import pytest
import agent_article.shared.config as cfg_mod
from agent_article.shared.gatekeeper import ApiGatekeeper, GatekeeperError


@pytest.fixture(autouse=True)
def reset_singleton():
    ApiGatekeeper._instance = None
    cfg_mod.reload()
    yield
    ApiGatekeeper._instance = None
    cfg_mod.reload()


@pytest.fixture
def gatekeeper(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    log_dir = tmp_path / "logs"
    (cfg_dir / "rate_limits.json").write_text(json.dumps({
        "version": "1.00",
        "services": {
            "test_svc": {
                "requests_per_minute": 2,
                "tokens_per_article": 1000,
                "hard_cap_percent": 95,
            }
        }
    }))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00",
        "log_dir": str(log_dir),
        "fifo_files": 5,
        "max_lines_per_file": 100,
        "level": "INFO",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return ApiGatekeeper.instance()


def test_call_returns_fn_result(gatekeeper) -> None:
    result = gatekeeper.call("test_svc", lambda: 42)
    assert result == 42


def test_call_passes_args(gatekeeper) -> None:
    result = gatekeeper.call("test_svc", lambda x, y: x + y, 3, 4)
    assert result == 7


def test_rate_limit_enforced(gatekeeper) -> None:
    gatekeeper.call("test_svc", lambda: None)
    gatekeeper.call("test_svc", lambda: None)
    with pytest.raises(GatekeeperError, match="Rate limit"):
        gatekeeper.call("test_svc", lambda: None)


def test_singleton_returns_same_instance(tmp_path, monkeypatch) -> None:
    cfg_dir = tmp_path / "config2"
    cfg_dir.mkdir()
    (cfg_dir / "rate_limits.json").write_text(json.dumps({"version": "1.00", "services": {}}))
    (cfg_dir / "logging_config.json").write_text(json.dumps({
        "version": "1.00", "log_dir": str(tmp_path / "logs2"),
        "fifo_files": 5, "max_lines_per_file": 100, "level": "INFO",
    }))
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    g1 = ApiGatekeeper.instance()
    g2 = ApiGatekeeper.instance()
    assert g1 is g2


def test_get_spend_report(gatekeeper) -> None:
    gatekeeper.call("test_svc", lambda: None)
    report = gatekeeper.get_spend_report()
    assert "test_svc" in report
    assert report["test_svc"].calls == 1


def test_unknown_service_uses_defaults(gatekeeper) -> None:
    result = gatekeeper.call("unknown_svc", lambda: "ok")
    assert result == "ok"
