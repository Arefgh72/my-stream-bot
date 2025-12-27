import os
import asyncio
from pyrogram import Client, filters, idle

# دریافت اطلاعات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تعریف ربات بدون وب‌سرور
bot = Client(
    "SwiftStreamBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text("🚀 بالاخره وصل شدم!\n\nحالا هر فایلی داری بفرست تا تست کنیم.")

@bot.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_message(client, message):
    await message.reply_text("✅ فایل رو گرفتم، بزودی لینک دانلود رو برات میسازم.")

async def main():
    await bot.start()
    print("--- BOT IS ONLINE ---")
    await idle() # این دستور باعث میشه ربات روشن بمونه و گوش بده
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
