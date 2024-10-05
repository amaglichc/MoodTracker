from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from typing import Annotated
from Auth.jwt import decode_token
from jwt import ExpiredSignatureError
from utils.Exceptions import TokenException, InActiveUserException
from Schemas.UserSchema import UserSchema
from db.repositories.UserRepo import get_user_by_id

bearer = HTTPBearer()


def get_token_payload(cred: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    token = cred.credentials
    try:
        payload = decode_token(token=token)
        return payload
    except ExpiredSignatureError:
        raise TokenException


async def get_user_by_token(
    payload: Annotated[dict, Depends(get_token_payload)]
) -> UserSchema:
    user_id: str = payload["sub"]
    user = await get_user_by_id(user_id=user_id)
    if not user["is_active"]:
        raise InActiveUserException
    return UserSchema.model_validate(user)