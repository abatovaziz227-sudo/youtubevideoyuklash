import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

# 🔴 TOKENNI SHU YERGA QO‘YING
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 YouTube link yuboring")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtu" not in url:
        await update.message.reply_text("❗ To‘g‘ri link yuboring")
        return

    await update.message.reply_text("⏬ Yuklanmoqda...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, 'rb'))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ Bot ishga tushdi")
app.run_polling()
