from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from routers.MoodRouter import router as moodRouter
from db import client

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app succsessfully startup")
    yield
    client.close()
    logger.info("Mongo db connection close")
    
    
app = FastAPI(lifespan=lifespan)

app.include_router(moodRouter)
@app.get("/")
async def root():
    return {"message": "Hello World!"}
