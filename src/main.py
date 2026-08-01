from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI

from src.routes import router
from src.storage import ExpenseStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    storage_path = Path(__file__).resolve().parent / "expenses.json"
    app.state.storage = ExpenseStorage(storage_path)
    yield


app = FastAPI(
    title="Smart Expense Tracker API",
    description="A JSON-file-backed API for tracking personal expenses.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
