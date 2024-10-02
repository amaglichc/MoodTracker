from pydantic import BaseModel
from datetime import datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ConfirmTokenSchema(BaseModel):
    token: int
    user_id: str
    expires_at: datetime
