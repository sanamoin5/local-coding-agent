from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from app.models.run import PersistedRun, RunState, RunStepRecord
from app.models.tool_call import ToolCallRecord
from app.storage.db import Database


class RunRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, state: RunState) -> PersistedRun:
        payload = state.model_dump_json()
        with self.db.connect() as conn:
            cursor = conn.execute("INSERT INTO runs(state_json) VALUES(?)", (payload,))
            run_id = cursor.lastrowid
            row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return self._row_to_run(row)

    def get(self, run_id: int) -> PersistedRun | None:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_run(row)

    def update_state(self, run_id: int, state: RunState) -> PersistedRun:
        payload = state.model_dump_json()
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE runs SET state_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (payload, run_id),
            )
            row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return self._row_to_run(row)

    def add_step(
        self,
        run_id: int,
        node: str,
        status_before: str,
        status_after: str,
        tests_passed: bool,
        reviewer_blocked: bool,
    ) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO run_steps(run_id, node, status_before, status_after, tests_passed, reviewer_blocked)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (run_id, node, status_before, status_after, int(tests_passed), int(reviewer_blocked)),
            )

    def list_steps(self, run_id: int) -> list[RunStepRecord]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM run_steps WHERE run_id = ? ORDER BY id ASC",
                (run_id,),
            ).fetchall()
        return [
            RunStepRecord(
                id=row["id"],
                run_id=row["run_id"],
                node=row["node"],
                status_before=row["status_before"],
                status_after=row["status_after"],
                tests_passed=bool(row["tests_passed"]),
                reviewer_blocked=bool(row["reviewer_blocked"]),
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]

    def add_tool_call(
        self,
        run_id: int,
        action: str,
        args: dict[str, Any],
        ok: bool,
        output: Any,
        error: str | None,
    ) -> ToolCallRecord:
        args_json = json.dumps(args)
        output_json = json.dumps(output)
        with self.db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tool_calls(run_id, action, args_json, ok, output_json, error)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (run_id, action, args_json, int(ok), output_json, error),
            )
            row = conn.execute("SELECT * FROM tool_calls WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return self._row_to_tool_call(row)

    def list_tool_calls(self, run_id: int) -> list[ToolCallRecord]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM tool_calls WHERE run_id = ? ORDER BY id ASC",
                (run_id,),
            ).fetchall()
        return [self._row_to_tool_call(row) for row in rows]

    def _row_to_run(self, row) -> PersistedRun:
        state_data = json.loads(row["state_json"])
        return PersistedRun(
            id=row["id"],
            state=RunState.model_validate(state_data),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def _row_to_tool_call(self, row) -> ToolCallRecord:
        return ToolCallRecord(
            id=row["id"],
            run_id=row["run_id"],
            action=row["action"],
            args_json=row["args_json"],
            ok=bool(row["ok"]),
            output_json=row["output_json"],
            error=row["error"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
