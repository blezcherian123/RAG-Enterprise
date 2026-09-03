from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.auth import LoginRequest, SignupRequest
from app.schemas.tenant import TenantCreate
from app.schemas.user import TokenWithUser, UserCreate
from app.security import create_access_token
from app.services.tenant import create_tenant, get_tenant_by_id, get_tenant_by_name
from app.services.user import authenticate_user, create_user, get_user_by_email

router = APIRouter()

DEFAULT_TENANT = "default"


def resolve_tenant_id(db: Session, tenant_id: str | None = None, tenant_name: str | None = None) -> str:
    if tenant_id:
        tenant = get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        return tenant_id

    name = tenant_name or DEFAULT_TENANT
    tenant = get_tenant_by_name(db, name)
    if tenant:
        return tenant.id

    new_tenant = create_tenant(db, TenantCreate(name=name))
    return new_tenant.id


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db_session)):
    tenant_id = resolve_tenant_id(db, body.tenant_id, body.tenant_name)
    user = authenticate_user(db, tenant_id, body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=TokenWithUser, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, db: Session = Depends(get_db_session)):
    tenant_id = resolve_tenant_id(db, tenant_name=body.tenant_name)

    if get_user_by_email(db, tenant_id, body.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists for this tenant")

    user = create_user(db, tenant_id, UserCreate(email=body.email, full_name=body.full_name, password=body.password))
    token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": token, "token_type": "bearer", "user": user}
