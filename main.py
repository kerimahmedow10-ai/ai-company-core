import os
import json
import urllib.request
import urllib.error
from fastapi import FastAPI, Request

# Берем ключи напрямую из безопасного окружения Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

app = FastAPI(title="AI_Digital_Corp_Core", version="10.0.0")

def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

def ask_free_ai(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "Ошибка конфигурации: API-ключ Groq не найден в системе."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system", 
                "content": "Ты — ведущий ИИ-консультант компании AI Digital Corp. Отвечай только на русском языке, развернуто и профессионально."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        # Выводим реальную ошибку в логи Render для диагностики
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"Groq API Error Status: {e.code}, Body: {error_body}")
        return f"ИИ-сервер вернул статус {e.code}. Проверьте правильность ключа в настройках."
    except Exception as e:
        return f"Ошибка соединения: {e}"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"status": "bad json"}
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

        if user_text.startswith("/start"):
            reply = "Приветствуем! 🚀 Напишите любой бизнес-вопрос, и ИИ выдаст решение."
            send_telegram_message(chat_id, reply)
        elif user_text.startswith("/analytics"):
            reply = "📊 *Аналитика:* Тренд сильный бычий импульс."
            send_telegram_message(chat_id, reply)
        else:
            send_telegram_message(chat_id, "🤖 _Запрос обрабатывается официальным ИИ-ядром..._")
            ai_response = ask_free_ai(user_text)
            send_telegram_message(chat_id, f"🧠 *Ответ:* \n\n{ai_response}")
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running"}
