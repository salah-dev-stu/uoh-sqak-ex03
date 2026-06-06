"""Generate matplotlib charts and save as PNG for LaTeX inclusion."""
from pathlib import Path
from typing import Any

from .base_tool import BaseTool


class ChartGeneratorTool(BaseTool):
    """
    Input:  chart_type, title, labels, values, ylabel, filename
    Output: str path to saved PNG file
    Setup:  output_dir defaults to latex/figures/
    """

    def __init__(self, output_dir: Path | None = None) -> None:
        if output_dir is not None:
            self._output_dir = output_dir
        else:
            from agent_article.shared.config import cfg
            latex_main = cfg("latex", "main_file", "latex/main.tex")
            self._output_dir = Path(latex_main).parent / "figures"

    @property
    def name(self) -> str:
        return "chart_generator"

    @property
    def description(self) -> str:
        return (
            "Generate a matplotlib chart and save as PNG. "
            "Args: chart_type (bar|line|pie), title (str), "
            "labels (list), values (list), ylabel (str), filename (str)"
        )

    def run(
        self,
        chart_type: str,
        title: str,
        labels: list,
        values: list,
        ylabel: str,
        filename: str,
        **_: Any,
    ) -> str:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        self._output_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 5))

        if chart_type == "bar":
            ax.bar(labels, values, color="#4C72B0")
        elif chart_type == "line":
            ax.plot(labels, values, marker="o", color="#4C72B0")
        elif chart_type == "pie":
            ax.pie(values, labels=labels, autopct="%1.1f%%")
        else:
            ax.bar(labels, values)

        ax.set_title(title, fontsize=14, fontweight="bold")
        if chart_type != "pie":
            ax.set_ylabel(ylabel)
        plt.tight_layout()

        output_path = self._output_dir / filename
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return str(output_path)
