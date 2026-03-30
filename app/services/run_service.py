from __future__ import annotations

from app.models.run import RunState
from app.workflows.coding_graph import CodingWorkflow


class RunService:
    def __init__(self) -> None:
        self.workflow = CodingWorkflow()

    def initialize_run(self, task: str, repo_path: str) -> RunState:
        return RunState(task=task, repo_path=repo_path)

    def tick(self, state: RunState, tests_passed: bool = True, reviewer_blocked: bool = False) -> RunState:
        return self.workflow.advance(state, tests_passed=tests_passed, reviewer_blocked=reviewer_blocked)
