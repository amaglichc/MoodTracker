from fastapi import APIRouter, Depends
from Schemas.UserSchema import SignUpSchema, SignInSchema, UserSchema
from Schemas.TokenSchema import TokenSchema
from db.repositories.UserRepo import save_user, sign_in_user
from db.repositories.AuthRepo import activate_user_by_token
from utils.Email import send_confirmation_email
from typing import Annotated
from Auth.main import get_user_by_token

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup")
async def signup(user: SignUpSchema):
    saved_user = await save_user(user)
    send_confirmation_email.delay(saved_user.dict())
    return {"message": "You`ve been registred, check your email to activate profile"}


@router.get("/confirm/{token}")
async def confirm_user(token: int):
    await activate_user_by_token(token)
    return {"User has been activate"}


@router.post("/signin")
async def signin(user: SignInSchema) -> TokenSchema:
    return await sign_in_user(user)


async def refresh_token() -> TokenSchema: ...


@router.get("/protect")
async def protect_endpoind(
    user: Annotated[UserSchema, Depends(get_user_by_token)]
) -> UserSchema:
    return user
