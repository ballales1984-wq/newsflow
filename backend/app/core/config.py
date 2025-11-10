from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "NewsFlow"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:4200"
    
    @field_validator("CORS_ORIGINS")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        return [origin.strip() for origin in v.split(",")]
    
    # News APIs
    NEWSAPI_KEY: str = ""
    GUARDIAN_API_KEY: str = ""
    
    # NLP Settings
    SIMILARITY_THRESHOLD: float = 0.7
    MIN_ARTICLE_LENGTH: int = 200
    MAX_ARTICLE_AGE_DAYS: int = 30
    
    # Collection Settings
    COLLECTION_INTERVAL_HOURS: int = 1
    MAX_ARTICLES_PER_SOURCE: int = 50
    
    # Email (optional)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

