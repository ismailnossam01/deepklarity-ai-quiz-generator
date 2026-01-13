import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:5644@localhost:5432/wiki_quiz_db"
    )

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", "10000")))
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    MIN_QUESTIONS: int = 5
    MAX_QUESTIONS: int = 10

    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://deepklarity-ai-quiz-generator.vercel.app",
        "https://*.vercel.app",
    ]

settings = Settings()

if not settings.GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not set in .env file!")
    print("Get your free API key from: https://makersuite.google.com/app/apikey")
