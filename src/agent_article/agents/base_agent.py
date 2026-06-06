"""Abstract base for all CrewAI agents in the article pipeline."""
from abc import ABC, abstractmethod

from crewai import Agent

from agent_article.shared.config import get_config
from agent_article.skills.base_skill import FileSkill
from agent_article.tools.base_tool import BaseTool


class BaseAgent(ABC):
    """
    Input:  config_key (str) — key in config/agents.json
    Output: crewai.Agent via build()
    Setup:  config/agents.json, skills/<config_key>/SKILL.md
    """

    def __init__(self, config_key: str, tools: list[BaseTool]) -> None:
        self._cfg = get_config("agents")["agents"][config_key]
        self._skill = FileSkill(self._cfg["skill_ref"])
        self._tools = tools

    @abstractmethod
    def build(self) -> Agent: ...

    def _make_agent(self) -> Agent:
        backstory = self._cfg["backstory"] + "\n\n---\n\n" + self._skill.content
        return Agent(
            role=self._cfg["role"],
            goal=self._cfg["goal"],
            backstory=backstory,
            tools=[t.as_crewai_tool() for t in self._tools],
            verbose=True,
        )
