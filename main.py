import json
import urllib.request
import urllib.error
from fastapi import FastAPI, Request

TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
GROQ_API_KEY = "Gsk_9bvTObVDLi4Y11CtwaXyWGdyb3FYg4OzsOPjZInYsa3CgafS5Jha"

app = FastAPI(title="AI_Digital_Corp_Core", version="9.0.0")

def send_telegram_message(chat_id: int, text: str):
    """Отправка сообщений в Telegram через встроенный urllib"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read()
    except Exception as e:
        print(f"Ошибка Telegram: {e}")

def ask_free_ai(prompt: str) -> str:
    """Запрос к Groq API через встроенный urllib"""
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
                "content": "Ты — ведущий ИИ-консультант компании AI Digital Corp. Отвечай только на русском языке, развернуто, структурировано и профессионально, используя списки и маркеры."
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
        print(f"Groq HTTP Error: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
        return "ИИ-ядро перегружено. Пожалуйста, повторите запрос через минуту."
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        return "Не удалось установить защищенное соединение с ИИ-сервером корпорации."

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"status": "bad json"}
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Партнер")

        if user_text.startswith("/start"):
            reply = (
                f"Приветствуем, *{user_name}*! 🚀\n"
                f"Вы внутри экосистемы **AI Digital Corp**.\n\n"
                f"📊 Нажмите /analytics — для технического анализа рынка.\n"
                f"🤖 Напишите любой бизнес-вопрос, и наше официальное AI-ядро мгновенно выдаст вам решение!"
            )
            send_telegram_message(chat_id, reply)
        
        elif user_text.startswith("/analytics"):
            reply = (
                f"📊 *Аналитический отчет AI Digital Corp*\n"
                f"📈 **Тренд:** Сильный бычий импульс (Strong Buy)\n"
                f"⏱ **Рекомендуемый таймфрейм:** 1-3 мин\n"
                f"📉 **Индикаторы:** RSI в нейтральной зоне (54), Bollinger Bands сужаются.\n\n"
                f"_Для получения приватных сигналов обновите тариф до Premium._"
            )
            send_telegram_message(chat_id, reply)
        
        else:
            send_telegram_message(chat_id, "🤖 _Запрос обрабатывается официальным ИИ-ядром... Секунду..._")
            ai_response = ask_free_ai(user_text)
            reply = f"🧠 *Ответ AI-Ассистента Digital Corp:*\n\n{ai_response}"
            send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
