import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw"

L = instaloader.Instaloader()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "instagram.com" in text:
        username = text.rstrip("/").split("/")[-1]
    else:
        username = text

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        L.download_profile(username, profile_pic_only=True)

        file_path = f"{username}/{username}_profile_pic.jpg"

        await update.message.reply_photo(photo=open(file_path, "rb"))

    except Exception as e:
        await update.message.reply_text("❌ Profil topilmadi yoki yopiq!")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
