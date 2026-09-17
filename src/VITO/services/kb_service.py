import json
from pathlib import Path

_DATA = Path(__file__).resolve().parents[3] / "data"
_policies = json.loads((_DATA / "kb_policies.json").read_text())


def find_policies(category: str) -> list[dict]:
    if not category or category == "unclear":
        return []
    return [p for p in _policies if p["category"] == category]


def get_all_policies() -> list[dict]:
    return list(_policies)
