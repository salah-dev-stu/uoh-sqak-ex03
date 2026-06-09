"""Prompt-assembly utilities for the parallel LaTeX phase."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from crewai import Task

_MAX_CTX_CHARS = 12_000

_CHAPTER_MARKERS: dict[str, list[str]] = {
    "ch01": ["ch01_edited", "Chapter 1", "Introduction"],
    "ch02": ["ch02_edited", "Chapter 2", "Architectures"],
    "ch03": ["ch03_edited", "Chapter 3", "Framework"],
    "ch04": ["ch04_edited", "Chapter 4", "Production"],
    "ch05": ["ch05_edited", "Chapter 5", "BiDi", "bidi"],
    "ch06": ["ch06_edited", "Chapter 6", "Case Study"],
    "ch07": ["ch07_edited", "Chapter 7", "Conclusion"],
    "references.bib": ["bibliography", "Bibliography", "BIBLIOGRAPHY", "references.bib"],
}

_NEXT_SECTION_PREFIXES = ("## **ch0", "## **references", "## **Bibliography")


def _chapter_key(out_path: str) -> str | None:
    for key in _CHAPTER_MARKERS:
        if key in out_path:
            return key
    return None


def extract_chapter_excerpt(raw_ctx: str, out_path: str) -> str:
    """Return only the editor-output section relevant to out_path."""
    key = _chapter_key(out_path)
    if key is None:
        return raw_ctx
    markers = _CHAPTER_MARKERS[key]
    lines = raw_ctx.splitlines()
    start_idx = next(
        (i for i, ln in enumerate(lines) if any(m in ln for m in markers)), -1
    )
    if start_idx < 0:
        return raw_ctx
    end_idx = next(
        (i for i in range(start_idx + 4, len(lines))
         if any(lines[i].startswith(p) for p in _NEXT_SECTION_PREFIXES)),
        len(lines),
    )
    return "\n".join(lines[start_idx:end_idx])


def build_prompt(task: "Task") -> str:
    """Combine task description with a capped, chapter-targeted context excerpt."""
    prompt = task.description
    out_path = task.output_file or ""
    for ctx in task.context or []:
        output = getattr(ctx, "output", None)
        raw_ctx = getattr(output, "raw", None) if output else None
        if not raw_ctx:
            continue
        excerpt = extract_chapter_excerpt(raw_ctx, out_path)
        if len(excerpt) > _MAX_CTX_CHARS:
            excerpt = excerpt[:_MAX_CTX_CHARS]
        prompt = f"{prompt}\n\nContext from previous task:\n{excerpt}"
    return prompt
