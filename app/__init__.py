from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from contextlib import asynccontextmanager
import logging
import os

from dotenv import load_dotenv


# Retrieve environment variables
load_dotenv()
sqlite_file_name = os.getenv("SQLITE_FILE_NAME")
sqlite_url = os.getenv("SQLITE_URL", f"sqlite:///{sqlite_file_name}")


# Create the FastAPI application
app = FastAPI(title=os.getenv("APP_NAME", "API"))


# Get the Uvicorn logger (FastAPI is using Uvicorn)
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


# Log the application running and API documentation URLs at startup
@asynccontextmanager
async def lifespan(app):
    logger.info(
        "Application running changed to: http://localhost:8000 for local development")
    logger.info(
        "API Documentation available at: http://localhost:8000/docs")

    # Create the SQLite database if it does not exist
    if not os.path.exists(sqlite_file_name):
        try:
            engine = create_engine(sqlite_url, echo=False)
            SQLModel.metadata.create_all(engine)
        except Exception as e:
            logger.error(
                f"Error creating SQLite database: {e}")
        else:
            logger.info(
                f'SQLite database "{sqlite_file_name}" was created.')

    yield

app.router.lifespan_context = lifespan
