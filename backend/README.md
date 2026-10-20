# Company RAG API

FastAPI, SQLAlchemy, PostgreSQL, and tenant scoped authentication for the Homeegram workspace.

## Configure

Create `backend/.env` (or inject these values through the deployment environment):

```dotenv
DATABASE_URL=postgresql+psycopg2://app_user:replace-me@localhost:5432/company_rag
SECRET_KEY=replace-with-at-least-32-random-bytes
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=["http://localhost:5173"]
ENVIRONMENT=development
ENABLE_API_DOCS=true
```

Use a managed PostgreSQL database and a randomly generated secret in production. Set `ALLOWED_ORIGINS` to the exact HTTPS frontend origins, set `ENVIRONMENT=production`, and set `ENABLE_API_DOCS=false`. Production settings are rejected if they expose interactive docs, use HTTP CORS origins, or have a short signing key. A short key only emits a warning in local development.

## Database setup and run

Schema changes are managed through Alembic; the API does not create or modify tables during startup.

```bash
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
alembic upgrade head
python -m scripts.create_admin
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The optional `requirements-rag.txt` contains retrieval and LLM packages for a future server-side RAG service. The current API does not import these packages.

Apply migrations as a deployment step before starting new application instances. The initial migration creates the `default` workspace. Create its first administrator from a trusted shell; the script prompts for credentials and never exposes administrator provisioning over the public API.

## Authentication and authorization

- Login and signup issue signed, expiring JWT bearer tokens. Tokens include issuer, audience, issue time, subject, and tenant claims.
- `POST /api/v1/auth/logout` revokes the current token; authenticated requests reject revoked tokens.
- User identity, active status, tenant membership, and role are loaded from PostgreSQL on each authenticated request. A client supplied tenant header is never treated as proof of membership.
- Public signup creates only an `employee` in the pre-provisioned default workspace. It cannot create tenants or assign privileged roles.
- Administrators manage users within their own tenant. HR and administrators can list users. Tenant detail reads are scoped to the authenticated user's own tenant.
- Roles are `admin`, `hr`, `employee`, `finance`, and `c_level`; a database check constraint limits stored values.
- The dashboard currently exposes all four assistant profiles for exploration. Role-based assistant authorization is intentionally deferred; enforce it on the server when a chat API is added.
- `GET /api/v1/models` and the legacy `GET /v1/models` both return all four assistant identifiers for existing clients.

Send `Authorization: Bearer <access_token>` to authenticated routes. Login accepts either a tenant ID or tenant name. Self-service signup is limited to `tenant_name: "default"`.

## Operational endpoints

- `GET /health/live` reports that the process is running.
- `GET /health/ready` checks database connectivity and returns HTTP 503 when the database is unavailable.
- `/health` remains a liveness alias for existing deployments.

The dashboard currently provides local demo replies only. This repository does not yet implement a conversation, retrieval, or LLM API; local replies are not grounded in company data.
