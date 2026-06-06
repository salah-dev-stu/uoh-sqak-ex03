"""Rich terminal UI menu for article generation."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from agent_article.sdk.sdk import ArticleSDK
from agent_article.shared import version as ver

_console = Console()


def _header() -> None:
    _console.print(Panel(
        f"[bold cyan]Article Generator[/bold cyan]  v{ver.VERSION}\n"
        "Multi-Agent Orchestration Patterns — CrewAI Pipeline",
        title="[bold]uoh-sqak-ex03[/bold]",
        border_style="cyan",
    ))


def _show_config() -> None:
    summary = ArticleSDK.config_summary()
    table = Table(title="Current Configuration", show_header=True)
    table.add_column("Key", style="bold")
    table.add_column("Value")
    for k, v in summary.items():
        table.add_row(str(k), str(v))
    _console.print(table)


def _run_pipeline(sdk: ArticleSDK) -> None:
    topic = Prompt.ask("[bold]Enter article topic[/bold]",
                       default="Multi-Agent Orchestration Patterns")
    _console.print(f"\n[yellow]Starting pipeline for:[/yellow] {topic}")
    with _console.status("[bold green]Running 4-agent CrewAI pipeline...[/bold green]"):
        result = sdk.generate(topic)
    if result.success:
        _console.print(f"\n[bold green]✓ Done![/bold green] PDF at: {result.pdf_path}")
    else:
        _console.print(f"\n[bold red]✗ Failed:[/bold red] {result.errors}")


def _show_spend(sdk: ArticleSDK) -> None:
    report = sdk.spend_report()
    if not report:
        _console.print("[dim]No API calls recorded yet.[/dim]")
        return
    table = Table(title="Spend Report", show_header=True)
    table.add_column("Service", style="bold")
    table.add_column("Calls")
    table.add_column("Tokens")
    for svc, rec in report.items():
        table.add_row(svc, str(getattr(rec, "calls", "?")), str(getattr(rec, "tokens", "?")))
    _console.print(table)


def run_tui() -> None:
    """Entry point for the terminal UI."""
    _header()
    sdk = ArticleSDK()
    menu = {
        "1": ("Run article pipeline", lambda: _run_pipeline(sdk)),
        "2": ("Show configuration", _show_config),
        "3": ("Show spend report", lambda: _show_spend(sdk)),
        "4": ("Exit", None),
    }
    while True:
        _console.print("\n[bold]Menu[/bold]")
        for k, (label, _) in menu.items():
            _console.print(f"  [cyan]{k}[/cyan] — {label}")
        choice = Prompt.ask("Choice", choices=list(menu.keys()), default="1")
        label, action = menu[choice]
        if action is None:
            _console.print("[dim]Bye![/dim]")
            break
        action()
