from transformers import FSMTForConditionalGeneration, FSMTTokenizer
import logging
from app.config import config
import re
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_name = config.HUGGINGFACE_MODEL
        self.translator = None
        
        try:
            from transformers import pipeline
            
            logger.info(f"🔄 Loading translation pipeline...")
            
            self.translator = pipeline(
                "translation",
                model=self.model_name,
                tokenizer=self.model_name
            )
            
            logger.info("✅ Translation pipeline loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            logger.info("💡 Trying fallback...")
            self._setup_fallback()
    
    def _setup_fallback(self):
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            logger.info(f"🔄 Loading model directly...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_fast=False
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name
            )
            logger.info("✅ Model loaded directly!")
            
        except Exception as e:
            logger.error(f"❌ All loading attempts failed: {e}")
            raise
    
    def detect_languages(self, text):
        cyrillic = len(re.findall(r'[а-яА-ЯёЁ]', text))
        latin = len(re.findall(r'[a-zA-Z]', text))
        return ("ru", "en") if cyrillic > latin else ("en", "ru")
    
    def translate(self, text: str):
        source_lang, target_lang = self.detect_languages(text)
        
        try:
            if hasattr(self, 'translator') and self.translator:
                result = self.translator(text)
                translated = result[0]['translation_text']
            else:
                tokenizer = self.tokenizer
                model = self.model
                
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                )
                
                outputs = model.generate(
                    **inputs,
                    max_length=512,
                    num_beams=4
                )
                
                translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "translated_text": translated,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence_score": 0.95
            }
            
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return {
                "translated_text": f"ERROR: {text}",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence_score": 0.0
            }

try:
    translation_service = TranslationService()
except Exception as e:
    logger.error(f"CRITICAL: {e}")
    logger.info("💡 TIP: Try 'pip install transformers --upgrade'")
    exit(1)
def __init__(self):
    self.model_name = "facebook/wmt19-en-ru"
    self.tokenizer = FSMTTokenizer.from_pretrained(self.model_name)
    self.model = FSMTForConditionalGeneration.from_pretrained(self.model_name)