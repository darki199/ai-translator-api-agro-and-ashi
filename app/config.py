import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/translator_db")
    HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Helsinki-NLP/opus-mt-en-ru")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
config = Config()