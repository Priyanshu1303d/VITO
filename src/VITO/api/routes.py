from fastapi import APIRouter, HTTPException
from VITO.api.models import ChatRequest, ChatResponse
from VITO.graph.workflow import app as graph_app
from VITO.services import ticket_service, audit_service
from VITO.models.ticket import AuditEntry
from datetime import datetime

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    state = graph_app.invoke({
        "employee": req.employee, "message": req.message,
        "category": None, "missing_fields": [], "kb_matches": [],
        "action": None, "response_text": None,
        "escalation_reason": None, "ticket": None,
    })
    kb = ",".join(p["id"] for p in state.get("kb_matches", []))
    tid = state.get("ticket", {}).get("id", "") if state.get("ticket") else ""
    return ChatResponse(
        response_text=state.get("response_text", ""),
        action=state.get("action"), category=state.get("category"),
        kb_source=kb, ticket_id=tid,
        escalation_reason=state.get("escalation_reason", ""),
    )


@router.patch("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: str):
    t = ticket_service.close_ticket(ticket_id)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found or already closed")
    audit_service.write_entry(AuditEntry(
        timestamp=datetime.now().isoformat(), ticket_id=ticket_id,
        employee=t.get("employee", ""), action="closed",
        response_summary="Ticket closed manually via dashboard",
        kb_used=t.get("kb_source", "")))
    return t


@router.get("/tickets")
def get_tickets():
    return ticket_service.get_tickets()


@router.get("/audit")
def get_audit():
    return audit_service.get_audit_log()


@router.delete("/audit")
def clear_audit():
    audit_service.clear_log()
    return {"status": "cleared"}

