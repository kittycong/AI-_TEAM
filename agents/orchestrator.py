from __future__ import annotations

from pathlib import Path
from shared import ask_llm, write_report

import bug_hunter
import strategy_validator
import scalp_research_1

SYSTEM_PROMPT = """
You are the Main Orchestrator.

Responsibilities:
- collect outputs from all agents
- resolve conflicts
- prioritize findings
- produce final decision

Return in markdown:
# FINAL DECISION
- Overall status:
- Priority issues:
- Recommended next action:

# AGENT SUMMARY
- each agent summary

# TOP FIXES
1.
2.
3.
"""

def run() -> str:
    outputs = []
    outputs.append(bug_hunter.run())
    outputs.append(strategy_validator.run())
    outputs.append(scalp_research_1.run())

    combined = "\n\n".join(outputs)
    final = ask_llm(SYSTEM_PROMPT, combined, model="gpt-4.1")
    write_report("final_report.md", final)
    return final

if __name__ == "__main__":
    print(run())
