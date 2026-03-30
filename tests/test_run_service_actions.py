from app.models.tool_call import ActionRequest
from app.services.run_service import RunService
from app.storage.db import Database
from app.storage.repositories.run_repository import RunRepository


def test_execute_action_logs_tool_call(tmp_path):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    db = Database(str(tmp_path / "runs.db"))
    service = RunService(repository=RunRepository(db))

    run = service.initialize_run(task="t", repo_path=str(repo_path))
    result = service.execute_action(
        run.id,
        ActionRequest(action="write_file", args={"relative_path": "a.txt", "content": "hello"}),
    )

    calls = service.list_tool_calls(run.id)
    assert result.ok is True
    assert len(calls) == 1
    assert calls[0].action == "write_file"
