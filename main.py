from fastapi import FastAPI, Request
import httpx

# Настройки подключения к Telegram
TELEGRAM_TOKEN = "8727691504:AAHPhlzNi2qcNyVMe7pOaX0cuFGBRDUomm0"
app = FastAPI(title="AI_Digital_Corp_Core", version="6.0.0")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

async def send_telegram_message(chat_id: int, text: str):
    """Асинхронная отправка сообщений в Telegram"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload, timeout=10.0)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

async def ask_free_ai(prompt: str) -> str:
    """Стабильный ИИ-движок на базе открытой модели Llama-3 через Hugging Face API"""
    # Используем публичный стабильный шлюз без авторизации
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    
    # Формируем правильный запрос для ИИ эксперта
    full_prompt = f"<|system|>\nОтвечай строго на русском языке, кратко и профессионально, как AI эксперт. внедри в ответ бизнес-анализ.\n<|user|>\n{prompt}\n<|assistant|>\n"
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 250, "temperature": 0.7}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=15.0)
            if response.status_code == 200:
                res_json = response.json()
                # Извлекаем сгенерированный текст и очищаем от промпта
                generated_text = res_json[0]["generated_text"]
                clean_text = generated_text.split("<|assistant|>\n")[-1].strip()
                return clean_text if clean_text else "Ответ сформирован, но пуст. Попробуйте еще раз."
            return "AI-модель сейчас перезагружается в облаке. Подождите 30 секунд и повторите запрос!"
        except Exception as e:
            print(f"Ошибка ИИ-движка: {e}")
            return "Канал связи с ИИ временно занят. Пожалуйста, отправьте запрос повторно."

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        user_name = data["message"]["from"].get("first_name", "Партнер")

        # 1. Обработка стартовой команды
        if user_text.startswith("/start"):
            reply = (
                f"Приветствуем, *{user_name}*! 🚀\n"
                f"Вы внутри экосистемы **AI Digital Corp**.\n\n"
                f"📊 Нажмите /analytics — для технического анализа рынка.\n"
                f"🤖 Напишите любой бизнес-вопрос, и наше обновленное AI-ядро мгновенно выдаст вам решение!"
            )
            await send_telegram_message(chat_id, reply)
        
        # 2. Обработка аналитики рынка
        elif user_text.startswith("/analytics"):
            reply = (
                f"📊 *Аналитический отчет AI Digital Corp*\n"
                f"📈 **Тренд:** Сильный бычий импульс (Strong Buy)\n"
                f"⏱ **Рекомендуемый таймфрейм:** 1-3 мин\n"
                f"📉 **Индикаторы:** RSI в нейтральной зоне (54), Bollinger Bands сужаются — ожидается мощный пробой волатильности.\n\n"
                f"_Для получения приватных сигналов обновите тариф до Premium._"
            )
            await send_telegram_message(chat_id, reply)
        
        # 3. Обработка любых вопросов к ИИ
        else:
            await send_telegram_message(chat_id, "🤖 _Запрос обрабатывается AI-ядром корпорации... Секунду..._")
            ai_response = await ask_free_ai(user_text)
            reply = f"🧠 *Ответ AI-Ассистента Digital Corp:*\n\n{ai_response}"
            await send_telegram_message(chat_id, reply)
        
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}
