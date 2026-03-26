import os
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

# Bot tokeningizni kiriting
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Yuklab olish funksiyasi (Kengaytirilgan)
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',  # GitHubdagi faylingiz
        'noplaylist': True,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'Video')

# Start komandasi
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Tugmalar yaratish
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Yordam ❓", callback_data="help"))
    builder.row(types.InlineKeyboardButton(text="Dasturchi 👨‍💻", url="https://t.me/abatovaziz227")) # O'zingizni profilingizni qo'ying

    welcome_text = (
        f"Assalomu alaykum, {message.from_user.full_name}! 👋\n\n"
        "Men YouTube-dan video yuklab beruvchi botman.\n\n"
        "📥 **Video yuklash uchun link yuboring.**\n"
        "⚠️ *Eslatma: 50MB gacha video, undan kattasi hujjat sifatida yuboriladi.*"
    )
    
    await message.answer(welcome_text, reply_markup=builder.as_markup(), parse_mode="Markdown")

# Yordam tugmasi uchun
@dp.callback_query(F.data == "help")
async def help_callback(callback: types.CallbackQuery):
    help_text = (
        "📖 **Botdan foydalanish:**\n"
        "1. YouTube-dan video linkini nusxalang.\n"
        "2. Linkni shu yerga yuboring.\n"
        "3. Bir oz kuting, bot videoni yuboradi.\n\n"
        "Agar xatolik bo'lsa, link to'g'riligini tekshiring."
    )
    await callback.answer()
    await callback.message.answer(help_text, parse_mode="Markdown")

# Linklarni ushlash
@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def youtube_download(message: types.Message):
    status_msg = await message.answer("🔍 **Link tahlil qilinmoqda...**")
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = message.text
        loop = asyncio.get_event_loop()
        
        await status_msg.edit_text("📥 **Serverga yuklab olinmoqda...**")
        file_path, title = await loop.run_in_executor(None, download_video, url)

        file_size = os.path.getsize(file_path) / (1024 * 1024) # MB

        await status_msg.edit_text("📤 **Telegramga yuborilmoqda...**")
        
        video_file = types.FSInputFile(file_path)
        
        if file_size > 50:
            await message.answer_document(
                video_file, 
                caption=f"🎬 **{title}**\n\n⚖️ Hajmi: {file_size:.2f} MB\n✅ @SizningBot_nomi"
            )
        else:
            await message.answer_video(
                video=video_file, 
                caption=f"🎬 **{title}**\n✅ @SizningBot_nomi"
            )

        await status_msg.delete()
        os.remove(file_path)

    except Exception as e:
        await status_msg.edit_text(f"❌ **Xatolik yuz berdi:**\n`{str(e)[:100]}`", parse_mode="Markdown")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

# Botni yurgizish
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
