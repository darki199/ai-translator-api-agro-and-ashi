from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.ml_service import translation_service
from app.schemas import HealthResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    model_status = "loaded"
    
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    try:
        if translation_service:
            model_status = "loaded"
        else:
            model_status = "not loaded"
    except Exception as e:
        model_status = f"error: {str(e)}"
        logger.error(f"Model health check failed: {e}")
    
    return HealthResponse(
        status="ok",
        database=db_status,
        model=model_status
    )