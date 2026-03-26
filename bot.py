import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

os.makedirs("downloads", exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 YouTube link yuboring")

def download_video(url):
    ydl_opts = {
        'format': 'best',   # faqat eng oddiy format
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return None
            return ydl.prepare_filename(info)
    except:
        return None

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtu" not in url:
        await update.message.reply_text("❗ To‘g‘ri link yuboring")
        return

    await update.message.reply_text("⏬ Yuklanmoqda...")

    file_path = download_video(url)

    if not file_path or not os.path.exists(file_path):
        await update.message.reply_text("❌ Bu video yuklab bo‘lmadi (YouTube blok yoki cheklov)")
        return

    try:
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)
    except:
        await update.message.reply_text("❌ Video juda katta yoki yuborib bo‘lmadi")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ Ishga tushdi")
app.run_polling()
