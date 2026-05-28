from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, SignupRequest
from app.schemas.user import Token, TokenUserResponse, UserCreate, UserOut
from app.services.tenant_service import create_tenant, get_tenant_by_id, get_tenant_by_name
from app.services.user_service import authenticate_user, create_user, get_user_by_email
from app.schemas.tenant import TenantCreate

router = APIRouter()

DEFAULT_TENANT_NAME = "default"


def resolve_tenant_id(
    db: Session,
    tenant_id: Optional[str] = None,
    tenant_name: Optional[str] = None,
) -> str:
    if tenant_id:
        tenant = get_tenant_by_id(db, tenant_id=tenant_id)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found",
            )
        return tenant_id

    requested_name = tenant_name or DEFAULT_TENANT_NAME
    tenant = get_tenant_by_name(db, name=requested_name)
    if tenant:
        return tenant.id

    new_tenant = create_tenant(db, TenantCreate(name=requested_name))
    return new_tenant.id


@router.post("/login", response_model=Token)
def login_for_access_token(
    login_request: LoginRequest,
    db: Session = Depends(get_db_session),
):
    tenant_id = resolve_tenant_id(db, tenant_id=login_request.tenant_id, tenant_name=login_request.tenant_name)
    user = authenticate_user(
        db,
        tenant_id=tenant_id,
        email=login_request.email,
        password=login_request.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=TokenUserResponse, status_code=status.HTTP_201_CREATED)
def signup_for_tenant(
    signup_request: SignupRequest,
    db: Session = Depends(get_db_session),
):
    tenant_id = resolve_tenant_id(db, tenant_name=signup_request.tenant_name)
    existing_user = get_user_by_email(db, tenant_id=tenant_id, email=signup_request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists for this tenant",
        )

    user_in = UserCreate(
        email=signup_request.email,
        full_name=signup_request.full_name,
        password=signup_request.password,
    )
    user = create_user(db=db, tenant_id=tenant_id, user_in=user_in)
    access_token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": access_token, "token_type": "bearer", "user": user}
