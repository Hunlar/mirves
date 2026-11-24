import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
    API_ID = int(os.getenv("API_ID", "0") or "0")
    API_HASH = os.getenv("API_HASH", "").strip()
    SESSION_STRING = os.getenv("SESSION_STRING", "").strip()
    ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID", "0") or "0")
