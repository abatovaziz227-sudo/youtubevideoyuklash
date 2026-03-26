import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# --- SOZLAMALAR ---
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

# Loglarni yoqish (xatolarni terminalda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ANDROID REJIMIDAGI YUKLAB OLISH FUNKSIYASI ---
def download_video(url):
    ydl_opts = {
        # Eng yaxshi mp4 sifatni tanlash
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        
        # --- MUHIM: ANDROID SIMULYATSIYASI ---
        'user_agent': 'com.google.android.youtube/19.11.38 (Linux; U; Android 14; en_US; Pixel 8 Pro; Build/UQ1A.240205.004) gzip',
        'extractor_args': {
            'youtube': {
                'player_client': ['android'], # Faqat android mijozidan foydalanish
                'player_skip': ['webpage', 'configs'], # Web-tekshiruvlarni chetlab o'tish
            }
        },
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        'nocheckcertificate': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'Video')

# --- BOT INTERFEYSI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 🤖\n\n"
        "Men hozir **Android rejimida** ishlayapman. YouTube linkini yuboring!"
    )

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_youtube(message: types.Message):
    status = await message.answer("🔍 **Android protokoli orqali ulanilmoqda...**")
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = message.text
        loop = asyncio.get_event_loop()
        
        await status.edit_text("📥 **Yuklanmoqda...**")
        file_path, title = await loop.run_in_executor(None, download_video, url)

        file_size = os.path.getsize(file_path) / (1024 * 1024)
        await status.edit_text(f"📤 **Telegramga yuborilmoqda...** ({file_size:.1f} MB)")
        
        video_input = types.FSInputFile(file_path)
        
        if file_size > 50:
            await message.answer_document(video_input, caption=f"🎬 {title}")
        else:
            await message.answer_video(video=video_input, caption=f"🎬 {title}")
        
        await status.delete()
        os.remove(file_path)

    except Exception as e:
        error_text = str(e)
        if "Sign in to confirm" in error_text:
            await status.edit_text("❌ **Blok: Android rejimi ham yordam bermadi.** \n\n⚠️ Sizning IP-manzilingiz YouTube tomonidan qattiq cheklovga tushgan. Iltimos, **Warp 1.1.1.1** yoki **VPN** yoqib ko'ring.")
        else:
            await status.edit_text(f"❌ **Xato:** {error_text[:150]}")
        
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

async def main():
    print("Bot Android rejimida ishga tushdi! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
