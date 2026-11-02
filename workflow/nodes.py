from workflow.state import WorkflowState
from workflow.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
import json

def search_node(state: WorkflowState):
    query = state["query"]
    mock_results = [
        f"【背景】LangGraph 是 LangChain 团队推出的 Agent 工作流编排框架，"
        f"用 StateGraph 把流程建模为「节点函数 + 路由边」，节点间通过共享 State 传递数据，"
        f"相比线性 Chain 更适合多步、有分支、需要状态管理的场景。与本问题「{query}」相关。",

        "【最新动态】LangGraph 内置 checkpoint 机制（SqliteSaver / PostgresSaver）"
        "和 interrupt 人工中断原语，使「暂停 → 人工审批 → 从断点恢复」成为执行器的一等能力，"
        "而不是业务代码里手写的 try-catch。这是它区别于普通 Agent 框架的核心卖点。",

        "【争议点】LangGraph 相比简单 Chain 有明显学习曲线，对纯线性任务可能属于过度设计；"
        "但对需要人工介入、需要审计轨迹、需要跨进程恢复的生产场景，收益远大于成本。"
        "招聘市场上「LangGraph、Agent 工作流、状态编排」关键词出现频率上升，也侧面印证了这一点。",
    ]
    return {"search_results": mock_results}

def analyze_node(state: WorkflowState):
    results_text = "\n".join(state["search_results"])
    response = llm.invoke([
        SystemMessage(content="你是分析助手。基于给定资料，提炼 3-5 条关键结论，不要编造资料之外的信息。"),
        HumanMessage(content=f"用户问题：{state['query']}\n\n资料：\n{results_text}"),
    ])
    return {"analysis": response.content}

def report_node(state: WorkflowState):
    response = llm.invoke([
        SystemMessage(content="你是报告撰写助手。基于分析结论，写一份结构清晰的中文报告草稿，包含：背景、关键发现、建议。"),
        HumanMessage(content=f"分析结论：\n{state['analysis']}"),
    ])
    return {"report_draft": response.content}