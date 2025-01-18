from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging


app = FastAPI(title="Task Manager API")

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app):
    logger.info("Application running changed to: http://localhost:8000 for local development")
    logger.info("API Documentation available at: http://localhost:8000/docs")
    yield

app.router.lifespan_context = lifespan