from db.db import db
from Schemas.TokenSchema import ConfirmTokenSchema
from random import randint
from datetime import datetime, UTC, timedelta
from utils.Exceptions import TokenException
from bson import ObjectId

collection = db["Token"]


async def create_and_save_token(user_id: str) -> int:
    token = randint(100000, 999999)
    token_schema = ConfirmTokenSchema(
        token=token,
        user_id=user_id,
        expires_at=(datetime.now(UTC) + timedelta(minutes=15)),
    )

    await collection.insert_one(token_schema.model_dump())
    return token


async def activate_user_by_token(token: int) -> None:
    token_info = await collection.find_one({"token": token})
    if token_info:
        expires_at: datetime = token_info["expires_at"]
        print(type(expires_at))
        if expires_at.timestamp() >= (datetime.now(UTC)).timestamp():
            user_collection = db["User"]
            user_collection.update_one(
                {"_id": ObjectId(token_info["user_id"])}, {"$set": {"is_active": True}}
            )
            return None
    raise TokenException
