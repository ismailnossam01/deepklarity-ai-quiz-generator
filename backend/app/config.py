import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/wiki_quiz_db"
    )
    
    # Gemini API settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Application settings
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    
    # Quiz generation settings
    MIN_QUESTIONS: int = 5
    MAX_QUESTIONS: int = 10
    
    # CORS settings (Allow frontend to connect)
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

# Create settings instance
settings = Settings()

# Validate critical settings
if not settings.GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not set in .env file!")
    print("Get your free API key from: https://makersuite.google.com/app/apikey")