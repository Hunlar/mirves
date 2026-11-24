import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

from config import Config
from sources import get_source_status
from security import validate_media_url

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("site-stream-bot")

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# MTProto user session is required for group-call streaming.
user_client = Client(
    "stream_user",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION_STRING,
)
calls = PyTgCalls(user_client)


def allowed_chat(message: Message) -> bool:
    if Config.ALLOWED_CHAT_ID == 0:
        return True
    return bool(message.chat and message.chat.id == Config.ALLOWED_CHAT_ID)


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🎬 Site Stream Bot hazır.\\n\\n"
        "Komutlar:\\n"
        "/play URL - izinli doğrudan MP4/HLS akışını başlatır\\n"
        "/stop - yayından çıkar\\n"
        "/sources - kaynak modüllerinin durumunu gösterir\\n"
        "/id - sohbet kimliğini gösterir\\n\\n"
        "Not: Grup görüntülü sohbetini önce Telegram'da elle başlatın. "
        "Bot komutları ayrı bot hesabından, yayın ise SESSION_STRING ile "
        "bağlanan kullanıcı hesabından yapılır."
    )


@dp.message(Command("id"))
async def id_cmd(message: Message):
    await message.answer(f"Chat ID: `{message.chat.id}`")


@dp.message(Command("sources"))
async def sources_cmd(message: Message):
    lines = get_source_status()
    await message.answer("Kaynak modülleri:\\n" + "\\n".join(lines))


@dp.message(Command("play"))
async def play_cmd(message: Message):
    if not allowed_chat(message):
        await message.answer("Bu sohbet için kullanım yetkisi yok.")
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Kullanım: /play https://izinli-kaynak/ornek.m3u8")
        return
    url = parts[1].strip()
    ok, reason = validate_media_url(url)
    if not ok:
        await message.answer(f"Kaynak reddedildi: {reason}")
        return
    try:
        await calls.play(message.chat.id, MediaStream(url))
        await message.answer(
            "▶️ Yayın isteği gönderildi. Grup görüntülü sohbetinin önceden "
            "başlatılmış olması ve yayın hesabının grupta bulunması gerekir."
        )
    except Exception as exc:
        log.exception("Stream start failed")
        await message.answer(
            "Yayın başlatılamadı. Görüntülü sohbetin açık olduğunu, "
            "SESSION_STRING hesabının grupta bulunduğunu ve bağlantının "
            f"erişilebilir olduğunu kontrol edin. Ayrıntı: {type(exc).__name__}"
        )


@dp.message(Command("stop"))
async def stop_cmd(message: Message):
    if not allowed_chat(message):
        await message.answer("Bu sohbet için kullanım yetkisi yok.")
        return
    try:
        await calls.leave_call(message.chat.id)
        await message.answer("⏹️ Yayın durduruldu.")
    except Exception as exc:
        log.exception("Stop failed")
        await message.answer(f"Yayın durdurulamadı: {type(exc).__name__}")


async def health(request):
    return web.json_response({"status": "ok", "service": "telegram-site-stream-bot"})


async def main():
    web_app = web.Application()
    web_app.router.add_get("/", health)
    web_app.router.add_get("/health", health)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", "8080")))
    await site.start()

    await user_client.start()
    await calls.start()
    log.info("MTProto stream client started")
    try:
        await dp.start_polling(bot)
    finally:
        await calls.stop()
        await user_client.stop()
        await bot.session.close()
        await runner.cleanup()


if __name__ == "__main__":
    if not Config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN eksik.")
    if not (Config.API_ID and Config.API_HASH and Config.SESSION_STRING):
        raise SystemExit("API_ID, API_HASH ve SESSION_STRING eksik.")
    asyncio.run(main())
