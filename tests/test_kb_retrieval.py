from VITO.services.kb_service import find_policies


def test_password_returns_kb01():
    results = find_policies("password")
    assert any(p["id"] == "KB-01" for p in results)


def test_laptop_returns_both_policies():
    results = find_policies("laptop")
    ids = {p["id"] for p in results}
    assert "KB-03" in ids and "ASSET-POLICY" in ids


def test_security_returns_kb09():
    results = find_policies("security_incident")
    assert any(p["id"] == "KB-09" for p in results)


def test_unclear_returns_empty():
    assert find_policies("unclear") == []
    assert find_policies("") == []
