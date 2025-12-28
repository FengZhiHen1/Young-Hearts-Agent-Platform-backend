from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "心青年智能体平台 - Backend"
    DB_URL: str = "sqlite:///./dev.db"
    VECTOR_STORE: str = "chroma"

    # auth settings
    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
