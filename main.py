from workflow.graph import graph

result = graph.invoke({
    "query": "LangGraph 在生产级 Agent 工程中的应用价值",
})

print("=" * 40)
print("search_results：", result["search_results"])
print("=" * 40)
print("analysis：", result["analysis"])
print("=" * 40)
print("report_draft（前 500 字）：", result["report_draft"][:500])