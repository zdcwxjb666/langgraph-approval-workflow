from langgraph.types import Command
from workflow.graph import graph

config = {"configurable": {"thread_id": "idem-test-001"}}

# 第一次：跑到 approval 暂停
graph.invoke({"query": "LangGraph 在生产级 Agent 工程中的应用价值"}, config)
print("next:", graph.get_state(config).next)

# 第一次恢复：应该真正导出
r1 = graph.invoke(Command(resume={"action": "approve"}), config)
print("第一次恢复 export_done:", r1.get("export_done"))

# 第二次恢复：模拟重复点击/重试
try:
    r2 = graph.invoke(Command(resume={"action": "approve"}), config)
    print("第二次恢复 export_done:", r2.get("export_done"))
except Exception as e:
    print("第二次恢复异常（也符合预期）：", type(e).__name__, e)