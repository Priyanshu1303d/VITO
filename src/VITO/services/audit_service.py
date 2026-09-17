import json
from pathlib import Path
from VITO.models.ticket import AuditEntry

_DATA = Path(__file__).resolve().parents[3] / "data"
_FILE = _DATA / "audit_log.json"


def _load() -> list[dict]:
    if not _FILE.exists():
        return []
    return json.loads(_FILE.read_text())


def write_entry(entry: AuditEntry):
    log = _load()
    log.append(entry.model_dump())
    _FILE.write_text(json.dumps(log, indent=2))


def get_audit_log() -> list[dict]:
    return _load()


def clear_log():
    _FILE.write_text("[]")
