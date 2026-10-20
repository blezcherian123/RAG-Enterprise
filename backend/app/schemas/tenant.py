from pydantic import BaseModel, ConfigDict, Field


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)


class TenantOut(TenantCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)
