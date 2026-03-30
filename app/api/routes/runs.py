from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.models.run import RunState
from app.services.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"])
service = RunService()


class CreateRunRequest(BaseModel):
    task: str
    repo_path: str


@router.post("", response_model=RunState)
def create_run(payload: CreateRunRequest) -> RunState:
    return service.initialize_run(task=payload.task, repo_path=payload.repo_path)
