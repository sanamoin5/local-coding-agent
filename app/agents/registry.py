from __future__ import annotations

from app.models.agent import AgentDefinition

DEFAULT_AGENTS = [
    AgentDefinition(
        id="planner",
        name="Planner",
        description="Turns task into implementation plan",
        model="qwen2.5-coder:7b",
        system_prompt="Create a concrete implementation plan with acceptance criteria.",
        allowed_tools=["list_files", "read_file"],
    ),
    AgentDefinition(
        id="coder",
        name="Coder",
        description="Writes implementation code",
        model="qwen2.5-coder:7b",
        system_prompt="Implement only the current step. Keep changes scoped.",
        allowed_tools=["read_file", "write_file", "run_command"],
    ),
    AgentDefinition(
        id="reviewer",
        name="Reviewer",
        description="Reviews correctness and quality",
        model="qwen2.5-coder:7b",
        system_prompt="Return findings with severity and recommendation.",
        allowed_tools=["read_file"],
    ),
    AgentDefinition(
        id="tester",
        name="Tester",
        description="Runs tests and validation commands",
        model="qwen2.5-coder:7b",
        system_prompt="Execute tests and summarize outcomes.",
        allowed_tools=["run_command"],
    ),
]
