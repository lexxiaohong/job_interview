import logging
import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")


logging_level = logging.INFO

logging.basicConfig(
    level=logging_level,
    format="%(asctime)s.%(msecs)03d - %(name)s : %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Job Interview")
