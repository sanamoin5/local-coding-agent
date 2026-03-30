from app.models.run import RunState
from app.storage.db import Database
from app.storage.repositories.run_repository import RunRepository


def test_run_repository_persists_run_and_steps(tmp_path):
    db = Database(str(tmp_path / "runs.db"))
    repo = RunRepository(db)

    created = repo.create(RunState(task="build", repo_path="/repo"))
    repo.add_step(
        run_id=created.id,
        node="planner",
        status_before="planning",
        status_after="coding",
        tests_passed=True,
        reviewer_blocked=False,
    )

    loaded = repo.get(created.id)
    steps = repo.list_steps(created.id)

    assert loaded is not None
    assert loaded.state.task == "build"
    assert len(steps) == 1
    assert steps[0].node == "planner"
