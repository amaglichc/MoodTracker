from fastapi import APIRouter
from db.repositories.UserRepo import get_user_by_id

router = APIRouter(tags=["mood"], prefix="/mood")


@router.get("")
async def get_you_moods(user_id: str) -> dict:
    user: dict = await get_user_by_id(user_id)
    return user
