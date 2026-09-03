from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_tenant, get_db_session
from app.schemas.user import UserCreate, UserOut
from app.services.user import create_user, list_users

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_tenant_user(body: UserCreate, db: Session = Depends(get_db_session), tenant=Depends(get_current_tenant)):
    return create_user(db, tenant.id, body)


@router.get("/", response_model=list[UserOut])
def get_tenant_users(db: Session = Depends(get_db_session), tenant=Depends(get_current_tenant)):
    return list_users(db, tenant.id)
