from fastapi import FastAPI, Request
import httpx
import asyncio

app = FastAPI(title="AI_Digital_Corp_Core", version="2.0.0")

# Данные нашей компании (зашиваем ваш токен безопасности)
TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Асинхронная отправка ответа пользователю в Telegram"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Слушатель сообщений от нашего Telegram-бота"""
    data = await request.json()
    
    # Проверяем, что пришло именно текстовое сообщение
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Клиент")

        # Приветственное сообщение
        if user_text.startswith("/start"):
            reply = f"Приветствуем вас, {user_name}! 🚀\nВы обратились в AI Digital Corp. Я — ваш персональный AI-ассистент.\n\nЗадайте мне любой вопрос по автоматизации бизнеса, разработке или трейдингу, и я мгновенно сформирую решение!"
        else:
            # Имитация работы мощного AI-интеллекта компании
            reply = f"[AI СЕО] Специально для вас, {user_name}:\nЯ проанализировал ваш запрос '{user_text}'. Система автоматизации подготавливает персональное решение. Наша платформа работает на 100%!"

        # Отправляем ответ в чат
        await send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
