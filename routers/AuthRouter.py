from fastapi import APIRouter
from Schemas.UserSchema import SignUpSchema, UserSchema, SignInSchema
from db.repositories.UserRepo import save_user
from db.repositories.AuthRepo import activate_user_by_token
from utils.Email import send_confirmation_email

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup")
async def signup(user: SignUpSchema):
    saved_user = await save_user(user)
    send_confirmation_email.delay(saved_user.dict())
    return {"message": "You`ve been registred, check your email to activate profile"}


@router.post("/confirm/{token}")
async def confirm_user(token: int):
    await activate_user_by_token(token)


@router.post("/signin")
async def signin(user: SignInSchema) -> UserSchema:
    pass
