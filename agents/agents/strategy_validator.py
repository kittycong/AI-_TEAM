from __future__ import annotations

from pathlib import Path
from shared import BASE_DIR, ask_llm, write_report

SYSTEM_PROMPT = """
You are Bug Hunter.
Review code for:
- bugs
- edge cases
- incorrect assumptions
- risky logic
Return:
[BUG HUNTER]
- Findings
- Severity
- Fix suggestions
- Status: pass / fail / warning
- Confidence: 0~100
"""

def collect_code() -> str:
    chunks = []
    for path in BASE_DIR.rglob("*.py"):
        if ".github" in path.parts or "venv" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"\n### FILE: {path}\n{text[:12000]}")
        except Exception:
            continue
    return "\n".join(chunks)[:40000]

def run() -> str:
    code_snapshot = collect_code()
    prompt = f"Review this repository code:\n\n{code_snapshot}"
    result = ask_llm(SYSTEM_PROMPT, prompt)
    write_report("bug_hunter.md", result)
    return result

if __name__ == "__main__":
    print(run())
