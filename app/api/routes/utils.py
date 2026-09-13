from fastapi import APIRouter, Depends

# from app.api.deps import get_current_active_superuser

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check() -> bool:
    return True


