from VITO.graph.edges import route_after_decide


def test_followup_on_missing_fields():
    state = {"action": "followup", "missing_fields": []}
    assert route_after_decide(state) == "ask_followup"


def test_escalate_on_escalate_action():
    state = {"action": "escalate", "missing_fields": []}
    assert route_after_decide(state) == "escalate_request"


def test_resolve_on_ticket_action():
    state = {"action": "ticket", "missing_fields": []}
    assert route_after_decide(state) == "resolve_request"


def test_resolve_on_self_service():
    state = {"action": "self_service", "missing_fields": []}
    assert route_after_decide(state) == "resolve_request"
