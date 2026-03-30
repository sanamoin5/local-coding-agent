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
        self.allowed_commands = {
            "python",
            "pytest",
            "ruff",
            "mypy",
            "npm",
        }

    def run(self, command: str) -> CommandResult:
        parts = shlex.split(command)
        if not parts:
            raise ValueError("Command cannot be empty")
        if parts[0] not in self.allowed_commands:
            raise PermissionError(f"Command not allowed: {parts[0]}")

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
