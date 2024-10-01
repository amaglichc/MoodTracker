import jwt
from datetime import datetime, timedelta, UTC
from Schemas.UserSchema import UserSchema
from Schemas.TokenSchema import TokenSchema, ConfirmTokenSchema
from db.repositories.AuthRepo import save_token

ALGORITHM: str = "RS256"

# Открываем ключи
with open("certs/private.pem", "r") as private, open("certs/public.pem", "r") as public:
    private_key = private.read()
    public_key = public.read()


def create_token(
    data: dict, expire_minutes: float, private=private_key, algorithm=ALGORITHM
) -> str:
    now = datetime.now(UTC)
    exp = now + timedelta(minutes=expire_minutes)
    # Преобразуем даты в timestamp (в секунды)
    data["iat"] = now.timestamp()
    data["exp"] = exp.timestamp()
    token = jwt.encode(payload=data, key=private, algorithm=algorithm)
    return token


def decode_token(token: str, public=public_key, algorithm=ALGORITHM) -> dict:
    return jwt.decode(jwt=token, key=public, algorithms=[algorithm])


def create_access_token(user: UserSchema) -> str:
    data = {"token_type": "access", "sub": user.id, "role": UserSchema.role}
    return create_token(data, expire_minutes=15)


def create_refresh_token(user: UserSchema) -> str:
    data = {"token_type": "refresh", "sub": user.id}
    return create_token(data, expire_minutes=60 * 24 * 7)


def create_tokens(user: UserSchema) -> TokenSchema:
    return TokenSchema(
        access_token=create_access_token(user), refresh_token=create_refresh_token(user)
    )


async def create_confirmation_token(user_id: str):
    now = datetime.now(UTC)
    exp = now + timedelta(minutes=15)
    # Преобразуем даты в timestamp
    token = jwt.encode(
        {"sub": user_id, "iat": now.timestamp(), "exp": exp.timestamp()},
        key=private_key,
        algorithm=ALGORITHM,
    )
    token_schema = ConfirmTokenSchema(token=token, user_id=user_id, expires_at=exp)
    await save_token(token=token_schema)
