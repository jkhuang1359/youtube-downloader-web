import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
