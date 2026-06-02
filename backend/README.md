# FIM Backend

FastAPI backend for the File Integrity Monitoring research application.

## Stack

- Python FastAPI
- SQLite
- SQLAlchemy
- hashlib for SHA-256 and PBKDF2
- argon2-cffi for Argon2id

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API base path: `/api/v1`.
