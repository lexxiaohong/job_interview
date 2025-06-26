from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import DATABASE_URL

# Set echo=True for debugging purposes, can be set to False in production
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# cannot move this import to the top because of Base will not know CandidateModel, FeedbackModel, InterviewModel !!!
from src.models.models import CandidateModel, FeedbackModel, InterviewModel
