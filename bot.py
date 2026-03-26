import yt_dlp
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================== SIZNING TOKENINGIZ ==================
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

# Yuklab olingan videolar saqlanadigan papka
DOWNLOAD_DIR = "Downloaded_Videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "YouTube (yoki boshqa sayt) linkini yuboring, men uni yuklab beraman.\n"
        "Masalan: https://youtu.be/..."
    )

def download_with_yt_dlp(url: str):
    """yt-dlp yordamida video yuklab olish"""
    filepath = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    
    ydl_opts = {
        'outtmpl': filepath,
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'cookiefile': 'cookies.txt',                    # cookies.txt bo'lsa ishlatadi
        'extractor_args': {'youtube': {'player_client': ['android', 'default']}},
        'concurrent_fragment_downloads': 4,
        'retries': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, info.get('title', 'Video')
    except Exception as e:
        return None, str(e)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text("❌ Iltimos, to'g'ri link yuboring!")
        return

    msg = await update.message.reply_text("⏳ Yuklanmoqda... Biroz kuting (20-60 soniya)")

    # Video yuklash
    filename, title = download_with_yt_dlp(url)

    if filename and os.path.exists(filename):
        try:
            await msg.edit_text(f"✅ Yuklandi: {title}\n\n📤 Telegramga yuborilmoqda...")
            await update.message.reply_video(
                video=open(filename, 'rb'),
                caption=f"🎥 {title}",
                supports_streaming=True
            )
            os.remove(filename)  # Yuklab bo'lgach o'chirish
        except Exception as e:
            await msg.edit_text(f"❌ Video yuborishda xatolik: {e}")
    else:
        await msg.edit_text(f"❌ Yuklab bo'lmadi.\nXatolik: {title[:500]}")

# ====================== BOTNI ISHGA TUSHIRISH ======================
def main():
    print("🤖 Bot ishga tushmoqda...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot muvaffaqiyatli ishga tushdi! Telegramda sinab ko'ring.")
    app.run_polling()

if __name__ == "__main__":
    main()
