# Password Strength Checker

[![Tests](https://github.com/yourpunk/password_checker/actions/workflows/tests.yml/badge.svg)](https://github.com/yourpunk/password_checker/actions/workflows/tests.yml)

Analyzes password strength in real time with a 0-100 score, detailed criteria breakdown, and actionable suggestions.

## Features

- Live analysis as you type (no need to click a button)
- 0-100 strength score across 5 weighted criteria:
  - Length
  - Character variety (lowercase, uppercase, digits, special characters)
  - Repeated characters
  - Predictable sequences (123, abc, qwerty)
  - Common password patterns
- Specific, actionable suggestions for improvement
- No password is ever stored or logged

## Tech Stack

- **Backend:** FastAPI, Pydantic
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Testing:** Pytest (20+ tests covering scoring logic and API)
- **CI/CD:** GitHub Actions
- **Deployment:** Render

## Installation

```bash
git clone https://github.com/yourpunk/password_checker.git
cd password_checker

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r backend/requirements.txt
```

## Running Locally

```bash
uvicorn backend.main:app --reload
```

Visit `http://localhost:8000`

## Testing

```bash
pytest -v
```

## API

### `POST /api/check`

```json
{
  "password": "MySecureP@ss123"
}
```

Returns:

```json
{
  "score": 78,
  "category": "good",
  "criteria": [
    {
      "name": "length",
      "passed": true,
      "points": 16,
      "max_points": 30,
      "message": "Длина пароля: 15 символов"
    }
  ],
  "suggestions": ["..."]
}
```

### `GET /health`

Health check endpoint for deployment monitoring.

## Notes

This tool checks password **structure** only (length, character variety,
patterns). It does **not** check against known breached password databases —
that would require an external dataset/API and is out of scope for this project.
