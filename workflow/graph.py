from langgraph.graph import StateGraph, START, END

from workflow.state import WorkflowState
from workflow.nodes import search_node, analyze_node, report_node

# 1. 建图，告诉它 State 的形状
builder = StateGraph(WorkflowState)

# 2. 注册节点：第一个参数是“节点名”（图内部用的标识），第二个是函数
builder.add_node("search", search_node)
builder.add_node("analyze", analyze_node)
builder.add_node("report", report_node)

# 3. 连边：固定路线
builder.add_edge(START, "search")      # 入口
builder.add_edge("search", "analyze")
builder.add_edge("analyze", "report")
builder.add_edge("report", END)        # 出口

# 4. 编译成可执行对象
graph = builder.compile()