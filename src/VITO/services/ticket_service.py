import json
from pathlib import Path
from datetime import datetime
from VITO.models.ticket import Ticket

_DATA = Path(__file__).resolve().parents[3] / "data"
_FILE = _DATA / "ticket_queue.json"


def _load() -> list[dict]:
    return json.loads(_FILE.read_text())


def _save(tickets: list[dict]):
    _FILE.write_text(json.dumps(tickets, indent=2))


def get_next_id() -> str:
    nums = [int(t["id"].split("-")[1]) for t in _load()]
    return f"TK-{max(nums) + 1}"


def create_ticket(ticket: Ticket) -> dict:
    tickets = _load()
    d = ticket.model_dump()
    tickets.append(d)
    _save(tickets)
    return d


def close_ticket(ticket_id: str) -> dict | None:
    tickets = _load()
    for t in tickets:
        if t["id"] == ticket_id and not t.get("closed"):
            t["closed"] = True
            t["closed_at"] = datetime.now().isoformat()
            _save(tickets)
            return t
    return None


def get_tickets() -> list[dict]:
    return _load()

