from app.tools.validation import ValidationError, ensure_within_workspace


def test_allows_safe_path(tmp_path):
    resolved = ensure_within_workspace(str(tmp_path), "src/main.py")
    assert str(resolved).startswith(str(tmp_path))


def test_rejects_escape(tmp_path):
    try:
        ensure_within_workspace(str(tmp_path), "../etc/passwd")
    except ValidationError:
        assert True
    else:
        raise AssertionError("Expected ValidationError")
