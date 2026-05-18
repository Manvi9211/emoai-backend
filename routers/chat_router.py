from fastapi import APIRouter, Header
from pydantic import BaseModel, Field
from config import MAX_HISTORY_MESSAGES, MAX_INPUT_CHARS
from services import emotion_service, llm_service, crisis_service
from services.auth_service import get_user

router = APIRouter(prefix="/chat", tags=["chat"])
_histories: dict[str, list] = {}


def _get_user_id(authorization: str) -> str:
    token = authorization.replace("Bearer ", "")
    return get_user(token)["user_id"]


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=MAX_INPUT_CHARS)


@router.post("")
def send_message(req: ChatRequest, authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    crisis = crisis_service.is_crisis(req.message)
    emotion = emotion_service.detect(req.message)

    history = _histories.setdefault(user_id, [])
    history.append({"role": "user", "content": req.message})
    if len(history) > MAX_HISTORY_MESSAGES:
        _histories[user_id] = history[-MAX_HISTORY_MESSAGES:]
        history = _histories[user_id]

    reply = llm_service.chat_reply(history, emotion["label"], emotion["score"])
    if crisis:
        reply = crisis_service.append_footer(reply)

    history.append({"role": "assistant", "content": reply})
    return {"reply": reply, "emotion": emotion}


@router.delete("/clear")
def clear_session(authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    _histories.pop(user_id, None)
    return {"cleared": True}
