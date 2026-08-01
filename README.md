# Smart Expense Tracker API

A FastAPI-based REST API that tracks expenses using a local JSON file instead of a database.

## Features

- Add an expense
- View all expenses
- Filter expenses by category (case insensitive)
- Calculate total expenses
- Calculate total expenses by category
- Delete an expense
- Automatic interactive API docs at `/docs` and `/redoc`
- File-based storage with graceful handling of missing, empty, or corrupted JSON

## Tech Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- pytest

## Installation

1. Ensure Python 3.12+ is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn src.main:app --reload
```

## Run Tests

```bash
pytest
```

## API Endpoints

### POST /expenses
Create a new expense.

Request body:

```json
{
  "title": "Lunch",
  "amount": 12.50,
  "category": "Food",
  "date": "2026-07-31"
}
```

Response `201`:

```json
{
  "id": "e7ad27e0-c9f9-4e8b-a282-18f1dfd7505c",
  "title": "Lunch",
  "amount": 12.5,
  "category": "Food",
  "date": "2026-07-31"
}
```

### GET /expenses
Return all expenses.

Response `200`:

```json
[
  {
    "id": "e7ad27e0-c9f9-4e8b-a282-18f1dfd7505c",
    "title": "Lunch",
    "amount": 12.5,
    "category": "Food",
    "date": "2026-07-31"
  }
]
```

### GET /expenses?category=Food
Return expenses filtered by category (case insensitive).

Response `200`:

```json
[
  {
    "id": "e7ad27e0-c9f9-4e8b-a282-18f1dfd7505c",
    "title": "Lunch",
    "amount": 12.5,
    "category": "Food",
    "date": "2026-07-31"
  }
]
```

### GET /expenses/total
Return total amount for all expenses.

Response `200`:

```json
{
  "total": 1234.5
}
```

### GET /expenses/total?category=Food
Return total amount for the provided category.

Response `200`:

```json
{
  "category": "Food",
  "total": 500.0
}
```

### DELETE /expenses/{id}
Delete an expense by UUID.

Response `204`: no content.

If missing, response `404`:

```json
{
  "detail": "Expense not found"
}
```

## Validation Rules

- `amount` must be greater than 0
- `title` cannot be empty
- `category` cannot be empty
- `date` must be a valid ISO date (`YYYY-MM-DD`)

## Folder Structure

```text
expense-tracker-api/
|
|-- README.md
|-- AI_NOTES.md
|-- requirements.txt
|-- src/
|   |-- main.py
|   |-- models.py
|   |-- storage.py
|   |-- routes.py
|   |-- utils.py
|   `-- expenses.json
`-- tests/
    `-- test_api.py
```
