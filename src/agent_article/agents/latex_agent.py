"""LaTeX-Producer agent — converts Markdown to LaTeX and compiles PDF."""
from crewai import Agent

from .base_agent import BaseAgent
from agent_article.tools.file_rw import FileReadTool, FileWriteTool
from agent_article.tools.latex_compile import LaTeXCompileTool
from agent_article.tools.chart_generator import ChartGeneratorTool


class LaTeXAgent(BaseAgent):
    """
    Input:  workspace/chapters/*_edited.md (via context from EditingTask)
    Output: latex/output/uoh-sqak-article.pdf
    Setup:  config/agents.json::latex_producer, latex_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="latex_producer",
            tools=[FileReadTool(), FileWriteTool(), LaTeXCompileTool(), ChartGeneratorTool()],
        )

    def build(self) -> Agent:
        return self._make_agent()
