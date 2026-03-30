from __future__ import annotations

from pathlib import Path

from app.models.run import PersistedRun, RunState, RunStepRecord
from app.models.tool_call import ActionRequest, ActionResult, ToolCallRecord
from app.sandbox.subprocess_runner import SubprocessSandbox
from app.storage.db import Database
from app.storage.repositories.run_repository import RunRepository
from app.tools.file_tools import FileTools
from app.workflows.coding_graph import CodingWorkflow


class RunService:
    def __init__(self, repository: RunRepository | None = None) -> None:
        self.workflow = CodingWorkflow()
        self.repository = repository or RunRepository(Database())

    def initialize_run(self, task: str, repo_path: str) -> PersistedRun:
        state = RunState(task=task, repo_path=repo_path)
        return self.repository.create(state)

    def get_run(self, run_id: int) -> PersistedRun | None:
        return self.repository.get(run_id)

    def list_steps(self, run_id: int) -> list[RunStepRecord]:
        return self.repository.list_steps(run_id)

    def list_tool_calls(self, run_id: int) -> list[ToolCallRecord]:
        return self.repository.list_tool_calls(run_id)

    def tick(self, run_id: int, tests_passed: bool = True, reviewer_blocked: bool = False) -> PersistedRun:
        run = self.repository.get(run_id)
        if run is None:
            raise ValueError(f"Run not found: {run_id}")

        status_before = run.state.status
        node = self.workflow.next_node(run.state)
        updated = self.workflow.advance(run.state, tests_passed=tests_passed, reviewer_blocked=reviewer_blocked)
        self.repository.add_step(
            run_id=run_id,
            node=node,
            status_before=status_before,
            status_after=updated.status,
            tests_passed=tests_passed,
            reviewer_blocked=reviewer_blocked,
        )
        return self.repository.update_state(run_id=run_id, state=updated)

    def execute_action(self, run_id: int, request: ActionRequest) -> ActionResult:
        run = self.repository.get(run_id)
        if run is None:
            raise ValueError(f"Run not found: {run_id}")

        workspace = Path(run.state.repo_path)
        if not workspace.exists() or not workspace.is_dir():
            raise ValueError(f"Invalid repo_path for run {run_id}: {run.state.repo_path}")

        file_tools = FileTools(run.state.repo_path)
        sandbox = SubprocessSandbox(run.state.repo_path)

        try:
            if request.action == "list_files":
                output = file_tools.list_files(request.args.get("relative_dir", "."))
            elif request.action == "read_file":
                output = file_tools.read_file(request.args["relative_path"])
            elif request.action == "write_file":
                output = file_tools.write_file(
                    request.args["relative_path"],
                    request.args["content"],
                )
            elif request.action == "run_command":
                result = sandbox.run(request.args["command"])
                output = {
                    "command": result.command,
                    "exit_code": result.exit_code,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            else:
                raise ValueError(f"Unsupported action: {request.action}")

            self.repository.add_tool_call(
                run_id=run_id,
                action=request.action,
                args=request.args,
                ok=True,
                output=output,
                error=None,
            )
            return ActionResult(ok=True, output=output)
        except Exception as exc:  # noqa: BLE001
            self.repository.add_tool_call(
                run_id=run_id,
                action=request.action,
                args=request.args,
                ok=False,
                output=None,
                error=str(exc),
            )
            return ActionResult(ok=False, error=str(exc))
