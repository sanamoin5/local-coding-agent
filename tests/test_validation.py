from pathlib import Path

import pytest

from app.tools.validation import ValidationError, ensure_within_workspace


def test_allows_safe_path(tmp_path):
    resolved = ensure_within_workspace(str(tmp_path), "src/main.py")
    assert str(resolved).startswith(str(tmp_path))


def test_rejects_escape(tmp_path):
    with pytest.raises(ValidationError):
        ensure_within_workspace(str(tmp_path), "../etc/passwd")


def test_rejects_sibling_prefix_escape(tmp_path):
    sibling = tmp_path.parent / f"{tmp_path.name}_sibling"
    sibling.mkdir()
    relative = str(Path("..") / sibling.name / "secret.txt")
    with pytest.raises(ValidationError):
        ensure_within_workspace(str(tmp_path), relative)
