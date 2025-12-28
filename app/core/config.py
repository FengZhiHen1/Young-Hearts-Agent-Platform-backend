from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "心青年智能体平台 - Backend"
    DB_URL: str = "sqlite:///./dev.db"
    VECTOR_STORE: str = "chroma"

    class Config:
        env_file = ".env"


settings = Settings()
