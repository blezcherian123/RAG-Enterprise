from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.deps import bearer_scheme, get_current_user, get_db_session
from app.models.revoked_token import RevokedToken
from app.schemas.auth import LoginRequest, SignupRequest
from app.schemas.user import TokenWithUser, UserCreate
from app.security import create_access_token, decode_access_token
from app.services.tenant import get_tenant_by_id, get_tenant_by_name
from app.services.user import authenticate_user, create_user, get_user_by_email

router = APIRouter()

DEFAULT_TENANT = "default"


def resolve_tenant_id(db: Session, tenant_id: str | None = None, tenant_name: str | None = None) -> str:
    if tenant_id and tenant_name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Provide only one tenant selector")
    if tenant_id:
        tenant = get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        return tenant_id

    name = tenant_name or DEFAULT_TENANT
    tenant = get_tenant_by_name(db, name)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant.id


@router.post("/login", response_model=TokenWithUser)
def login(body: LoginRequest, db: Session = Depends(get_db_session)):
    tenant_id = resolve_tenant_id(db, body.tenant_id, body.tenant_name)
    user = authenticate_user(db, tenant_id, str(body.email), body.password)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    payload = decode_access_token(credentials.credentials)
    token_id = payload.get("jti")
    if token_id is None:  # Existing tokens issued before logout revocation was enabled.
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    expiry = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    if not db.query(RevokedToken.jti).filter(RevokedToken.jti == token_id).first():
        db.add(RevokedToken(jti=token_id, expires_at=expiry))
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/signup", response_model=TokenWithUser, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, db: Session = Depends(get_db_session)):
    if body.tenant_name and body.tenant_name != DEFAULT_TENANT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Self-service signup is available for the default workspace only",
        )
    tenant_id = resolve_tenant_id(db, tenant_name=DEFAULT_TENANT)

    if get_user_by_email(db, tenant_id, str(body.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists for this tenant")

    try:
        user = create_user(
            db,
            tenant_id,
            UserCreate(email=body.email, full_name=body.full_name, password=body.password),
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists for this tenant") from None
    token = create_access_token(subject=str(user.id), tenant_id=tenant_id)
    return {"access_token": token, "token_type": "bearer", "user": user}
