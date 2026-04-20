from __future__ import annotations

from shared import ask_llm, write_report

SYSTEM_PROMPT = """
You are Scalping Researcher 1.
Analyze existing scalping strategies.

Return:
[SCALPING RESEARCH 1]
- Existing strategy patterns
- Entry/exit logic
- Weaknesses
- Status: pass / fail / warning
- Confidence: 0~100
"""

def run() -> str:
    prompt = """
Analyze common scalping strategy structures for:
- momentum spikes
- mean reversion moves
- breakout scalping
Focus on robustness and practical execution.
"""
    result = ask_llm(SYSTEM_PROMPT, prompt)
    write_report("scalp_research_1.md", result)
    return result

if __name__ == "__main__":
    print(run())
