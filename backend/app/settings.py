from pydantic import BaseSettings


# Класс для загрузки настроек из .env
class Settings(BaseSettings):
    api_token: str

    class Config:
        env_file = ".env"

settings = Settings()