from pydantic_settings import BaseSettings, SettingsConfDict


class Settings(BaseSettings):
    model_config = SettingsConfDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra = "ignore",
    )

    PROJECT_NAME: str ="Login Service"
    DATABASE_URL: str = "postgresql+psycopg://postgres:dev@localhost:5432/postgres"

settings = Settings()