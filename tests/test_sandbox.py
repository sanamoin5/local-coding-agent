import pytest

from app.sandbox.subprocess_runner import SubprocessSandbox


def test_allows_pytest_prefix(tmp_path):
    sandbox = SubprocessSandbox(str(tmp_path))
    result = sandbox.run("pytest -q")
    assert result.command == "pytest -q"


def test_rejects_unsafe_command(tmp_path):
    sandbox = SubprocessSandbox(str(tmp_path))
    with pytest.raises(PermissionError):
        sandbox.run("python -c 'import os; print(os.listdir())'")
