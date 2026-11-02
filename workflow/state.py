from typing import TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages


class WorkflowState(TypedDict):
    # ---- 输入 ----
    query: str

    # ---- 各节点产出 ----
    search_results: Annotated[list, operator.add]
    analysis: str
    report_draft: str
    approval_decision: str | None
    edited_report: str | None
    export_done: bool

    # ---- 对话/日志（可选，后面可观测性会用到）----
    messages: Annotated[list, add_messages]