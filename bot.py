import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL

# Bot tokeningizni kiriting
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Yuklab olish funksiyasi (Blokdan qochish uchun maksimal sozlangan)
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best', # Eng yaxshi mp4 format
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',  # Siz yangilagan fayl nomi
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # Brauzer simulyatsiyasi (Blokdan qochish uchun)
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'Video')

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "Menga YouTube linkini yuboring, men uni yuklab beraman. 📥\n"
        "_(Eslatma: 50MB dan katta videolar hujjat sifatida yuboriladi)_"
    )

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_video(message: types.Message):
    # Yuklash boshlanganini bildirish
    status_msg = await message.answer("🔄 **Link tahlil qilinmoqda...**")
    
    try:
        # Yuklash papkasini yaratish
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = message.text
        loop = asyncio.get_event_loop()
        
        await status_msg.edit_text("📥 **Video serverga yuklanmoqda...**")
        # Videoni yuklab olish
        file_path, title = await loop.run_in_executor(None, download_video, url)

        # Fayl hajmini tekshirish (Telegram botlar uchun 50MB limit)
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        
        await status_msg.edit_text(f"📤 **Telegramga yuborilmoqda...** ({file_size:.1f} MB)")
        
        video_file = types.FSInputFile(file_path)
        
        if file_size > 50:
            # 50MB dan katta bo'lsa hujjat sifatida
            await message.answer_document(
                video_file, 
                caption=f"🎬 **{title}**\n\n⚠️ Hajmi katta bo'lgani uchun hujjat sifatida yuborildi."
            )
        else:
            # 50MB dan kichik bo'lsa video formatida
            await message.answer_video(
                video=video_file, 
                caption=f"🎬 **{title}**\n\n✅ Yuklab olindi!"
            )
            
        # Tozalash
        await status_msg.delete()
        os.remove(file_path)

    except Exception as e:
        error_text = str(e)
        if "Sign in to confirm" in error_text:
            await status_msg.edit_text("❌ **Xato:** YouTube botni blokladi. `cookies.txt` faylini yangilang.")
        else:
            await status_msg.edit_text(f"❌ **Xatolik yuz berdi:**\n`{error_text[:100]}`")
        
        # Xato bo'lsa ham qoldiq faylni o'chirish
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

async def main():
    print("Bot muvaffaqiyatli ishga tushdi! ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
