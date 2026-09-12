from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra = "ignore",
    )
    SECRET_KEY: str
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str ="Login Service"
    DATABASE_URL: str = "postgresql+psycopg://postgres:dev@localhost:5432/postgres"

settings = Settings()
