from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I like this movie!"
            }
        }

class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence_score: Optional[float] = None

class HistoryItem(BaseModel):
    id: int
    input_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    model_name: str
    confidence_score: Optional[float]
    created_at: datetime

class HealthResponse(BaseModel):
    status: str
    database: str
    model: str

class ErrorResponse(BaseModel):
    error: str
    detail: str