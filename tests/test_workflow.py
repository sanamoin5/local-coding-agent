from app.models.run import RunState
from app.workflows.coding_graph import CodingWorkflow


def test_workflow_fails_after_max_iterations():
    workflow = CodingWorkflow()
    state = RunState(task="x", repo_path=".", status="fixing", iteration_count=0, max_iterations=1)

    updated = workflow.advance(state, tests_passed=False, reviewer_blocked=True)

    assert updated.status == "failed"
    assert updated.iteration_count == 1
