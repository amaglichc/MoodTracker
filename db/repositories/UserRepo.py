from db.db import db
from utils.Exceptions import UserNotFoundException
from bson import ObjectId
from Schemas.UserSchema import SignUpSchema,UserSchema
from fastapi import HTTPException
import datetime
import pprint
from pymongo.errors import DuplicateKeyError

collection = db["User"]


async def get_user_by_id(user_id: str) -> dict:
    try:
        user = await collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            
            return user
    except Exception:
        raise UserNotFoundException
    

async def save_user(user: SignUpSchema):
    user = user.model_dump()
    user["created_at"] = datetime.datetime.now(datetime.UTC)
    try:    
        user["id"] = str((await collection.insert_one(user)).inserted_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=409,detail="User with this email or username already created")
    pprint.pprint(user)
    return UserSchema.model_validate(user)
    