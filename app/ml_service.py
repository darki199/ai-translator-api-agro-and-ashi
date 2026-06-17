import logging
from app.config import config
from transformers import pipeline

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_name = config.HUGGINGFACE_MODEL
        self.translator = None
        self.load_model()
    
    def load_model(self):
        """Загрузка локальной модели перевода"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.translator = pipeline("translation", model=self.model_name)
            logger.info("✅ Model loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.translator = None
    
    def detect_languages(self, text):
        """Определение языка по символам"""
        if any('\u0400' <= char <= '\u04FF' for char in text):
            return "ru", "en"
        else:
            return "en", "ru"
    
    def translate(self, text: str):
        try:
            source_lang, target_lang = self.detect_languages(text)
            
            # Если модель загружена
            if self.translator:
                try:
                    # Если русский → английский, а модель en-ru, меняем модель
                    if source_lang == "ru" and "en-ru" in self.model_name:
                        logger.info("Switching to ru-en model")
                        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ru-en")
                    
                    result = self.translator(text, max_length=512)
                    translated_text = result[0]['translation_text']
                    confidence_score = 0.85
                    
                    logger.info(f"✅ Translation: {source_lang}->{target_lang}")
                    return {
                        "translated_text": translated_text,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "confidence_score": confidence_score
                    }
                except Exception as e:
                    logger.error(f"Model translation failed: {e}")
                    return self._mock_translate(text, source_lang, target_lang)
            else:
                # Если модель не загружена — заглушка
                logger.warning("Model not loaded, using mock")
                return self._mock_translate(text, source_lang, target_lang)
                
        except Exception as e:
            logger.error(f"Translation error: {e}")
            source_lang, target_lang = self.detect_languages(text)
            return self._mock_translate(text, source_lang, target_lang)
    
    def _mock_translate(self, text, source_lang, target_lang):
        """Заглушка (на случай ошибки модели)"""
        translations = {
            "I like this movie!": "Мне нравится этот фильм!",
            "Hello, how are you?": "Привет, как дела?",
            "Thank you": "Спасибо",
            "Good morning": "Доброе утро",
            "Goodbye": "До свидания",
        }
        
        translated_text = translations.get(text)
        if not translated_text:
            if source_lang == "en":
                translated_text = f"Перевод: {text}"
            else:
                translated_text = f"Translation: {text}"
        
        return {
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "confidence_score": 0.50
        }

translation_service = TranslationService()