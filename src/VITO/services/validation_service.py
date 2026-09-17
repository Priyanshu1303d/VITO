import re

_INJECTION_KEYWORDS = [
    "ignore previous", "ignore all instructions",
    "system prompt", "override instructions",
    "disregard", "forget your instructions",
    "you are now", "act as", "new instructions:",
]

_PII_PATTERNS = [
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
    (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
]


def check_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in _INJECTION_KEYWORDS)


def mask_pii(text: str) -> str:
    for pattern, replacement in _PII_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text
