import logging
import re
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from dotenv import load_dotenv
import instaloader
from moviepy import VideoFileClip

# ENV yuklash
load_dotenv()
API_TOKEN = os.getenv("8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi .env faylda!")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

L = instaloader.Instaloader()

# START
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("📥 Instagram link yuboring\nMen musiqasini ajratib beraman 🎵")

# AUDIO OLISH
@dp.message()
async def get_audio(message: Message):
    text = message.text

    if not text or "instagram.com" not in text:
        return

    await message.answer("⏳ Yuklanmoqda...")

    try:
        url = text.strip()

        # shortcode olish
        match = re.search(r"/(reel|p|tv)/([^/]+)/", url)
        if not match:
            await message.answer("❌ Noto‘g‘ri link yubordingiz")
            return

        shortcode = match.group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # temp papka
        os.makedirs("temp", exist_ok=True)

        # yuklash
        L.download_post(post, target="temp")

        video_path = None

        # mp4 topish
        for file in os.listdir("temp"):
            if file.endswith(".mp4"):
                video_path = os.path.join("temp", file)
                break

        if not video_path:
            await message.answer("❌ Video topilmadi")
            return

        audio_path = video_path.replace(".mp4", ".mp3")

        # 🎵 Audio ajratish (MoviePy 2.0+)
        with VideoFileClip(video_path) as clip:
            if clip.audio is None:
                await message.answer("❌ Audio topilmadi")
                return
            clip.audio.write_audiofile(audio_path)

        # yuborish
        await message.answer_audio(FSInputFile(audio_path))

        # tozalash
        try:
            os.remove(video_path)
            os.remove(audio_path)
        except:
            pass

        await message.answer("✅ Tayyor!")

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

# RUN
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
