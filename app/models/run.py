from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    id: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)


class ReviewFinding(BaseModel):
    severity: Literal["low", "medium", "high", "blocker"]
    file: str | None = None
    issue: str
    recommendation: str


class TestResult(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    passed: bool


class RunState(BaseModel):
    task: str
    repo_path: str
    plan: list[PlanStep] = Field(default_factory=list)
    current_step: str | None = None
    file_changes: list[str] = Field(default_factory=list)
    test_results: list[TestResult] = Field(default_factory=list)
    review_findings: list[ReviewFinding] = Field(default_factory=list)
    status: Literal[
        "planning",
        "coding",
        "reviewing",
        "testing",
        "fixing",
        "verifying",
        "done",
        "failed",
    ] = "planning"
    iteration_count: int = 0
    max_iterations: int = 5


class PersistedRun(BaseModel):
    id: int
    state: RunState
    created_at: datetime
    updated_at: datetime


class RunStepRecord(BaseModel):
    id: int
    run_id: int
    node: str
    status_before: str
    status_after: str
    tests_passed: bool
    reviewer_blocked: bool
    created_at: datetime
