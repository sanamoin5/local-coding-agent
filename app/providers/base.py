from __future__ import annotations

from typing import Any, Protocol


class ModelProvider(Protocol):
    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str,
        tools: list[dict[str, Any]] | None = None,
        schema: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...

    async def list_models(self) -> list[str]: ...
