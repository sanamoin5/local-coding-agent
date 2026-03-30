from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.run import PersistedRun, RunStepRecord
from app.services.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"])
service = RunService()


class CreateRunRequest(BaseModel):
    task: str
    repo_path: str


class TickRunRequest(BaseModel):
    tests_passed: bool = True
    reviewer_blocked: bool = False


@router.post("", response_model=PersistedRun)
def create_run(payload: CreateRunRequest) -> PersistedRun:
    return service.initialize_run(task=payload.task, repo_path=payload.repo_path)


@router.get("/{run_id}", response_model=PersistedRun)
def get_run(run_id: int) -> PersistedRun:
    run = service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/tick", response_model=PersistedRun)
def tick_run(run_id: int, payload: TickRunRequest) -> PersistedRun:
    try:
        return service.tick(
            run_id=run_id,
            tests_passed=payload.tests_passed,
            reviewer_blocked=payload.reviewer_blocked,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{run_id}/steps", response_model=list[RunStepRecord])
def list_steps(run_id: int) -> list[RunStepRecord]:
    run = service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return service.list_steps(run_id)
