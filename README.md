# local-coding-agent

A **local-first coding agent platform** scaffold with four layers:

1. **Model runtime** (`app/providers`) with an Ollama provider abstraction.
2. **Agent orchestration** (`app/workflows`, `app/services`) with a fixed v1 coding workflow.
3. **Sandbox executor** (`app/sandbox`, `app/tools`) for controlled file and command operations.
4. **UI + persistence ready backend** (`app/api`, `app/storage`, typed models in `app/models`) to support agents, tasks, runs, logs, and artifacts.

## Implemented architecture

- `ModelProvider` protocol + `OllamaProvider` for local model chat + model listing.
- Pydantic contracts for `AgentDefinition`, `AgentAction`, `RunState`, `PlanStep`, `ReviewFinding`, `TestResult`, `PersistedRun`, and `RunStepRecord`.
- Fixed workflow engine (`CodingWorkflow`) for planner/coder/reviewer/tester/verifier transitions with max-iteration failure guard.
- Subprocess sandbox with command allowlist and timeout enforcement.
- Workspace-safe file tools with strict path traversal protection.
- SQLite-backed run persistence for run state, run steps, and tool calls.
- Action broker in `RunService.execute_action` that validates run workspace and executes controlled file/command tools.
- FastAPI endpoints:
  - `POST /runs` create run
  - `GET /runs/{run_id}` get current run state
  - `POST /runs/{run_id}/tick` advance workflow state with gate outcomes
  - `GET /runs/{run_id}/steps` list execution timeline
  - `POST /runs/{run_id}/actions` execute a validated tool action (`list_files`, `read_file`, `write_file`, `run_command`)
  - `GET /runs/{run_id}/tool-calls` list tool call audit trail
- Unit tests for path validation, workflow stop conditions, persistence, service action logging, and sandbox policy enforcement.

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
