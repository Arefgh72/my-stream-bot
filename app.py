import os
from pyrogram import Client, filters
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

# تنظیمات
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تعریف ربات
bot = Client("SwiftStreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# مدیریت چرخه حیات برنامه
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.start()
    print("--- Bot Started Successfully! ---")
    yield
    await bot.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health():
    return {"status": "running"}

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text("✅ ربات فعال است!\nفایل خود را بفرستید.")

@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_message(client, message):
    file_id = (message.document or message.video or message.audio).file_id
    # فعلاً برای تست لینک ساده می‌دهیم
    await message.reply_text(f"فایل دریافت شد!\nID: `{file_id}`")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
