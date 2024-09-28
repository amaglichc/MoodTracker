from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://root:example@localhost:27017/"
DB_NAME = "Mood"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]