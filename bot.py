import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

# 🔴 TOKENNI SHU YERGA QO‘YING
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

# downloads papka yaratish
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 YouTube link yuboring")

# video yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    # cookies bo‘lsa qo‘shadi
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# link kelganda
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtu" not in url:
        await update.message.reply_text("❗ To‘g‘ri YouTube link yuboring")
        return

    await update.message.reply_text("⏬ Yuklanmoqda...")

    try:
        file_path = download_video(url)

        await update.message.reply_video(video=open(file_path, 'rb'))

        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik:\n{e}")

# botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("✅ Bot ishga tushdi")
app.run_polling()
