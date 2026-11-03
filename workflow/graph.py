import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from workflow.state import WorkflowState
from workflow.nodes import (
    search_node, analyze_node, report_node, approval_node,
)
import json
from pathlib import Path

LEDGER = Path("export_ledger.json")


def _load_ledger() -> dict:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text(encoding="utf-8"))
    return {}


def _save_ledger(ledger: dict) -> None:
    LEDGER.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def export_node(state: WorkflowState, config):
    thread_id = config["configurable"]["thread_id"]
    key = f"{thread_id}:export"

    ledger = _load_ledger()
    if key in ledger:
        print(f"[export] 幂等命中，跳过重复导出：{key}")
        return {"export_done": True}

    content = state.get("edited_report") or state["report_draft"]
    out_path = Path(f"exports/{thread_id}.md")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(content, encoding="utf-8")

    ledger[key] = {"file": str(out_path), "source": "edited" if state.get("edited_report") else "draft"}
    _save_ledger(ledger)

    print(f"[export] 已导出到 {out_path}")
    return {"export_done": True}

builder = StateGraph(WorkflowState)

builder.add_node("search", search_node)
builder.add_node("analyze", analyze_node)
builder.add_node("report", report_node)
builder.add_node("approval", approval_node)
builder.add_node("export", export_node)

builder.add_edge(START, "search")
builder.add_edge("search", "analyze")
builder.add_edge("analyze", "report")
builder.add_edge("report", "approval")


def route_after_approval(state: WorkflowState):
    if state["approval_decision"] == "reject":
        return END
    return "export"


builder.add_conditional_edges(
    "approval",
    route_after_approval,
    {"export": "export", END: END},
)
builder.add_edge("export", END)

conn = sqlite3.connect("workflow_checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
graph = builder.compile(checkpointer=checkpointer)