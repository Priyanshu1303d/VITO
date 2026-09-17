from VITO.graph.state import AgentState
from VITO.services import llm_service, kb_service
from VITO.services import ticket_service, audit_service, validation_service
from VITO.models.employee import ClassifyResult, DecideResult
from VITO.models.ticket import Ticket, AuditEntry
from VITO.prompts.system_prompts import CLASSIFY, DECIDE
from datetime import datetime


def classify_issue(state: AgentState) -> dict:
    r = llm_service.call_llm_structured(CLASSIFY.format(message=state["message"]), ClassifyResult)
    return {"category": r.category, "missing_fields": r.missing_fields}

def retrieve_policy(state: AgentState) -> dict:
    return {"kb_matches": kb_service.find_policies(state.get("category", ""))}

def decide_action(state: AgentState) -> dict:
    p = DECIDE.format(employee=state["employee"], message=state["message"],
                      category=state.get("category", ""), kb_matches=state.get("kb_matches", []))
    r = llm_service.call_llm_structured(p, DecideResult)
    return {"action": r.action, "response_text": r.response_text, "escalation_reason": r.escalation_reason}

def ask_followup(state: AgentState) -> dict:
    return {}
def resolve_request(state: AgentState) -> dict:
    return {}
def escalate_request(state: AgentState) -> dict:
    return {"action": "escalate"}

def validate_output(state: AgentState) -> dict:
    txt = state.get("response_text", "")
    if validation_service.check_prompt_injection(txt):
        return {"action": "escalate", "response_text": "Request escalated for manual review."}
    return {"response_text": validation_service.mask_pii(txt)}

def create_ticket(state: AgentState) -> dict:
    kb = ",".join(p["id"] for p in state.get("kb_matches", []))
    t = Ticket(id=ticket_service.get_next_id(), employee=state["employee"],
        issue=state["message"][:100], status=state.get("action", "ticket"),
        category=state.get("category", ""), kb_source=kb,
        resolution=state.get("response_text", ""), closed=state.get("action") != "ticket")
    return {"ticket": ticket_service.create_ticket(t)}

def write_audit(state: AgentState) -> dict:
    kb = ",".join(p["id"] for p in state.get("kb_matches", []))
    e = AuditEntry(timestamp=datetime.now().isoformat(),
        ticket_id=state.get("ticket", {}).get("id", ""), employee=state["employee"],
        action=state.get("action", ""), response_summary=state.get("response_text", "")[:200],
        kb_used=kb)
    audit_service.write_entry(e)
    return {}
