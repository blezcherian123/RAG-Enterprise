# Backend

This backend is built with FastAPI and PostgreSQL using a tenant-aware architecture.

## Features
- FastAPI application structure
- PostgreSQL database configured from `.env`
- Multi-tenant support via `X-Tenant-ID` request header
- Clean separation of routers, services, schemas, and database models
- JWT login support using tenant-aware authentication

## Setup
1. Create and activate your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env` with your database and secret key.

## Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Tenant flow
1. Create a tenant:
   - `POST /api/v1/tenants`
2. Use the returned tenant ID in the `X-Tenant-ID` header for user and auth requests.

## Example headers
```http
X-Tenant-ID: <tenant-id>
Content-Type: application/json
```
