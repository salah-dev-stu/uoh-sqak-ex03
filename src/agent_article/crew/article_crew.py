"""Article-writing CrewAI crew — sequential 3-agent phase + parallel LaTeX phase."""
from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from crewai import Crew, Process

from agent_article.agents.editor_agent import EditorAgent
from agent_article.agents.researcher_agent import ResearcherAgent
from agent_article.agents.writer_agent import WriterAgent
from agent_article.shared.config import cfg
from agent_article.shared.logging_fifo import StructuredLogger
from agent_article.tasks.article_tasks import (
    build_edit_task,
    build_latex_tasks,
    build_research_task,
    build_write_task,
)

if TYPE_CHECKING:
    from crewai import Task

_log = StructuredLogger("crew")


def _clean_latex(raw: str) -> str:
    """Strip markdown fences and leading/trailing prose; return clean LaTeX/BibTeX."""
    lines = raw.splitlines()
    start, end, open_fence = 0, len(lines), -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            if open_fence < 0:
                open_fence = i
                start = i + 1
            else:
                end = i
                break
    if open_fence < 0:
        for i, line in enumerate(lines):
            if line.strip().startswith(("%", "\\", "@")):
                start = i
                break
        else:
            # No LaTeX/BibTeX content found at all — return empty to prevent
            # writing a Markdown prose file that breaks compilation.
            return ""
    return "\n".join(lines[start:end]).strip()


@dataclass
class CrewResult:
    """
    Input:  Crew kickoff result
    Output: pdf_path str, raw_output str
    Setup:  auto-populated by ArticleCrew.run()
    """

    pdf_path: str = ""
    raw_output: str = ""
    success: bool = False
    errors: list[str] = field(default_factory=list)


class ArticleCrew:
    """
    Input:  topic str
    Output: CrewResult with pdf_path
    Setup:  agents/tasks built lazily on run()
    """

    def __init__(self, topic: str) -> None:
        self._topic = topic
        self._workspace = Path(cfg("setup", "workspace_dir", "workspace"))
        self._workspace.mkdir(parents=True, exist_ok=True)

    def _build_prompt(self, task: Task) -> str:
        """Combine task description with context outputs (editor's content)."""
        prompt = task.description
        for ctx in task.context or []:
            output = getattr(ctx, "output", None)
            raw_ctx = getattr(output, "raw", None) if output else None
            if raw_ctx:
                prompt = f"{prompt}\n\nContext from previous task:\n{raw_ctx}"
        return prompt

    def _run_single_latex_task(self, task: Task) -> str:
        tid = threading.current_thread().name
        out_path = task.output_file or ""
        _log.info(f"[{tid}] latex task start: {out_path}")
        try:
            prompt = self._build_prompt(task)
            raw = task.agent.llm.call(prompt)
            clean = _clean_latex(raw)
            if out_path:
                Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                Path(out_path).write_text(clean, encoding="utf-8")
            _log.info(f"[{tid}] latex task done: {out_path}")
            return out_path
        except Exception as exc:
            _log.error(f"[{tid}] latex task failed {out_path}: {exc}")
            return ""

    def _run_latex_phase_parallel(self, tasks: list[Task]) -> list[str]:
        if not tasks:
            return []
        max_w = min(len(tasks), os.cpu_count() or 4)
        _log.info(f"Parallel LaTeX phase: {len(tasks)} tasks, {max_w} workers")
        with ThreadPoolExecutor(max_workers=max_w) as pool:
            futures = {pool.submit(self._run_single_latex_task, t): t for t in tasks}
            return [f.result() for f in as_completed(futures)]

    def run(self) -> CrewResult:
        """Execute the full pipeline: sequential 3-agent phase, parallel LaTeX phase."""
        _log.info(f"Starting crew run for topic={self._topic!r}")
        result = CrewResult()
        try:
            researcher = ResearcherAgent()
            writer = WriterAgent()
            editor = EditorAgent()

            t_research = build_research_task(researcher, self._topic)
            t_write = build_write_task(writer, self._topic, [t_research])
            t_edit = build_edit_task(editor, [t_write])

            seq_crew = Crew(
                agents=[researcher.build(), writer.build(), editor.build()],
                tasks=[t_research, t_write, t_edit],
                process=Process.sequential,
                verbose=True,
                respect_context_window=True,
            )
            output = seq_crew.kickoff()
            result.raw_output = str(output)

            latex_tasks = build_latex_tasks([t_edit])
            self._run_latex_phase_parallel(latex_tasks)

            compiled = self._compile_pdf()
            output_filename = cfg("setup", "output_filename", "uoh-sqak-article.pdf")
            pdf_path = Path("latex/output") / output_filename
            if compiled:
                import shutil
                shutil.copy2(compiled, pdf_path)
            result.pdf_path = str(pdf_path)
            result.success = True
            _log.info(f"Crew run complete: pdf_path={result.pdf_path}")
        except Exception as exc:
            result.errors.append(str(exc))
            _log.error(f"Crew run failed: {exc}")
        return result

    def _compile_pdf(self) -> Path | None:
        """Run lualatex→biber→lualatex→lualatex and return the compiled PDF path."""
        from agent_article.tools.latex_compile import LaTeXCompileTool
        try:
            tool = LaTeXCompileTool()
            pdf = tool.run("main.tex")
            _log.info(f"LaTeX compile succeeded: {pdf}")
            return Path(pdf)
        except Exception as exc:
            _log.error(f"LaTeX compile failed: {exc}")
            return None
