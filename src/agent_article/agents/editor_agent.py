"""Editor agent — polishes chapters and prepares them for LaTeX conversion."""
from crewai import Agent

from agent_article.tools.file_rw import FileReadTool, FileWriteTool

from .base_agent import BaseAgent


class EditorAgent(BaseAgent):
    """
    Input:  workspace/chapters/ch*.md (via context from WritingTask)
    Output: workspace/chapters/ch*_edited.md
    Setup:  config/agents.json::editor, editor_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="editor",
            tools=[FileReadTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
