from dotenv import load_dotenv
load_dotenv()

from langgraph.types import Command
from workflow.graph import graph

QUERY = "LangGraph 在生产级 Agent 工程中的应用价值"


def run_path(thread_id: str, decision: dict, label: str):
    config = {"configurable": {"thread_id": thread_id}}

    # 1) 跑到 approval 暂停
    graph.invoke({"query": QUERY}, config)
    snap = graph.get_state(config)
    print(f"[{label}] 暂停时 next =", snap.next)

    # 2) 用人工决策恢复
    result = graph.invoke(Command(resume=decision), config)

    print(f"[{label}] approval_decision =", result.get("approval_decision"))
    print(f"[{label}] export_done      =", result.get("export_done"))
    print(f"[{label}] edited_report    =", repr(result.get("edited_report"))[:60])
    print("-" * 60)


run_path("path-approve", {"action": "approve"}, "approve")
run_path("path-reject",  {"action": "reject"},  "reject")
run_path("path-edit",    {"action": "edit", "edited_content": "# 人工修改版报告\n这是审批人改过的版本。"}, "edit")