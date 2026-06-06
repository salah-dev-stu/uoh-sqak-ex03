"""Tests for skills/base_skill.py — BaseSkill and FileSkill."""
import pytest

from agent_article.skills.base_skill import FileSkill


def test_loads_content(tmp_path) -> None:
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("You are an expert.")
    assert "You are an expert." in FileSkill(skill_dir).content


def test_strips_yaml_frontmatter(tmp_path) -> None:
    skill_dir = tmp_path / "test_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: test\n---\nActual content here.")
    assert FileSkill(skill_dir).content == "Actual content here."


def test_missing_raises_file_not_found(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        _ = FileSkill(tmp_path / "nonexistent").content


def test_loads_researcher_skill() -> None:
    skill = FileSkill("researcher_skill")
    assert len(skill.content) > 100
    assert "citation" in skill.content.lower()


def test_loads_latex_skill() -> None:
    skill = FileSkill("latex_skill")
    assert "fancy formula, not plain text" in skill.content


def test_loads_writer_skill() -> None:
    skill = FileSkill("writer_skill")
    assert "Hebrew" in skill.content


def test_loads_editor_skill() -> None:
    skill = FileSkill("editor_skill")
    assert "NEEDS_FORMULA" in skill.content
