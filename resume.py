from dotenv import load_dotenv
load_dotenv()

from langgraph.types import Command
from workflow.graph import graph

config = {"configurable": {"thread_id": "demo-thread-003"}}

result = graph.invoke(
    Command(resume={"action": "approve"}),
    config,
)

print("approval_decision:", result["approval_decision"])
print("export_done:", result["export_done"])