import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# --- SOZLAMALAR ---
# BotFather-dan olgan tokenni shu yerga qo'ying
TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

# Loglarni ko'rish (xatolarni terminalda ko'rsatadi)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- YUKLAB OLISH FUNKSIYASI ---
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',  # Papkadagi cookies.txt fayli
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # YouTube blokidan qochish uchun maxsus sozlamalar
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'Video')

# --- BOT BUYRUQLARI ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "🎬 Menga YouTube linkini yuboring, men uni yuklab beraman.\n\n"
        "⚠️ **Eslatma:** Agar video 50MB dan katta bo'lsa, Telegram cheklovi tufayli hujjat sifatida yuboriladi."
    )

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_youtube(message: types.Message):
    # Jarayon boshlanganini bildirish
    status = await message.answer("🔄 **Link tahlil qilinmoqda...**")
    
    try:
        # Yuklash papkasini tekshirish
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        url = message.text
        loop = asyncio.get_event_loop()
        
        await status.edit_text("📥 **Video yuklanmoqda...** (Bir oz kuting)")
        
        # Videoni yuklab olish (bloklamaslik uchun asinxron)
        file_path, title = await loop.run_in_executor(None, download_video, url)

        # Fayl hajmini aniqlash
        file_size = os.path.getsize(file_path) / (1024 * 1024) # MBda
        
        await status.edit_text(f"📤 **Telegramga yuborilmoqda...** ({file_size:.1f} MB)")
        
        video_input = types.FSInputFile(file_path)

        if file_size > 50:
            # 50MB limitidan oshsa hujjat sifatida yuboramiz
            await message.answer_document(
                document=video_input,
                caption=f"🎬 **{title}**\n\n✅ Hajmi katta bo'lgani uchun hujjat sifatida yuborildi."
            )
        else:
            # 50MB dan kichik bo'lsa video ko'rinishida
            await message.answer_video(
                video=video_input,
                caption=f"🎬 **{title}**\n\n✅ Tayyor!"
            )
        
        # Xabarni o'chirish va faylni serverdan tozalash
        await status.delete()
        os.remove(file_path)

    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            await status.edit_text("❌ **YouTube xatoligi:** Bot bloklandi. Yangi `cookies.txt` faylini yuklang yoki VPN ishlating.")
        else:
            await status.edit_text(f"❌ **Xatolik yuz berdi:**\n`{error_msg[:150]}`")
        
        # Xato bo'lganda ham fayl qolgan bo'lsa o'chirish
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

# --- ISHGA TUSHIRISH ---
async def main():
    print("Bot ishlamoqda... ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
