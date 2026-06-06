"""Immutable enumerations for agent_article."""
from enum import StrEnum


class AgentRole(StrEnum):
    RESEARCHER = "researcher"
    WRITER = "writer"
    EDITOR = "editor"
    LATEX_PRODUCER = "latex_producer"


class ServiceName(StrEnum):
    CLAUDE_CLI = "claude_cli"
    DUCKDUCKGO = "duckduckgo"
    LUALATEX = "lualatex"


class ProcessType(StrEnum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
