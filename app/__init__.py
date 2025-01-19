from typing import Optional
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine.base import Engine
from contextlib import asynccontextmanager
import logging
import os

from dotenv import load_dotenv


load_dotenv()
sqlite_file_name = os.getenv("SQLITE_FILE_NAME")
sqlite_url = os.getenv("SQLITE_URL", f"sqlite:///{sqlite_file_name}")
app_name = os.getenv("APP_NAME", "API")


# Create the FastAPI application
app = FastAPI(title=app_name)


# Get the Uvicorn logger (FastAPI is using Uvicorn)
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


# Create the SQLite database engine
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args={"check_same_thread": False})


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
            create_db_and_tables()
        except Exception as e:
            logger.error(
                f"Error creating SQLite database: {e}")
        else:
            logger.info(
                f'SQLite database "{sqlite_file_name}" was created.')

    yield

app.router.lifespan_context = lifespan


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
