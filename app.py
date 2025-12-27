import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn

# دریافت اطلاعات از بخش Secrets (تنظیم شده در Settings > Secrets)
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ساخت اپلیکیشن سرور و ربات
app = FastAPI()
bot = Client("SwiftStreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await bot.start()
    print("--- Bot is Started! ---")

@app.get("/")
async def health_check():
    return {"status": "Online", "message": "SwiftStream Server is running smoothly!"}

# ۱. دستور /start (پیام خوش‌آمدگویی دوزبانه)
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    welcome_text = (
        "🚀 **Welcome to SwiftStream Bot**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🇮🇷 **فارسی:**\n"
        "من به شما کمک می‌کنم فایل‌های تلگرام را با **سرعت بالا** و **بدون فیلترشکن** دانلود کنید.\n\n"
        "✅ **چطور استفاده کنیم؟**\n"
        "۱- فایل یا ویدیو را برای من بفرستید.\n"
        "۲- لینک مستقیم و پرسرعت دریافت کنید.\n"
        "۳- با حداکثر سرعت دانلود کنید!\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🇬🇧 **English:**\n"
        "I help you download Telegram files with **High Speed** and **No VPN** required.\n\n"
        "✅ **How to use?**\n"
        "1- Send or forward a file to me.\n"
        "2- Get a direct high-speed link.\n"
        "3- Download at maximum speed!\n\n"
        "👇 **Send me a file to start!**\n"
        "👇 **برای شروع یک فایل بفرستید!**"
    )
    await message.reply_text(welcome_text)

# ۲. دریافت فایل و تولید لینک
@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_message(client, message):
    # تشخیص نوع فایل و گرفتن ID آن
    media = message.document or message.video or message.audio
    file_id = media.file_id
    file_name = getattr(media, 'file_name', 'SwiftStream_File')
    
    # ساخت آدرس Space شما (Hugging Face به طور خودکار این متغیر را دارد)
    # اگر از Cloudflare استفاده می‌کنی، می‌توانی آدرس آن را اینجا دستی جایگزین کنی
    space_id = os.environ.get('SPACE_ID', 'user/repo').replace('/', '-')
    base_url = f"https://{space_id}.hf.space"
    
    download_link = f"{base_url}/download/{file_id}"
    
    response_text = (
        "✅ **File Received! / فایل دریافت شد**\n\n"
        f"📄 **Name:** `{file_name}`\n"
        f"🔗 **Direct Link:** [Click to Download]({download_link})\n\n"
        "⚠️ **Note:** Link expires in 1 hour.\n"
        "⚠️ **توجه:** لینک تا ۱ ساعت دیگر منقضی می‌شود."
    )
    
    await message.reply_text(response_text, disable_web_page_preview=True)

# ۳. عملیات استریم (انتقال مستقیم فایل از تلگرام به کاربر)
@app.get("/download/{file_id}")
async def stream_file(file_id: str):
    async def file_generator():
        # دانلود تکه تکه فایل از تلگرام و ارسال همزمان به کاربر
        async for chunk in bot.iter_download(file_id):
            yield chunk

    return StreamingResponse(
        file_generator(), 
        media_type="application/octet-stream"
    )

# اجرا روی پورت مخصوص هانگینگ فیس
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
