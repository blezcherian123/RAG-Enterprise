from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.tenant import TenantCreate, TenantOut
from app.services.tenant import create_tenant, get_tenant_by_id, get_tenant_by_name

router = APIRouter()


@router.post("/", response_model=TenantOut, status_code=status.HTTP_201_CREATED)
def create_new_tenant(body: TenantCreate, db: Session = Depends(get_db_session)):
    if get_tenant_by_name(db, body.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tenant already exists")
    return create_tenant(db, body)


@router.get("/{tenant_id}", response_model=TenantOut)
def get_tenant(tenant_id: str, db: Session = Depends(get_db_session)):
    tenant = get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant
