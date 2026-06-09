"""Debug script to time each stage of the pipeline."""
import time


def timed(label):
    t0 = time.time()
    print(f"[START] {label}")
    return t0


def done(label, t0):
    print(f"[DONE ] {label} — {time.time()-t0:.1f}s")


t_total = timed("import config")
import agent_article.shared.config as cfg_mod  # noqa: E402

done("import config", t_total)

t = timed("reload config")
cfg_mod.reload()
done("reload config", t)

t = timed("import ClaudeCLILLM")
from agent_article.shared.claude_cli_llm import ClaudeCLILLM  # noqa: E402

done("import ClaudeCLILLM", t)

t = timed("instantiate ClaudeCLILLM")
llm = ClaudeCLILLM()
done("instantiate ClaudeCLILLM", t)

t = timed("llm.call (one round-trip)")
response = llm.call("Reply with exactly 3 words: what is CrewAI?")
print(f"  response: {response!r}")
done("llm.call", t)

t = timed("import ResearcherAgent")
from agent_article.agents.researcher_agent import ResearcherAgent  # noqa: E402

done("import ResearcherAgent", t)

t = timed("build ResearcherAgent")
agent = ResearcherAgent()
done("build ResearcherAgent", t)

t = timed("ResearcherAgent.build() → crewai.Agent")
from unittest.mock import patch  # noqa: E402

with patch("agent_article.agents.base_agent.Agent") as mock:
    import unittest.mock  # noqa: E402
    mock.return_value = unittest.mock.MagicMock()
    agent.build()
done("ResearcherAgent.build()", t)

t = timed("import Crew + Process")

done("import Crew + Process", t)

print("\nDone. Longest step is the bottleneck.")
