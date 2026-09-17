from pydantic import BaseModel


class Ticket(BaseModel):
    id: str
    employee: str
    issue: str
    status: str
    category: str = ""
    kb_source: str = ""
    resolution: str = ""
    closed: bool = False


class AuditEntry(BaseModel):
    timestamp: str = ""
    ticket_id: str = ""
    employee: str
    action: str
    response_summary: str
    kb_used: str = ""
