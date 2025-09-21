from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Surgery Scheduler API"
    APP_VERSION: str = "1.0.0"
    MONGODB_URI: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
