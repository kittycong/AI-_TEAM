from shared import ask_llm, write_report

def run():
    result = "Bug Hunter 실행됨 (테스트)"
    write_report("bug_hunter.md", result)
    return result
