from langgraph.graph import StateGraph, START, END
from VITO.graph.state import AgentState
from VITO.graph import nodes, edges

graph = StateGraph(AgentState)
_node_names = [
    "classify_issue", "retrieve_policy", "decide_action",
    "ask_followup", "resolve_request", "escalate_request",
    "validate_output", "create_ticket", "write_audit",
]
for name in _node_names:
    graph.add_node(name, getattr(nodes, name))

graph.add_edge(START, "classify_issue")
graph.add_edge("classify_issue", "retrieve_policy")
graph.add_edge("retrieve_policy", "decide_action")
graph.add_conditional_edges("decide_action", edges.route_after_decide)
graph.add_edge("ask_followup", END)
graph.add_edge("resolve_request", "validate_output")
graph.add_edge("escalate_request", "validate_output")
graph.add_edge("validate_output", "create_ticket")
graph.add_edge("create_ticket", "write_audit")
graph.add_edge("write_audit", END)

app = graph.compile()
