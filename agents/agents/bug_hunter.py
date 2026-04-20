from __future__ import annotations

from pathlib import Path
from shared import ask_llm, write_report

SYSTEM_PROMPT = """
You are Bug Hunter.

Review repository code for:
- bugs
- edge cases
- incorrect assumptions
- risky logic

Return in markdown:
# BUG HUNTER
- Findings
- Severity
- Suggested fixes

# FINAL
- Status: pass / fail / warning
- Confidence: 0-100
""".strip()


def collect_code() -> str:
    base = Path(__file__).resolve().parent.parent
    chunks = []

    for path in base.rglob("*.py"):
        if any(part in {".git", ".github", "__pycache__", "reports", ".venv", "venv"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            chunks.append(f"\n### FILE: {path.relative_to(base)}\n{text[:8000]}")
        except Exception:
            continue

    return "\n".join(chunks)[:40000]


def run() -> str:
    repo_context = collect_code()
    user_prompt = f"Review this repository code:\n\n{repo_context}"
    result = ask_llm(SYSTEM_PROMPT, user_prompt)
    write_report("bug_hunter.md", result)
    return result


if __name__ == "__main__":
    print(run())
