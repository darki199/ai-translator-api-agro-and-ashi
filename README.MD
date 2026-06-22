# 🌍 AI Translator API

Сервис перевода текста с использованием словарного подхода (EN↔RU) с сохранением истории в базу данных.

---

## 📦 Технологии

- **FastAPI** — веб-фреймворк
- **SQLite** — база данных (история переводов)
- **Docker** — контейнеризация
- **Hugging Face Transformers** — код для работы с моделями (готов)
- **Postman** — тестирование API

---

## 🚀 Запуск

### Локально (Windows/Linux)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/your-username/translator.git
cd translator

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
cp .env.example .env

# 5. Запустить приложение
python -m uvicorn app.main:app --reload