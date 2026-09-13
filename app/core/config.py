from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True, 
        extra = "ignore",
    )
    PROJECT_NAME: str ="Login Service"
    DATABASE_URL: str = "postgresql+psycopg://postgres:dev@localhost:5432/postgres"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str

    # JWT signing (RS256)
    PRIVATE_KEY_PATH: str = Path("keys/private.pem").read_text()
    PUBLIC_KEY_PATH: str = Path("keys/public.pem").read_text()
    JWT_KEY_ID: str = "2026-09"            # the "kid"; change it when you rotate keys
    JWT_ISSUER: str = "http://localhost:8000"
    JWT_AUDIENCE: str = "my-apps"          # start with one shared audience
    
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    

settings = Settings()
