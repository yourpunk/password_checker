# 🔒 Password Strength Checker

[![Tests](https://github.com/yourpunk/password_checker/actions/workflows/tests.yml/badge.svg)](https://github.com/yourpunk/password_checker/actions/workflows/tests.yml)

Analyzes password strength in real time with a 0-100 score, detailed criteria breakdown, and actionable suggestions. *Live demo*: [password-checker.onrender.com](https://password-checker-1w3s.onrender.com)

> **Note:** This runs on Render's free tier, which spins down after inactivity. The first request after idle time may take 30-60 seconds to respond.

## Preview

<img width="951" height="417" alt="image" src="https://github.com/user-attachments/assets/0d2d8c73-14db-4af3-8b1a-33e69cc9d62b" />
<br>
<img width="922" height="623" alt="image" src="https://github.com/user-attachments/assets/ec0722bd-0dbf-485a-bd8e-17a2baf59d62" />
<br>
<img width="930" height="686" alt="image" src="https://github.com/user-attachments/assets/07c1cec7-0204-43a5-805d-bf98f80f3ee1" />

## Features

- Live analysis as you type (no need to click a button)
- 0-100 strength score across **5 weighted criteria**:
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

pip install -r requirements.txt
```

## Running Locally

```bash
uvicorn backend.main:app --reload
```

_Visit `http://localhost:8000`_

## Testing

```bash
pytest -v
```

## API Endpoints

|Method	|Endpoint|	Description|
|--------|----------|-------------|
|`POST`	| `/api/check` |	Analyze password strength|
|`GET`	| `/health`	| Service health check|

### Example 

```bash
curl -X POST https://password-checker-1w3s.onrender.com/api/check \
  -H "Content-Type: application/json" \
  -d '{"password": "MySecureP@ss123"}'
```

## Notes

This tool checks password **structure** only (length, character variety,
patterns). It does **not** check against known breached password databases:
that would require an external dataset/API and is out of scope for this project.

## 👤 Author
🦾 Crafted by Aleksandra Kenig (aka [yourpunk](https://github.com/yourpunk)).<br>
💌 Wanna collab or throw some feedback? You know where to find me.
