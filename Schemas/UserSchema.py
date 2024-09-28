from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class SignUpSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=5, max_length=50)


class UserSchema(SignUpSchema):
    id: str
    created_at: datetime
    password: str = Field(max_length=97)
