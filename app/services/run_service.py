from __future__ import annotations

from app.models.run import PersistedRun, RunState, RunStepRecord
from app.storage.db import Database
from app.storage.repositories.run_repository import RunRepository
from app.workflows.coding_graph import CodingWorkflow


class RunService:
    def __init__(self) -> None:
        self.workflow = CodingWorkflow()
        self.repository = RunRepository(Database())

    def initialize_run(self, task: str, repo_path: str) -> PersistedRun:
        state = RunState(task=task, repo_path=repo_path)
        return self.repository.create(state)

    def get_run(self, run_id: int) -> PersistedRun | None:
        return self.repository.get(run_id)

    def list_steps(self, run_id: int) -> list[RunStepRecord]:
        return self.repository.list_steps(run_id)

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
