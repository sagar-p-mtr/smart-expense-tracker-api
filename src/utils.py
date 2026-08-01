from __future__ import annotations

from uuid import uuid4

from src.models import Expense, ExpenseCreate


def create_expense(payload: ExpenseCreate) -> Expense:
    return Expense(id=uuid4(), **payload.model_dump())


def filter_expenses_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    normalized = category.strip().lower()
    return [expense for expense in expenses if expense.category.strip().lower() == normalized]


def calculate_total(expenses: list[Expense]) -> float:
    return round(sum(expense.amount for expense in expenses), 2)
