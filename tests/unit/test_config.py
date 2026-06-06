"""Tests for shared/config.py."""
import json

import pytest

import agent_article.shared.config as cfg_mod


@pytest.fixture(autouse=True)
def reset_cache() -> None:
    cfg_mod.reload()


@pytest.fixture
def fake_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    (cfg_dir / "setup.json").write_text(
        json.dumps({"version": "1.00", "package": "test_pkg", "workspace_dir": "ws"})
    )
    monkeypatch.setattr(cfg_mod, "_CONFIG_DIR", cfg_dir)
    return cfg_dir


def test_get_config_loads_json(fake_config) -> None:
    result = cfg_mod.get_config("setup")
    assert result["version"] == "1.00"
    assert result["package"] == "test_pkg"


def test_get_config_caches(fake_config) -> None:
    first = cfg_mod.get_config("setup")
    second = cfg_mod.get_config("setup")
    assert first is second


def test_cfg_returns_value(fake_config) -> None:
    assert cfg_mod.cfg("setup", "package") == "test_pkg"


def test_cfg_returns_default_for_missing(fake_config) -> None:
    assert cfg_mod.cfg("setup", "nonexistent", default="fallback") == "fallback"


def test_cfg_returns_none_default(fake_config) -> None:
    assert cfg_mod.cfg("setup", "nonexistent") is None


def test_reload_clears_cache(fake_config) -> None:
    cfg_mod.get_config("setup")
    assert "setup" in cfg_mod._cache
    cfg_mod.reload()
    assert cfg_mod._cache == {}


def test_missing_file_raises(fake_config) -> None:
    with pytest.raises(FileNotFoundError):
        cfg_mod.get_config("nonexistent_file")
