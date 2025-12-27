import os
import asyncio
from pyrogram import Client, filters, idle
from fastapi import FastAPI
import uvicorn

# تنظیمات
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = FastAPI()

# تعریف ربات
bot = Client("SwiftStreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup_event():
    # اجرای ربات در پس‌زمینه
    await bot.start()
    print("--- Bot is LIVE and Listening ---")

@app.get("/")
async def health():
    return {"status": "Bot is Running"}

# دستور استارت
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    print(f"Received start from {message.from_user.id}") # برای تست در لاگ
    await message.reply_text("🚀 سلام! ربات با موفقیت متصل شد.\nفایل خود را بفرستید.")

# دریافت فایل
@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_message(client, message):
    await message.reply_text("✅ فایل دریافت شد! در حال پردازش...")

if __name__ == "__main__":
    # رندر معمولا پورت را از متغیر محیطی میگیرد، اگر نبود روی 10000 اجرا میشود
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
