from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str

    class Config:
        env_file = "dev.env"


settings = Settings()
