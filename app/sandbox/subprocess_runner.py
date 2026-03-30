from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str


class SubprocessSandbox:
    def __init__(self, workspace_root: str, timeout_seconds: int = 120) -> None:
        self.workspace_root = workspace_root
        self.timeout_seconds = timeout_seconds
        self.allowed_command_prefixes = [
            ["python", "-m", "pytest"],
            ["pytest"],
            ["ruff", "check"],
            ["ruff", "format", "--check"],
            ["mypy"],
            ["npm", "test"],
            ["npm", "run", "build"],
        ]

    def run(self, command: str) -> CommandResult:
        parts = shlex.split(command)
        if not parts:
            raise ValueError("Command cannot be empty")
        if not self._is_allowed(parts):
            raise PermissionError(f"Command not allowed by policy: {command}")

        completed = subprocess.run(
            parts,
            cwd=self.workspace_root,
            timeout=self.timeout_seconds,
            capture_output=True,
            text=True,
            check=False,
        )
        return CommandResult(
            command=command,
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    def _is_allowed(self, parts: list[str]) -> bool:
        for prefix in self.allowed_command_prefixes:
            if parts[: len(prefix)] == prefix:
                return True
        return False
