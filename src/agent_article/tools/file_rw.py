"""File read/write tools for agent workspace."""
from pathlib import Path
from typing import Any

from .base_tool import BaseTool


class FileWriteTool(BaseTool):
    """
    Input:  relative_path (str), content (str)
    Output: str confirmation message
    Setup:  base_dir defaults to workspace_dir from config
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir is not None:
            self._base = base_dir
        else:
            from agent_article.shared.config import cfg
            self._base = Path(cfg("setup", "workspace_dir", "workspace"))

    @property
    def name(self) -> str:
        return "file_write"

    @property
    def description(self) -> str:
        return "Write text content to a file under workspace. Args: relative_path (str), content (str)"

    def run(self, relative_path: str, content: str, **_: Any) -> str:
        target = self._base / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Written: {target}"


class FileReadTool(BaseTool):
    """
    Input:  relative_path (str)
    Output: str file contents
    Setup:  base_dir defaults to workspace_dir from config
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        if base_dir is not None:
            self._base = base_dir
        else:
            from agent_article.shared.config import cfg
            self._base = Path(cfg("setup", "workspace_dir", "workspace"))

    @property
    def name(self) -> str:
        return "file_read"

    @property
    def description(self) -> str:
        return "Read text content from a file under workspace. Args: relative_path (str)"

    def run(self, relative_path: str, **_: Any) -> str:
        target = self._base / relative_path
        if not target.exists():
            raise FileNotFoundError(f"File not found: {target}")
        return target.read_text(encoding="utf-8")
