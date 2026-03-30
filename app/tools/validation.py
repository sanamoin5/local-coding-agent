from __future__ import annotations

from pathlib import Path


class ValidationError(Exception):
    pass


def ensure_within_workspace(workspace_root: str, relative_path: str) -> Path:
    root = Path(workspace_root).resolve()
    destination = (root / relative_path).resolve()
    if not str(destination).startswith(str(root)):
        raise ValidationError(f"Path escapes workspace: {relative_path}")
    return destination
