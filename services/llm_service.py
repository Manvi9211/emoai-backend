import requests
from fastapi import HTTPException
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_URL, MAX_TOKENS_REPLY, EMOTION_TONE_MAP


def _call(system: str, messages: list) -> str:
    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}",
                     "Content-Type": "application/json"},
            json={"model": OPENROUTER_MODEL, "messages": [
                {"role": "system", "content": system}, *messages], "max_tokens": MAX_TOKENS_REPLY},
            timeout=30,
        )
        data = resp.json()
        resp.raise_for_status()
        if "error" in data:
            raise HTTPException(
                status_code=500, detail=data["error"]["message"])
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504, detail="AI took too long. Try again.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def chat_reply(history: list, emotion_label: str, emotion_score: float) -> str:
    tone = EMOTION_TONE_MAP.get(emotion_label, EMOTION_TONE_MAP["neutral"])
    intensity = "strongly" if emotion_score > 0.7 else "somewhat"
    system = f"""You are EmoAI, a warm and empathetic AI companion.
The user is {intensity} feeling {emotion_label}. {tone}
Rules: Acknowledge the emotion FIRST. Ask ONE follow-up question. Keep to 2-4 sentences.
Never diagnose or claim to be a therapist."""
    return _call(system, history)


def journal_reflection(entry: str) -> str:
    system = """You are EmoAI, a compassionate journaling companion.
The user shared a journal entry. Your response must:
1. Reflect back what you heard with warmth (2-3 sentences)
2. Gently name the dominant emotion you noticed
3. Share one insight or pattern
4. End with ONE open-ended reflective question
Keep total response under 150 words. No advice unless asked. No diagnoses."""
    return _call(system, [{"role": "user", "content": entry}])
