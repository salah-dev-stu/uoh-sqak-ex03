"""Task definitions for the article-writing crew."""
from typing import TYPE_CHECKING

from crewai import Task

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


# Per-chapter LaTeX conversion tasks — each has output_file so CrewAI writes
# the agent's Final Answer directly to disk without needing a tool call.
_LATEX_CHAPTERS = [
    ("latex_ch01", "latex/chapters/ch01_introduction.tex"),
    ("latex_ch02", "latex/chapters/ch02_architectures.tex"),
    ("latex_ch03", "latex/chapters/ch03_frameworks.tex"),
    ("latex_ch04", "latex/chapters/ch04_production.tex"),
    ("latex_ch05", "latex/chapters/ch05_bidi.tex"),
    ("latex_ch06", "latex/chapters/ch06_casestudy.tex"),
    ("latex_bib",  "latex/bib/references.bib"),
]


def build_latex_tasks(agent: "BaseAgent", context: list[Task]) -> list[Task]:
    """
    Input:  edit task context (6 edited chapters)
    Output: list[Task] — one per chapter + bibliography, each with output_file
    Setup:  config/tasks.json::latex_ch01..latex_bib
    """
    tasks: list[Task] = []
    agent_obj = agent.build()
    for cfg_key, output_path in _LATEX_CHAPTERS:
        desc = _task_cfg(cfg_key, "description")
        expected = _task_cfg(cfg_key, "expected_output")
        _log.info(f"Building latex task key={cfg_key!r} output={output_path!r}")
        task = Task(
            description=desc,
            expected_output=expected,
            agent=agent_obj,
            context=context if not tasks else [tasks[-1]],
            output_file=output_path,
        )
        tasks.append(task)
    return tasks


# Keep old name as alias so any external callers don't break immediately.
def build_latex_task(agent: "BaseAgent", context: list[Task]) -> Task:
    """Deprecated — use build_latex_tasks() which returns a list."""
    return build_latex_tasks(agent, context)[0]
