from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(
    title="Payment platform",
    summary="Платформа для интеграции с партнерами и проведения платежей через API.",
)

app.include_router(api_router)


# @app.get("/")
# def read_root():
#     return {"Hello": "from payment-platform!"}
