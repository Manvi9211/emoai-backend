from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from db.database import get_conn
from services import emotion_service, llm_service
from services.auth_service import get_user

router = APIRouter(prefix="/journal", tags=["journal"])


def _get_user_id(authorization: str) -> str:
    return get_user(authorization.replace("Bearer ", ""))["user_id"]


class JournalRequest(BaseModel):
    content: str = Field(..., min_length=10, max_length=5000)


@router.post("")
def create_entry(req: JournalRequest, authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    emotion = emotion_service.detect(req.content)
    reflection = llm_service.journal_reflection(req.content)
    word_count = len(req.content.split())

    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO journal_entries (user_id, content, reflection, emotion, word_count) VALUES (?,?,?,?,?)",
        (user_id, req.content, reflection, emotion["label"], word_count),
    )
    entry_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"id": entry_id, "reflection": reflection, "emotion": emotion, "word_count": word_count}


@router.get("/history")
def get_entries(limit: int = 20, authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    conn = get_conn()
    rows = conn.execute(
        """SELECT id, emotion, word_count, created_at, substr(content,1,120) AS preview
           FROM journal_entries WHERE user_id = ?
           ORDER BY created_at DESC LIMIT ?""",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return {"entries": [dict(r) for r in rows]}
