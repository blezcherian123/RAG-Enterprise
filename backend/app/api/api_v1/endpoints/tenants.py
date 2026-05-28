from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.schemas.tenant import TenantCreate, TenantOut
from app.services.tenant_service import create_tenant, get_tenant_by_id, get_tenant_by_name

router = APIRouter()


@router.post("/", response_model=TenantOut, status_code=status.HTTP_201_CREATED)
def create_new_tenant(*, db: Session = Depends(get_db_session), tenant_in: TenantCreate):
    existing_tenant = get_tenant_by_name(db, name=tenant_in.name)
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tenant already exists.",
        )
    return create_tenant(db=db, tenant_in=tenant_in)


@router.get("/{tenant_id}", response_model=TenantOut)
def read_tenant(*, db: Session = Depends(get_db_session), tenant_id: str):
    tenant = get_tenant_by_id(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant
