from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.routes import analyze, history, health
from app.database import engine, Base
from app.config import config
import logging
import sys
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Создание таблиц в БД
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise

# Создание FastAPI приложения
app = FastAPI(
    title="AI Translator API",
    description="Translation service using Hugging Face models",
    version="1.0.0"
)

# Маршрутизация
app.include_router(health.router, tags=["Health"])
app.include_router(analyze.router, tags=["Translation"])
app.include_router(history.router, tags=["History"])

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response status: {response.status_code}, time: {process_time:.3f}s")
        return response
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise

# Обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.on_event("startup")
async def startup_event():
    logger.info("AI Translator API service started")
    logger.info(f"Using model: {config.HUGGINGFACE_MODEL}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Translator API service shutting down")