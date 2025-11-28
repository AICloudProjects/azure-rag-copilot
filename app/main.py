# app/main.py
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "llm-hello-service"
    env: str = "dev"
    request_timeout_s: float = 15.0

settings = Settings()
app = FastAPI(title=settings.app_name)

@app.get("/healthz")
def healthz(): return {"status": "ok"}

@app.get("/readyz")
def readyz(): return {"ready": True, "env": settings.env}

from app.utils.logging import RequestContextMiddleware
app.add_middleware(RequestContextMiddleware)

from app import api
app.include_router(api.router)
