from dotenv import load_dotenv
load_dotenv()

from workflow.graph import graph

config = {"configurable": {"thread_id": "demo-thread-004"}}

graph.invoke(
    {"query": "LangGraph 在生产级 Agent 工程中的应用价值"},
    config,
)

snapshot = graph.get_state(config)
print("next:", snapshot.next)
print("待审批报告（前 300 字）：")
print(snapshot.values["report_draft"][:300])