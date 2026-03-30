# local-coding-agent

A **local-first coding agent platform** scaffold with four layers:

1. **Model runtime** (`app/providers`) with an Ollama provider abstraction.
2. **Agent orchestration** (`app/workflows`, `app/services`) with a fixed v1 coding workflow.
3. **Sandbox executor** (`app/sandbox`, `app/tools`) for controlled file and command operations.
4. **UI + persistence ready backend** (`app/api`, typed models in `app/models`) to support agents, tasks, runs, logs, and artifacts.

## Implemented architecture

- `ModelProvider` protocol + `OllamaProvider` for local model chat + model listing.
- Pydantic contracts for `AgentDefinition`, `AgentAction`, `RunState`, `PlanStep`, `ReviewFinding`, and `TestResult`.
- Fixed workflow engine (`CodingWorkflow`) for planner/coder/reviewer/tester/verifier transitions.
- Subprocess sandbox with command allowlist and timeout enforcement.
- Workspace-safe file tools with path traversal protection.
- FastAPI endpoint to create runs.
- Unit tests for workspace path validation.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.api.main:app --reload
```

Run tests:

```bash
pytest
```
