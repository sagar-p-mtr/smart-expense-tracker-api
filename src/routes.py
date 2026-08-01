from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status

from src.models import Expense, ExpenseCreate
from src.storage import ExpenseStorage
from src.utils import calculate_total, create_expense, filter_expenses_by_category

router = APIRouter()


def get_storage(request: Request) -> ExpenseStorage:
    return request.app.state.storage


@router.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def add_expense(
    payload: ExpenseCreate,
    storage: ExpenseStorage = Depends(get_storage),
) -> Expense:
    expense = create_expense(payload)
    return storage.add_expense(expense)


@router.get("/expenses", response_model=list[Expense])
def get_expenses(
    category: str | None = Query(default=None),
    storage: ExpenseStorage = Depends(get_storage),
) -> list[Expense]:
    expenses = storage.read_expenses()
    if category is None:
        return expenses
    return filter_expenses_by_category(expenses, category)


@router.get("/expenses/total")
def get_total_expenses(
    category: str | None = Query(default=None),
    storage: ExpenseStorage = Depends(get_storage),
) -> dict[str, str | float]:
    expenses = storage.read_expenses()
    if category is None:
        return {"total": calculate_total(expenses)}

    filtered_expenses = filter_expenses_by_category(expenses, category)
    return {
        "category": category,
        "total": calculate_total(filtered_expenses),
    }


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: UUID,
    storage: ExpenseStorage = Depends(get_storage),
) -> Response:
    deleted = storage.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
