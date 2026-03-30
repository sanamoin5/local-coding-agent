from __future__ import annotations

from app.models.run import RunState


class CodingWorkflow:
    """Fixed v1 workflow: planner -> coder -> reviewer -> tester -> verifier."""

    def next_node(self, state: RunState) -> str:
        if state.status == "planning":
            return "planner"
        if state.status == "coding":
            return "coder"
        if state.status == "reviewing":
            return "reviewer"
        if state.status == "testing":
            return "tester"
        if state.status == "fixing":
            return "fixer"
        if state.status == "verifying":
            return "verifier"
        return "done"

    def advance(self, state: RunState, tests_passed: bool, reviewer_blocked: bool) -> RunState:
        if state.status in {"done", "failed"}:
            return state

        if state.status == "planning":
            state.status = "coding"
        elif state.status == "coding":
            state.status = "reviewing"
        elif state.status == "reviewing":
            state.status = "fixing" if reviewer_blocked else "testing"
        elif state.status == "testing":
            state.status = "fixing" if not tests_passed else "verifying"
        elif state.status == "fixing":
            state.status = "coding"
            state.iteration_count += 1
        elif state.status == "verifying":
            state.status = "done" if tests_passed and not reviewer_blocked else "failed"

        if state.iteration_count >= state.max_iterations and state.status not in {"done", "failed"}:
            state.status = "failed"

        return state
