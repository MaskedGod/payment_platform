import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router

app = FastAPI(
    title="Payment platform",
    summary="Платформа предоставляющая удобный способ взаимодействия с партнёрским API.",
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "from payment-platform!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
