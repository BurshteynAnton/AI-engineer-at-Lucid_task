from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user:password@localhost:3306/blog_db"
    
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    max_post_size_mb: int = 1
    cache_expire_minutes: int = 5

    api_v1_prefix: str = "/api/v1"
    project_name: str = "FastAPI Blog API"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()