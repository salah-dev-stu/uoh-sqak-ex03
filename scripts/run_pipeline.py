"""Non-interactive pipeline runner — calls SDK directly, bypasses TUI."""
import sys

from agent_article.sdk.sdk import ArticleSDK


def main() -> int:
    topic = " ".join(sys.argv[1:]) or "Multi-Agent Orchestration Patterns"
    print(f"\n==> Running pipeline for: {topic!r}\n")
    sdk = ArticleSDK()
    result = sdk.generate(topic)
    if result.success:
        print(f"\n✓ Done! PDF: {result.pdf_path}")
        report = sdk.spend_report()
        if report:
            print(f"  Spend: {report}")
        return 0
    print(f"\n✗ Failed: {result.errors}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
