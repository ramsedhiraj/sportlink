from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Application settings using Pydantic v2 BaseSettings.
    Load configuration from environment variables or .env file.
    """
    
    # Application
    APP_NAME: str = "SportLink"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    API_V1_STR: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/sportlink"
    )
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", 10))
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = int(os.getenv("REDIS_CACHE_TTL", 3600))
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    if os.getenv("CORS_ORIGINS"):
        CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 104857600))  # 100MB
    ALLOWED_IMAGE_EXTENSIONS: list = ["jpg", "jpeg", "png", "gif", "webp"]
    ALLOWED_VIDEO_EXTENSIONS: list = ["mp4", "avi", "mov", "mkv", "webm"]
    
    # AWS S3 (Optional)
    USE_S3: bool = os.getenv("USE_S3", "False") == "True"
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME: Optional[str] = os.getenv("AWS_S3_BUCKET_NAME", "sportlink-uploads")
    AWS_S3_REGION: Optional[str] = os.getenv("AWS_S3_REGION", "us-east-1")
    
    # Local Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    # Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "noreply@sportlink.com")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True") == "True"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", 900))  # 15 minutes
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", 20))
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", 100))
    
    # WebSocket
    WEBSOCKET_HEARTBEAT: int = int(os.getenv("WEBSOCKET_HEARTBEAT", 30))
    MAX_CONNECTIONS_PER_USER: int = int(os.getenv("MAX_CONNECTIONS_PER_USER", 5))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Features
    ENABLE_NOTIFICATIONS: bool = os.getenv("ENABLE_NOTIFICATIONS", "True") == "True"
    ENABLE_RECOMMENDATIONS: bool = os.getenv("ENABLE_RECOMMENDATIONS", "True") == "True"
    ENABLE_MESSAGING: bool = os.getenv("ENABLE_MESSAGING", "True") == "True"
    ENABLE_WEBSOCKET: bool = os.getenv("ENABLE_WEBSOCKET", "True") == "True"
    
    # Recommendation Engine
    MIN_ENGAGEMENT_SCORE: int = int(os.getenv("MIN_ENGAGEMENT_SCORE", 50))
    RECOMMENDATION_LIMIT: int = int(os.getenv("RECOMMENDATION_LIMIT", 10))
    TALENT_ALERT_THRESHOLD: float = float(os.getenv("TALENT_ALERT_THRESHOLD", 0.8))
    
    # Security
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", 12))
    PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", 8))
    REQUIRE_SPECIAL_CHAR: bool = os.getenv("REQUIRE_SPECIAL_CHAR", "True") == "True"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Initialize global settings
settings = Settings()
