from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AgentDefinition(BaseModel):
    id: str
    name: str
    description: str
    model: str
    system_prompt: str
    allowed_tools: list[str] = Field(default_factory=list)
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    max_iterations: int = 3
    temperature: float = 0.2


class AgentAction(BaseModel):
    action: str
    args: dict[str, Any] = Field(default_factory=dict)
