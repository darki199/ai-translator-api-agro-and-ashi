from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import TranslateRequest, TranslateResponse
from app.ml_service import translation_service
from app.database import get_db
from app.models import TranslationHistory
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest, db: Session = Depends(get_db)):
    if not request.text or not request.text.strip():
        logger.warning("Empty text received")
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        translation_result = translation_service.translate(request.text)
        
        history_entry = TranslationHistory(
            input_text=request.text,
            translated_text=translation_result["translated_text"],
            source_lang=translation_result["source_lang"],
            target_lang=translation_result["target_lang"],
            model_name=translation_service.model_name,
            confidence_score=translation_result["confidence_score"]
        )
        
        db.add(history_entry)
        db.commit()
        db.refresh(history_entry)
        
        logger.info(f"Translation saved with id: {history_entry.id}")
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translation_result["translated_text"],
            source_lang=translation_result["source_lang"],
            target_lang=translation_result["target_lang"],
            confidence_score=translation_result["confidence_score"]
        )
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Translation service error: {str(e)}")