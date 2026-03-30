from __future__ import annotations

from pathlib import Path

from app.tools.validation import ensure_within_workspace


class FileTools:
    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root

    def list_files(self, relative_dir: str = ".") -> list[str]:
        base = ensure_within_workspace(self.workspace_root, relative_dir)
        files: list[str] = []
        for path in base.rglob("*"):
            if path.is_file():
                files.append(str(path.relative_to(Path(self.workspace_root))))
        return files

    def read_file(self, relative_path: str) -> str:
        path = ensure_within_workspace(self.workspace_root, relative_path)
        return path.read_text(encoding="utf-8")

    def write_file(self, relative_path: str, content: str) -> str:
        path = ensure_within_workspace(self.workspace_root, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return str(path)
