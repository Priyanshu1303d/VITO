from pydantic import BaseModel


class ChatRequest(BaseModel):
    employee: str
    message: str


class ClassifyResult(BaseModel):
    category: str
    missing_fields: list[str] = []


class DecideResult(BaseModel):
    action: str
    escalation_reason: str = ""
    response_text: str = ""
