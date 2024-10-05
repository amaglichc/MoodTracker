from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from loguru import logger
from routers.MoodRouter import router as MoodRouter
from routers.AuthRouter import router as AuthRouter
from db.db import client, init_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app succsessfully startup")
    await init_indexes()
    yield
    client.close()
    logger.info("Mongo db connection close")


app = FastAPI(lifespan=lifespan)

app.include_router(MoodRouter)
app.include_router(AuthRouter)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )