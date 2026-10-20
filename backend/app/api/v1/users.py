from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session, require_roles
from app.schemas.user import UserCreate, UserOut, UserRole
from app.services.user import create_user, list_users

router = APIRouter()


@router.get("/me", response_model=UserOut)
def get_current_user_profile(actor=Depends(get_current_user)):
    return actor


@router.post("/", response_model=UserOut)
def create_tenant_user(
    body: UserCreate,
    db: Session = Depends(get_db_session),
    actor=Depends(require_roles(UserRole.ADMIN)),
):
    try:
        return create_user(db, actor.tenant_id, body)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists for this tenant") from None


@router.get("/", response_model=list[UserOut])
def get_tenant_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db_session),
    actor=Depends(require_roles(UserRole.ADMIN, UserRole.HR)),
):
    return list_users(db, actor.tenant_id, offset=offset, limit=limit)
