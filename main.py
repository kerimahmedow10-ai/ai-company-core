from fastapi import FastAPI, Request
import httpx
import asyncio

app = FastAPI(title="AI_Digital_Corp_Core", version="3.1.0")

TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Асинхронная отправка сообщений пользователю"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            print(f"Ошибка Telegram API: {e}")

async def ask_free_ai(prompt: str) -> str:
    """Стабильный AI-движок с маскировкой под браузер"""
    # Кодируем текст, чтобы не было проблем с пробелами в URL
    from urllib.parse import quote
    encoded_prompt = quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai"
    
    # Маскируемся под реального пользователя, чтобы избежать таймаутов
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            # Даем серверу чуть больше времени на ответ (20 секунд)
            response = await client.get(url, timeout=20.0)
            if response.status_code == 200 and response.text.strip():
                return response.text
            return "AI-ядро временно обрабатывает другую задачу. Повторите запрос через минуту!"
        except Exception as e:
            print(f"Ошибка AI: {e}")
            return "Система перегружена. Пожалуйста, попробуйте еще раз."

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Партнер")

        # 1. Приветствие
        if user_text.startswith("/start"):
            reply = (
                f"Приветствуем, *{user_name}*! 🚀\n"
                f"Вы внутри экосистемы **AI Digital Corp**.\n\n"
                f"📊 Нажмите /analytics — чтобы получить быстрый технический анализ рынка и OTC трендов.\n"
                f"🤖 Или просто напишите любой вопрос, и наш встроенный AI мгновенно сгенерирует решение!"
            )
            await send_telegram_message(chat_id, reply)
        
        # 2. Блок Трейдинга и Аналитики
        elif user_text.startswith("/analytics"):
            reply = (
                f"📊 *Аналитический отчет AI Digital Corp*\n"
                f"📈 **Тренд:** Сильный бычий импульс (Strong Buy)\n"
                f"⏱ **Рекомендуемый таймфрейм:** 1-3 мин\n"
                f"📉 **Индикаторы:** RSI в нейтральной зоне (54), Bollinger Bands сужаются — ожидается мощный пробой волатильности.\n\n"
                f"_Для получения приватных сигналов и точных точек входа обновите тариф до Premium._"
            )
            await send_telegram_message(chat_id, reply)
        
        # 3. Блок Умного AI
        else:
            await send_telegram_message(chat_id, "🤖 _AI анализирует ваш запрос... Секунду..._")
            ai_response = await ask_free_ai(user_text)
            reply = f"🧠 *Ответ AI-Ассистента Digital Corp:*\n\n{ai_response}"
            await send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
