from fastapi import APIRouter, FastAPI

from src.api.v1.routes.health_check import health_check_router

# uvicorn src.main:app --reload
api_v1_router = APIRouter(prefix="/api/v1")

app = FastAPI()



app.include_router(health_check_router, prefix="/api/v1")

