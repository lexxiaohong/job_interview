from fastapi import FastAPI
from src.database import Base, engine
from src.api.v1.routes.health_check import health_check_router
from src.api.v1.routes.candidate import candidate_router
from src.api.v1.routes.interview import interview_router
from src.api.v1.routes.feedback import feedback_router
from contextlib import asynccontextmanager


# Database setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health_check_router, prefix="/api/v1")
app.include_router(candidate_router, prefix="/api/v1/candidates", tags=["candidates"])
app.include_router(interview_router, prefix="/api/v1/candidates/{candidate_id}/interviews", tags=["interviews"])
app.include_router(feedback_router, prefix="/api/v1/interviews/{interview_id}/feedback", tags=["feedback"])

