from fastapi import APIRouter
from bson import ObjectId
from db import db
from utils.Exceptions import UserNotFoundException
router = APIRouter(
    tags=["mood"],
    prefix="/mood"
)

@router.get("")
async def get_you_moods(user_id: str):
    collection = db["User"]
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise UserNotFoundException