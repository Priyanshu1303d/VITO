from typing import TypedDict


class AgentState(TypedDict):
    employee: str
    message: str
    category: str | None
    missing_fields: list[str]
    kb_matches: list[dict]
    action: str | None
    response_text: str | None
    escalation_reason: str | None
    ticket: dict | None
