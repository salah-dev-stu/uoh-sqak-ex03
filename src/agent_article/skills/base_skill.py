"""Skill layer — file-based instruction packages injected into agent backstory."""
from abc import ABC, abstractmethod
from pathlib import Path


class BaseSkill(ABC):
    """
    Input:  skill_ref (str | Path)
    Output: content (str) injected into agent backstory
    Setup:  SKILL.md file in the skill directory
    """

    @property
    @abstractmethod
    def content(self) -> str: ...


class FileSkill(BaseSkill):
    """Read skill instructions from SKILL.md, stripping YAML frontmatter."""

    def __init__(self, skill_ref: str | Path) -> None:
        if isinstance(skill_ref, str):
            skills_root = Path(__file__).parent
            self._skill_path = skills_root / skill_ref / "SKILL.md"
        else:
            self._skill_path = Path(skill_ref) / "SKILL.md"

    @property
    def content(self) -> str:
        if not self._skill_path.exists():
            raise FileNotFoundError(f"SKILL.md not found: {self._skill_path}")
        raw = self._skill_path.read_text(encoding="utf-8")
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            return parts[2].strip() if len(parts) >= 3 else raw
        return raw
