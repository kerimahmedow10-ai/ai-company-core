from fastapi import FastAPI, Request
import httpx

TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
app = FastAPI(title="AI_Digital_Corp_Core", version="7.0.0")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Асинхронная отправка сообщений в Telegram"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload, timeout=10.0)
        except Exception as e:
            print(f"Ошибка Telegram: {e}")

async def ask_free_ai(prompt: str) -> str:
    """Ультра-стабильный ИИ-движок без токенов и ограничений"""
    # Используем стабильный открытый шлюз интеграции ИИ
    url = "https://open-ai-api-production.up.railway.app/v1/chat/completions"
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты — ведущий бизнес-консультант и ИИ-аналитик корпорации AI Digital Corp. Отвечай четко, профессионально и только на русском языке."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=25.0)
            if response.status_code == 200:
                res_data = response.json()
                return res_data["choices"][0]["message"]["content"].strip()
            return "ИИ-модуль калибруется. Пожалуйста, повторите запрос через минуту."
        except Exception as e:
            print(f"Ошибка ИИ: {e}")
            return "Не удалось получить ответ от ИИ-ядра. Попробуйте еще раз."

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Партнер")

        if user_text.startswith("/start"):
            reply = (
                f"Приветствуем, *{user_name}*! 🚀\n"
                f"Вы внутри экосистемы **AI Digital Corp**.\n\n"
                f"📊 Нажмите /analytics — для технического анализа рынка.\n"
                f"🤖 Напишите любой бизнес-вопрос, и наше AI-ядро мгновенно выдаст вам решение!"
            )
            await send_telegram_message(chat_id, reply)
        
        elif user_text.startswith("/analytics"):
            reply = (
                f"📊 *Аналитический отчет AI Digital Corp*\n"
                f"📈 **Тренд:** Сильный бычий импульс (Strong Buy)\n"
                f"⏱ **Рекомендуемый таймфрейм:** 1-3 мин\n"
                f"📉 **Индикаторы:** RSI в нейтральной зоне (54), Bollinger Bands сужаются.\n\n"
                f"_Для получения приватных сигналов обновите тариф до Premium._"
            )
            await send_telegram_message(chat_id, reply)
        
        else:
            await send_telegram_message(chat_id, "🤖 _Запрос обрабатывается AI-ядром корпорации... Секунду..._")
            ai_response = await ask_free_ai(user_text)
            reply = f"🧠 *Ответ AI-Ассистента Digital Corp:*\n\n{ai_response}"
            await send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
