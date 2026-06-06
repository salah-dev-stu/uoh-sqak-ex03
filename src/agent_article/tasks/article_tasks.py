"""Task definitions for the article-writing crew."""
from crewai import Task
from typing import TYPE_CHECKING

from agent_article.shared.config import cfg
from agent_article.shared.logging_fifo import StructuredLogger

if TYPE_CHECKING:
    from agent_article.agents.base_agent import BaseAgent

_log = StructuredLogger("tasks")


def _task_cfg(key: str, field: str) -> str:
    tasks = cfg("tasks", "tasks", {})
    return str(tasks.get(key, {}).get(field, ""))


def build_research_task(agent: "BaseAgent", topic: str) -> Task:
    """
    Input:  topic str
    Output: Task writing workspace/research_notes.md
    Setup:  config/tasks.json::research
    """
    desc = _task_cfg("research", "description").format(topic=topic)
    expected = _task_cfg("research", "expected_output")
    _log.info(f"Building research task for topic={topic!r}")
    return Task(
        description=desc,
        expected_output=expected,
        agent=agent.build(),
    )


def build_write_task(agent: "BaseAgent", topic: str, context: list[Task]) -> Task:
    """
    Input:  topic str, research task context
    Output: Task writing workspace/chapters/ch0N.md
    Setup:  config/tasks.json::write
    """
    desc = _task_cfg("write", "description").format(topic=topic)
    expected = _task_cfg("write", "expected_output")
    _log.info(f"Building write task for topic={topic!r}")
    return Task(
        description=desc,
        expected_output=expected,
        agent=agent.build(),
        context=context,
    )


def build_edit_task(agent: "BaseAgent", context: list[Task]) -> Task:
    """
    Input:  write task context (6 chapter files)
    Output: Task writing workspace/chapters/ch0N_edited.md
    Setup:  config/tasks.json::edit
    """
    desc = _task_cfg("edit", "description")
    expected = _task_cfg("edit", "expected_output")
    _log.info("Building edit task")
    return Task(
        description=desc,
        expected_output=expected,
        agent=agent.build(),
        context=context,
    )


def build_latex_task(agent: "BaseAgent", context: list[Task]) -> Task:
    """
    Input:  edit task context (6 edited chapters)
    Output: Task compiling latex/output/uoh-sqak-article.pdf
    Setup:  config/tasks.json::latex
    """
    desc = _task_cfg("latex", "description")
    expected = _task_cfg("latex", "expected_output")
    _log.info("Building latex task")
    return Task(
        description=desc,
        expected_output=expected,
        agent=agent.build(),
        context=context,
    )
