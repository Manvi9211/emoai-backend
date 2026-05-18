from fastapi import APIRouter, Header
from pydantic import BaseModel, Field
from db.database import get_conn
from services.auth_service import get_user

router = APIRouter(prefix="/mood", tags=["mood"])


def _get_user_id(authorization: str) -> str:
    return get_user(authorization.replace("Bearer ", ""))["user_id"]


class MoodRequest(BaseModel):
    mood_score: int = Field(..., ge=1, le=5)
    mood_emoji: str


@router.post("")
def save_mood(req: MoodRequest, authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    conn = get_conn()
    conn.execute(
        "INSERT INTO mood_checkins (user_id, mood_score, mood_emoji) VALUES (?, ?, ?)",
        (user_id, req.mood_score, req.mood_emoji),
    )
    conn.commit()
    conn.close()
    return {"saved": True}


@router.get("/history")
def get_history(days: int = 7, authorization: str = Header(...)):
    user_id = _get_user_id(authorization)
    conn = get_conn()
    rows = conn.execute(
        """SELECT mood_score, mood_emoji, created_at
           FROM mood_checkins
           WHERE user_id = ?
             AND created_at >= datetime('now', ? || ' days')
           ORDER BY created_at ASC""",
        (user_id, f"-{days}"),
    ).fetchall()
    conn.close()
    return {"moods": [dict(r) for r in rows]}
