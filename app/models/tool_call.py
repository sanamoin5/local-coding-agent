from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ActionRequest(BaseModel):
    action: Literal["list_files", "read_file", "write_file", "run_command"]
    args: dict[str, Any] = Field(default_factory=dict)


class ActionResult(BaseModel):
    ok: bool
    output: Any = None
    error: str | None = None


class ToolCallRecord(BaseModel):
    id: int
    run_id: int
    action: str
    args_json: str
    ok: bool
    output_json: str
    error: str | None
    created_at: datetime
