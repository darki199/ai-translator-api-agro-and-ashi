from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def web_interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>AI Translator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            textarea {
                width: 100%;
                height: 120px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                font-family: Arial;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background: #45a049;
            }
            #result {
                margin-top: 20px;
                padding: 15px;
                background: #e8f5e9;
                border-radius: 5px;
                display: none;
            }
            #result.show {
                display: block;
            }
            .label {
                font-weight: bold;
                color: #333;
            }
            .error {
                background: #ffebee;
                color: #c62828;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
                display: none;
            }
            .error.show {
                display: block;
            }
            .loading {
                text-align: center;
                color: #666;
                margin-top: 10px;
                display: none;
            }
            .loading.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Translator</h1>
            
            <label for="text">Введите текст для перевода:</label>
            <textarea id="text" placeholder="Enter text to translate...">I like this movie!</textarea>
            
            <button onclick="translateText()">🚀 Перевести</button>
            
            <div class="loading" id="loading">⏳ Перевод...</div>
            <div class="error" id="error"></div>
            
            <div id="result">
                <p><span class="label">📝 Оригинал:</span> <span id="original"></span></p>
                <p><span class="label">✅ Перевод:</span> <span id="translated"></span></p>
                <p><span class="label">🌍 Языки:</span> <span id="languages"></span></p>
                <p><span class="label">📊 Уверенность:</span> <span id="confidence"></span></p>
            </div>
        </div>

        <script>
        async function translateText() {
            const text = document.getElementById('text').value.trim();
            const resultDiv = document.getElementById('result');
            const loadingDiv = document.getElementById('loading');
            const errorDiv = document.getElementById('error');
            
            resultDiv.classList.remove('show');
            errorDiv.classList.remove('show');
            errorDiv.textContent = '';
            
            if (!text) {
                errorDiv.textContent = '❌ Введите текст!';
                errorDiv.classList.add('show');
                return;
            }
            
            loadingDiv.classList.add('show');
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Ошибка');
                }
                
                document.getElementById('original').textContent = data.original_text;
                document.getElementById('translated').textContent = data.translated_text;
                document.getElementById('languages').textContent = data.source_lang + ' → ' + data.target_lang;
                document.getElementById('confidence').textContent = (data.confidence_score * 100).toFixed(0) + '%';
                
                resultDiv.classList.add('show');
                
            } catch (error) {
                errorDiv.textContent = '❌ ' + error.message;
                errorDiv.classList.add('show');
            } finally {
                loadingDiv.classList.remove('show');
            }
        }
        </script>
    </body>
    </html>
    """