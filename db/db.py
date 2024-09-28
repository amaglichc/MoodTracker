from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from loguru import logger

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]


async def init_indexes():
    collection = db.User
    await collection.create_index([("email", 1), ("username", 1)], unique=True)
    logger.info("Indexes have been sucssesfully created")
