from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import init_db
from routers import chat_router, mood_router, journal_router, auth_router

app = FastAPI(title="EmoAI API", version="4.0")

# ── CORS ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ─────────────────────────────────
app.include_router(chat_router.router)
app.include_router(mood_router.router)
app.include_router(journal_router.router)
app.include_router(auth_router.router)

# ── Startup ──────────────────────────────────────────


@app.on_event("startup")
def startup():
    init_db()
    print("Database ready.")

# ── Root route ───────────────────────────────────────


@app.get("/")
def root():
    return {"status": "EmoAI Week 4 running"}
