from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./osint.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "OSINT API"
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    # Logging
    LOG_LEVEL: str = "INFO"

    # External APIs (for OSINT collectors)
    SHODAN_API_KEY: Optional[str] = None
    VIRUSTOTAL_API_KEY: Optional[str] = None
    HAVEIBEENPWNED_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()