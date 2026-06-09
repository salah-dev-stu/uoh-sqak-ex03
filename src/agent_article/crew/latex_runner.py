"""Parallel LaTeX task runner — clean, write, and compile per-chapter tasks."""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

from agent_article.crew.prompt_builder import build_prompt
from agent_article.shared.logging_fifo import StructuredLogger

if TYPE_CHECKING:
    from crewai import Task

_log = StructuredLogger("latex_runner")


def clean_latex(raw: str) -> str:
    """Strip markdown fences and leading prose; return clean LaTeX/BibTeX or ''."""
    lines = raw.splitlines()
    start, end, open_fence = 0, len(lines), -1
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
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
            return ""
    return "\n".join(lines[start:end]).strip()


def run_single_latex_task(task: Task, retries: int = 2) -> str:
    """Run one LaTeX task: call LLM, clean output, write to output_file."""
    tid = threading.current_thread().name
    out_path = task.output_file or ""
    _log.info(f"[{tid}] latex task start: {out_path}")
    for attempt in range(retries + 1):
        try:
            prompt = build_prompt(task)
            raw = task.agent.llm.call(prompt)
            clean = clean_latex(raw)
            if not clean:
                preview = (raw[:300].replace("\n", " ")) if raw else "<empty>"
                _log.warning(f"[{tid}] attempt {attempt + 1}: empty LaTeX {out_path}. raw={preview!r}")
                if attempt < retries:
                    continue
                _log.error(f"[{tid}] all retries exhausted {out_path}")
                return ""
            if out_path:
                Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                Path(out_path).write_text(clean, encoding="utf-8")
            _log.info(f"[{tid}] latex task done: {out_path}")
            return out_path
        except Exception as exc:
            if attempt < retries:
                _log.warning(f"[{tid}] attempt {attempt + 1} failed {out_path}: {exc!r}, retrying")
            else:
                _log.error(f"[{tid}] latex task failed {out_path}: {exc}")
                return ""
    return ""


def run_latex_phase_parallel(tasks: list[Task]) -> list[str]:
    """Run all LaTeX tasks in parallel (up to 4 workers)."""
    if not tasks:
        return []
    max_w = min(len(tasks), 4)
    _log.info(f"Parallel LaTeX phase: {len(tasks)} tasks, {max_w} workers")
    with ThreadPoolExecutor(max_workers=max_w) as pool:
        futures = {pool.submit(run_single_latex_task, t): t for t in tasks}
        return [f.result() for f in as_completed(futures)]
