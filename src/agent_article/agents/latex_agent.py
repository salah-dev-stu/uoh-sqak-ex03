"""LaTeX-Producer agent — converts Markdown to LaTeX and compiles PDF."""
from pathlib import Path

from crewai import Agent

from agent_article.tools.chart_generator import ChartGeneratorTool
from agent_article.tools.file_rw import FileReadTool, FileWriteTool
from agent_article.tools.latex_compile import LaTeXCompileTool

from .base_agent import BaseAgent

# Project root — agent must read from workspace/ AND write to latex/
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


class LaTeXAgent(BaseAgent):
    """
    Input:  workspace/chapters/*_edited.md (via context from EditingTask)
    Output: latex/output/uoh-sqak-article.pdf
    Setup:  config/agents.json::latex_producer, latex_skill/SKILL.md
    """

    def __init__(self) -> None:
        super().__init__(
            config_key="latex_producer",
            tools=[
                FileReadTool(base_dir=_PROJECT_ROOT),
                FileWriteTool(base_dir=_PROJECT_ROOT),
                LaTeXCompileTool(),
                ChartGeneratorTool(),
            ],
        )

    def build(self) -> Agent:
        return self._make_agent()
