import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# BotFather-dan olgan tokenni shu yerga qo'ying
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # MUHIM: YouTube blokidan qochish uchun eng yangi usul
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        # Brauzer ma'lumotlarini aniq ko'rsatish
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'Video')

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"Salom {message.from_user.first_name}! 👋\nLink yuboring, yuklab beraman.")

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_youtube(message: types.Message):
    status = await message.answer("🔄 **Tahlil qilinmoqda...**")
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = message.text
        loop = asyncio.get_event_loop()
        
        await status.edit_text("📥 **Yuklanmoqda...**")
        file_path, title = await loop.run_in_executor(None, download_video, url)

        file_size = os.path.getsize(file_path) / (1024 * 1024)
        await status.edit_text(f"📤 **Yuborilmoqda...** ({file_size:.1f} MB)")
        
        video_input = types.FSInputFile(file_path)
        if file_size > 50:
            await message.answer_document(video_input, caption=f"🎬 {title}")
        else:
            await message.answer_video(video=video_input, caption=f"🎬 {title}")
        
        await status.delete()
        os.remove(file_path)

    except Exception as e:
        await status.edit_text(f"❌ **Xato:** {str(e)[:150]}")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
