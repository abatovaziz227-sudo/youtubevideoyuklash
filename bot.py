import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw"

logging.basicConfig(level=logging.INFO)

# Agar downloads papka yo‘q bo‘lsa yaratadi
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Video yuklab olish funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    # Agar cookies.txt mavjud bo‘lsa qo‘shadi
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Menga YouTube link yuboring!")

# Link kelganda ishlaydi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("⏬ Yuklanmoqda...")

        try:
            file_path = download_video(url)

            # Video yuborish
            await update.message.reply_video(video=open(file_path, 'rb'))

            # Faylni o‘chirish
            os.remove(file_path)

        except Exception as e:
            await update.message.reply_text(f"❌ Xatolik:\n{e}")
    else:
        await update.message.reply_text("❗ To‘g‘ri YouTube link yuboring")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Bot ishga tushdi...")
app.run_polling()
