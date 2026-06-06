"""Researcher agent — searches the web and writes structured research notes."""
from crewai import Agent

from .base_agent import BaseAgent
from agent_article.tools.web_search import WebSearchTool
from agent_article.tools.file_rw import FileWriteTool


class ResearcherAgent(BaseAgent):
    """
    Input:  topic (str) via task description
    Output: workspace/research_notes.md
    Setup:  config/agents.json::researcher, researcher_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="researcher",
            tools=[WebSearchTool(), FileWriteTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
