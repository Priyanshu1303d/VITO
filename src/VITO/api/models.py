from pydantic import BaseModel


class ChatRequest(BaseModel):
    employee: str
    message: str


class ChatResponse(BaseModel):
    response_text: str
    action: str | None = None
    category: str | None = None
    kb_source: str = ""
    ticket_id: str = ""
    escalation_reason: str = ""
