from __future__ import annotations

from pathlib import Path
from shared import BASE_DIR, ask_llm, write_report

SYSTEM_PROMPT = """
You are Strategy Validator.
Check:
- overfitting risk
- risk/reward quality
- real-world feasibility
Return:
[STRATEGY VALIDATOR]
- Strengths
- Weaknesses
- Risk flags
- Status: pass / fail / warning
- Confidence: 0~100
"""

def collect_strategy_docs() -> str:
    chunks = []
    for path in list(BASE_DIR.rglob("*.md")) + list(BASE_DIR.rglob("*.py")):
        if "reports" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(k in text.lower() for k in ["strategy", "signal", "backtest", "entry", "exit"]):
                chunks.append(f"\n### FILE: {path}\n{text[:10000]}")
        except Exception:
            continue
    return "\n".join(chunks)[:40000]

def run() -> str:
    repo_context = collect_strategy_docs()
    prompt = f"Evaluate the strategy logic in this repository:\n\n{repo_context}"
    result = ask_llm(SYSTEM_PROMPT, prompt)
    write_report("strategy_validator.md", result)
    return result

if __name__ == "__main__":
    print(run())
