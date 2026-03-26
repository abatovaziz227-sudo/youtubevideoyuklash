import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

# 🔴 TOKENNI SHU YERGA QO‘YING
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

# papka (xatosiz)
os.makedirs("downloads", exist_ok=True)

# start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 YouTube link yuboring")

# yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'ignoreerrors': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# link kelganda
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtu" not in url:
        await update.message.reply_text("❗ To‘g‘ri YouTube link yuboring")
        return

    await update.message.reply_text("⏬ Yuklanmoqda...")

    try:
        file_path = download_video(url)

        if file_path and os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, 'rb'))
            os.remove(file_path)
        else:
            await update.message.reply_text("❌ Video topilmadi")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik:\n{e}")

# bot ishga tushadi
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ Bot ishga tushdi")
app.run_polling()
