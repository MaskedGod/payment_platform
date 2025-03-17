from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql import text

from app.db.database import get_db


router = APIRouter()


@router.get("/")
async def health_check(db=Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "db_status": "reachable"}

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "db_status": "unreachable", "error": str(e)},
        )
