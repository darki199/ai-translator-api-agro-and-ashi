import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./translator.db")
    HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Helsinki-NLP/opus-mt-en-ru")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
config = Config()