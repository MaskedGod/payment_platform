from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.sql import text

from app.db.database import get_db


app = FastAPI(
    title="Payment platform",
    summary="Платформа для интеграции с партнерами и проведения платежей через API.",
)


@app.get("/")
def read_root():
    return {"Hello": "from payment-platform!"}


@app.get("/health")
async def health_check(db=Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return {"status": "healthy", "db_status": "reachable"}
        else:
            return {"status": "unhealthy", "db_status": "unexpected result"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "db_status": "unreachable", "error": str(e)},
        )
