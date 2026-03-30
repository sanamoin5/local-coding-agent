from __future__ import annotations

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings for local-first agent execution."""

    workspace_root: str = Field(default="./workspace")
    default_model: str = Field(default="qwen2.5-coder:7b")
    max_command_seconds: int = Field(default=120)
    allow_network: bool = Field(default=False)


settings = Settings()
