from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)


class TenantOut(TenantCreate):
    id: str

    class Config:
        from_attributes = True
