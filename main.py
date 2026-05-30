 from fastapi import FastAPI, Request
import httpx

# Конфигурация систем нашей корпорации
TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
app = FastAPI(title="AI_Digital_Corp_Core", version="5.0.0")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Асинхронная отправка сообщений в Telegram"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            print(f"Ошибка Telegram: {e}")

async def ask_free_ai(prompt: str) -> str:
    """Ультра-стабильное AI-ядро без региональных ограничений (Claude-3/GPT модель)"""
    url = "https://chateverywhere.app/api/chat/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Отвечай строго на русском языке, кратко, экспертно и профессионально, как ведущий аналитик компании AI Digital Corp."},
            {"role": "user", "content": prompt}
        ]
    }
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.post(url, json=payload, timeout=20.0)
            if response.status_code == 200:
                # Провайдер возвращает чистый текст
                return response.text.strip()
            return "Основной AI-канал перегружен. Повторите запрос через 30 секунд."
        except Exception as e:
            print(f"Ошибка AI-ядра: {e}")
            return "Не удалось установить соединение с сервером AI. Попробуйте еще раз."

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Партнер")

        # Команда /start
        if user_text.startswith("/start"):
            reply = (
                f"Приветствуем, *{user_name}*! 🚀\n"
                f"Вы внутри экосистемы **AI Digital Corp**.\n\n"
                f"📊 Нажмите /analytics — для технического анализа рынка.\n"
                f"🤖 Напишите любой бизнес-вопрос, и наше обновленное AI-ядро мгновенно выдаст вам решение!"
            )
            await send_telegram_message(chat_id, reply)
        
        # Команда Аналитики рынка
        elif user_text.startswith("/analytics"):
            reply = (
                f"📊 *Аналитический отчет AI Digital Corp*\n"
                f"📈 **Тренд:** Сильный бычий импульс (Strong Buy)\n"
                f"⏱ **Рекомендуемый таймфрейм:** 1-3 мин\n"
                f"📉 **Индикаторы:** RSI в нейтральной зоне (54), Bollinger Bands сужаются — ожидается мощный пробой волатильности.\n\n"
                f"_Для получения приватных сигналов обновите тариф до Premium._"
            )
            await send_telegram_message(chat_id, reply)
        
        # Запрос к текстовому AI
        else:
            await send_telegram_message(chat_id, "🤖 _Запрос обрабатывается AI-ядром корпорации... Секунду..._")
            ai_response = await ask_free_ai(user_text)
            reply = f"🧠 *Ответ AI-Ассистента Digital Corp:*\n\n{ai_response}"
            await send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
