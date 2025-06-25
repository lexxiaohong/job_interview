from fastapi import APIRouter, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.database import Base, engine
from src.api.v1.routes.health_check import health_check_router

# uvicorn src.main:app --reload
api_v1_router = APIRouter(prefix="/api/v1")

app = FastAPI()

# Database setup
Base.metadata.create_all(bind=engine)



app.include_router(health_check_router, prefix="/api/v1")

