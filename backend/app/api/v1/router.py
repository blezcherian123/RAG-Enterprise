from fastapi import APIRouter
from typing import List

from app.api.v1 import auth, tenants, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
router.include_router(users.router, prefix="/users", tags=["users"])

@router.get("/models", response_model=List[str], tags=["models"])
async def get_models():
    """Return a list of available role models for the frontend.
    This can be extended to fetch from a database.
    """
    return ["hr", "employee", "finance", "c_level"]
