from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str
    GOOGLE_PASSWORD: str
    EMAIL_SENDER: str

    class Config:
        env_file = "dev.env"


settings = Settings()
