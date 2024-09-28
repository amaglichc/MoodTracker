from fastapi import APIRouter
from Schemas.UserSchema import SignUpSchema, UserSchema
from db.repositories.UserRepo import save_user


router = APIRouter(tags=["Auth"])


@router.post("/signup")
async def signup(user: SignUpSchema) -> UserSchema:
    return await save_user(user)
