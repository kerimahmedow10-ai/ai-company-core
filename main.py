from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio

app = FastAPI(title="AI_Digital_Corp_Core", version="1.0.0")

class UserMessage(BaseModel):
    user_id: str
    message: str
    client_token: str

VALID_TOKENS = {"premium_token_123", "valleys_finest_777"}

async def generate_ai_response(text: str) -> str:
    await asyncio.sleep(0.5)
    return f"[AI СЕО]: Обработал ваш запрос: '{text}'. Ответ сформирован успешно."

@app.post("/v1/chat")
async def process_chat(payload: UserMessage):
    if payload.client_token not in VALID_TOKENS:
        raise HTTPException(status_code=403, detail="Доступ отклонен. Обновите подписку.")
    
    try:
        ai_reply = await generate_ai_response(payload.message)
        return {
            "status": "success",
            "user_id": payload.user_id,
            "reply": ai_reply
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "running", "infrastructure": "stable"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
