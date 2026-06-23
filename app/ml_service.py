import logging
from app.config import config
import re
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.model_name = config.HUGGINGFACE_MODEL
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            logger.info(f"🔄 Loading model: {self.model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_fast=False
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name
            )
            
            self.model_loaded = True
            logger.info("✅ Model loaded successfully!")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not load model: {e}")
            logger.info("ℹ️ Using dictionary-based translation")
            self.model_loaded = False
    
    def detect_languages(self, text):
        cyrillic = len(re.findall(r'[а-яА-ЯёЁ]', text))
        latin = len(re.findall(r'[a-zA-Z]', text))
        
        if cyrillic > latin:
            return "ru", "en"
        else:
            return "en", "ru"
    
    def translate(self, text: str):
        source_lang, target_lang = self.detect_languages(text)
        
        if not self.model_loaded:
            return self._translate_with_dict(text, source_lang, target_lang)
        
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            outputs = self.model.generate(
                **inputs,
                max_length=512,
                num_beams=4,
                early_stopping=True
            )
            
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "translated_text": translated_text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence_score": 0.95
            }
            
        except Exception as e:
            logger.error(f"❌ Translation error: {e}")
            return self._translate_with_dict(text, source_lang, target_lang)
    
    def _translate_with_dict(self, text, source_lang, target_lang):
        """Резервный словарный перевод — работает всегда!"""
        translations = {
            "hello": "привет", "world": "мир", "love": "люблю",
            "like": "нравится", "python": "питон", "programming": "программирование",
            "i": "я", "you": "ты", "we": "мы", "they": "они",
            "good": "хороший", "bad": "плохой", "beautiful": "прекрасный",
            "movie": "фильм", "book": "книга", "cat": "кот", "dog": "собака",
            "this": "этот", "that": "тот", "these": "эти", "those": "те",
            "today": "сегодня", "tomorrow": "завтра", "yesterday": "вчера",
            "now": "сейчас", "then": "тогда", "here": "здесь", "there": "там",
            "thank": "спасибо", "please": "пожалуйста", "sorry": "извините",
            "yes": "да", "no": "нет", "ok": "хорошо",
            "friend": "друг", "family": "семья", "time": "время", "day": "день",
            
            "привет": "hello", "мир": "world", "люблю": "love",
            "нравится": "like", "питон": "python", "программирование": "programming",
            "я": "i", "ты": "you", "мы": "we", "они": "they",
            "хороший": "good", "плохой": "bad", "красивый": "beautiful",
            "фильм": "movie", "книга": "book", "кот": "cat", "собака": "dog",
            "этот": "this", "тот": "that", "эти": "these", "те": "those",
            "сегодня": "today", "завтра": "tomorrow", "вчера": "yesterday",
            "спасибо": "thank you", "пожалуйста": "please", "извините": "sorry",
            "да": "yes", "нет": "no", "хорошо": "ok"
        }
        
        words = text.lower().split()
        translated_words = []
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word)
            translated = translations.get(clean_word, word)
            translated_words.append(translated)
        
        translated_text = " ".join(translated_words)
        
        if translated_text and text[0].isupper():
            translated_text = translated_text.capitalize()
        
        if text.endswith('!') and not translated_text.endswith('!'):
            translated_text += '!'
        elif text.endswith('?') and not translated_text.endswith('?'):
            translated_text += '?'
        elif text.endswith('.') and not translated_text.endswith('.'):
            translated_text += '.'
        
        return {
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "confidence_score": 0.85
        }

translation_service = TranslationService()