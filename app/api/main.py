from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.runs import router as runs_router

app = FastAPI(title="Local Coding Agent Platform")
app.include_router(runs_router)
