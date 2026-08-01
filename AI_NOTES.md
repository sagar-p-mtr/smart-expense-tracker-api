# AI Usage Report

## AI-Assisted Sections

- Generated the initial FastAPI app structure across `main.py`, `routes.py`, `models.py`, `storage.py`, and `utils.py`.
- Proposed request/response model definitions and input validation rules.
- Drafted endpoint handlers for CRUD and total-calculation behavior.
- Drafted pytest coverage scenarios and API documentation examples.

## Manually Reviewed and Modified

- Reviewed storage logic to ensure JSON file creation and safe writes (temp file + replace).
- Confirmed empty and corrupted JSON handling returns safe defaults rather than failing requests.
- Adjusted category filtering behavior to be case insensitive.
- Verified status codes: `201`, `200`, `204`, and `404` match assignment requirements.
- Checked project structure and command instructions for accuracy.

## Validation Performed

- Ran `pytest` to verify endpoint behavior and validation.
- Checked that import paths resolve correctly from the project root.
- Confirmed FastAPI docs endpoints are enabled by default (`/docs`, `/redoc`).
- Verified the app starts using `uvicorn src.main:app --reload`.

## AI Suggestion Not Used

- Suggested replacing local JSON storage with SQLite for stronger data integrity.
- Rejected because the assignment explicitly requires no database and local `expenses.json` storage.
