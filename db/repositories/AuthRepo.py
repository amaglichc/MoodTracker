from db.db import db
from Schemas.TokenSchema import ConfirmTokenSchema

collection = db["Token"]


async def save_token(token: ConfirmTokenSchema) -> None:
    await collection.insert_one(token.model_dump())
