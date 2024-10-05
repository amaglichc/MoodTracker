from passlib.context import CryptContext


context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return context.hash(password)


def validate_password(password: str, hashed_password: str) -> bool:
    return context.verify(password, hashed_password)
