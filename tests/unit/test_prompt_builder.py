"""Tests for crew/prompt_builder.py."""
from unittest.mock import MagicMock

from agent_article.crew.prompt_builder import (
    _MAX_CTX_CHARS,
    build_prompt,
    extract_chapter_excerpt,
)


def _make_task(description: str, out_path: str, raw_ctx: str | None = None) -> MagicMock:
    task = MagicMock()
    task.description = description
    task.output_file = out_path
    if raw_ctx is None:
        task.context = []
    else:
        ctx = MagicMock()
        ctx.output = MagicMock()
        ctx.output.raw = raw_ctx
        task.context = [ctx]
    return task


def test_build_prompt_no_context():
    task = _make_task("Write LaTeX", "latex/chapters/ch01_introduction.tex")
    assert build_prompt(task) == "Write LaTeX"


def test_build_prompt_appends_excerpt():
    raw = "## **ch01_edited** — Introduction\nSome intro text\n## **ch02_edited**\nOther"
    task = _make_task("Write", "latex/chapters/ch01_introduction.tex", raw)
    prompt = build_prompt(task)
    assert "Write" in prompt
    assert "intro text" in prompt
    assert "Other" not in prompt


def test_build_prompt_caps_at_max_chars():
    raw = "## **ch05_edited** — BiDi\n" + "x" * (_MAX_CTX_CHARS + 5000)
    task = _make_task("Desc", "latex/chapters/ch05_bidi.tex", raw)
    prompt = build_prompt(task)
    ctx_part = prompt[len("Desc\n\nContext from previous task:\n"):]
    assert len(ctx_part) <= _MAX_CTX_CHARS


def test_extract_chapter_excerpt_known_chapter():
    raw = (
        "prefix\n"
        "## **ch03_edited** — Frameworks\nFrame content\n"
        "## **ch04_edited** — Production\nProd content\n"
    )
    excerpt = extract_chapter_excerpt(raw, "latex/chapters/ch03_frameworks.tex")
    assert "Frame content" in excerpt
    assert "Prod content" not in excerpt


def test_extract_chapter_excerpt_unknown_returns_full():
    raw = "some content"
    assert extract_chapter_excerpt(raw, "latex/chapters/unknown.tex") == raw


def test_extract_chapter_excerpt_bib():
    raw = "chapters done\n## **references.bib**\n@article{key, ...}\n"
    excerpt = extract_chapter_excerpt(raw, "latex/bib/references.bib")
    assert "@article" in excerpt


def test_extract_chapter_excerpt_not_found_returns_full():
    raw = "no matching header here"
    result = extract_chapter_excerpt(raw, "latex/chapters/ch01_introduction.tex")
    assert result == raw
