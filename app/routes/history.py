from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import TranslationHistory
from app.schemas import HistoryItem
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/history", response_model=list[HistoryItem])
async def get_history(db: Session = Depends(get_db)):
    try:
        history = db.query(TranslationHistory).order_by(
            desc(TranslationHistory.created_at)
        ).limit(20).all()
        
        logger.info(f"Retrieved {len(history)} history items")
        return history
    except Exception as e:
        logger.error(f"Failed to retrieve history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

@router.get("/history/{history_id}", response_model=HistoryItem)
async def get_history_item(history_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(TranslationHistory).filter(
            TranslationHistory.id == history_id
        ).first()
        
        if not item:
            logger.warning(f"History item {history_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"History item with id {history_id} not found"
            )
        
        logger.info(f"Retrieved history item {history_id}")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve history item {history_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )