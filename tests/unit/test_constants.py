"""Tests for constants.py."""
from agent_article.constants import AgentRole, ServiceName, ProcessType


def test_agent_role_values() -> None:
    assert AgentRole.RESEARCHER == "researcher"
    assert AgentRole.WRITER == "writer"
    assert AgentRole.EDITOR == "editor"
    assert AgentRole.LATEX_PRODUCER == "latex_producer"


def test_service_name_values() -> None:
    assert ServiceName.CLAUDE_CLI == "claude_cli"
    assert ServiceName.DUCKDUCKGO == "duckduckgo"
    assert ServiceName.LUALATEX == "lualatex"


def test_process_type_values() -> None:
    assert ProcessType.SEQUENTIAL == "sequential"
    assert ProcessType.HIERARCHICAL == "hierarchical"


def test_agent_roles_are_strings() -> None:
    for role in AgentRole:
        assert isinstance(str(role), str)
