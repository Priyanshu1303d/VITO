from VITO.graph.state import AgentState


def route_after_decide(state: AgentState) -> str:
    action = state.get("action", "")
    if action == "followup":
        return "ask_followup"
    if action == "escalate":
        return "escalate_request"
    return "resolve_request"


def route_after_validate(state: AgentState) -> str:
    return "create_ticket"
