"""Writer agent — produces Markdown chapters from research notes."""
from crewai import Agent

from .base_agent import BaseAgent
from agent_article.tools.file_rw import FileReadTool, FileWriteTool


class WriterAgent(BaseAgent):
    """
    Input:  workspace/research_notes.md (via context from ResearchTask)
    Output: workspace/chapters/ch01.md … ch06.md
    Setup:  config/agents.json::writer, writer_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="writer",
            tools=[FileReadTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
