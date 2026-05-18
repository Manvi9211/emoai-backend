import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenRouter ────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ── Supabase ──────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# ── Database ──────────────────────────────────────────────
DB_PATH = "emoai.db"

# ── Limits ───────────────────────────────────────────────
MAX_HISTORY_MESSAGES = 10
MAX_TOKENS_REPLY = 400
MAX_INPUT_CHARS = 2000

# ── Crisis keywords ───────────────────────────────────────
CRISIS_KEYWORDS = [
    "kill myself", "want to die", "end my life", "suicide",
    "self harm", "hurt myself", "not worth living",
    "end it all", "no reason to live",
]

# ── Emotion tone map ──────────────────────────────────────
EMOTION_TONE_MAP = {
    "sadness":  "The user seems sad. Be gentle and validating. Acknowledge their pain first.",
    "anger":    "The user seems frustrated. Acknowledge it without judgment. Don't try to fix it immediately.",
    "fear":     "The user seems anxious. Be calm and reassuring. Help them feel safe.",
    "joy":      "The user seems happy. Match their energy warmly.",
    "surprise": "The user seems surprised. Be curious and engaged.",
    "disgust":  "The user seems bothered by something. Validate that their reaction makes sense.",
    "neutral":  "The user's tone is neutral. Be warm and curious — gently invite them to share more.",
}
