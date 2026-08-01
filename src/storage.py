from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from src.models import Expense


class ExpenseStorage:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read_raw_data(self) -> list[dict[str, Any]]:
        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            self._ensure_file_exists()
            return []
        except OSError:
            return []

        if not content:
            return []

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return []

        if not isinstance(parsed, list):
            return []

        return [item for item in parsed if isinstance(item, dict)]

    def read_expenses(self) -> list[Expense]:
        with self._lock:
            raw_items = self._read_raw_data()

        expenses: list[Expense] = []
        for item in raw_items:
            try:
                expenses.append(Expense.model_validate(item))
            except ValidationError:
                # Skip invalid records to keep the API resilient.
                continue
        return expenses

    def write_expenses(self, expenses: list[Expense]) -> None:
        payload = [expense.model_dump(mode="json") for expense in expenses]
        temp_file = self.file_path.with_suffix(".tmp")

        with self._lock:
            try:
                with temp_file.open("w", encoding="utf-8") as handle:
                    json.dump(payload, handle, indent=2)
                os.replace(temp_file, self.file_path)
            finally:
                if temp_file.exists():
                    temp_file.unlink(missing_ok=True)

    def add_expense(self, expense: Expense) -> Expense:
        expenses = self.read_expenses()
        expenses.append(expense)
        self.write_expenses(expenses)
        return expense

    def delete_expense(self, expense_id: UUID) -> bool:
        expenses = self.read_expenses()
        updated_expenses = [expense for expense in expenses if expense.id != expense_id]
        if len(updated_expenses) == len(expenses):
            return False

        self.write_expenses(updated_expenses)
        return True
