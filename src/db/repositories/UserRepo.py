from db.db import db
from utils.Exceptions import (
    UserNotFoundException,
    UserAlreadyExistException,
    WrongCredentialsException,
)
from bson import ObjectId
from Schemas.UserSchema import UserSchema, SignUpSchema, SignInSchema
import datetime
from utils.Hashing import hash_password, validate_password
from pymongo.errors import DuplicateKeyError
from Auth.jwt import create_tokens

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
    user["password"] = hash_password(user["password"])
    user["is_active"] = False
    user["role"] = "USER"
    try:
        user["id"] = str((await collection.insert_one(user)).inserted_id)
    except DuplicateKeyError:
        raise UserAlreadyExistException
    return UserSchema.model_validate(user)


async def sign_in_user(user: SignInSchema):
    user_from_db: dict = await collection.find_one({"email": user.email})
    if user and validate_password(user.password, user_from_db["password"]):
        user_from_db["id"] = str(user_from_db["_id"])
        del user_from_db["_id"]
        return create_tokens(UserSchema.model_validate(user_from_db))
    raise WrongCredentialsException
