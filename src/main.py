from fastapi import APIRouter, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.database import Base, engine
from src.api.v1.routes.health_check import health_check_router
from src.api.v1.routes.candidate import candidate_router
from contextlib import asynccontextmanager

# uvicorn src.main:app --reload
api_v1_router = APIRouter(prefix="/api/v1")



# Database setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)



app.include_router(health_check_router, prefix="/api/v1")
app.include_router(candidate_router, prefix="/api/v1/candidates")

