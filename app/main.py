from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(
    title="Payment platform",
    summary="Платформа предоставляющая удобный способ взаимодействия с партнёрским API.",
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "from payment-platform!"}
