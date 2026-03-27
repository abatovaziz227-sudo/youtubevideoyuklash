import logging
import re
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv
import instaloader
from moviepy.editor import VideoFileClip

# ENV yuklash
load_dotenv()
API_TOKEN = os.getenv("8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

L = instaloader.Instaloader()

# START
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Instagram link yuboring, men musiqasini ajratib beraman 🎵")

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
            await message.answer("❌ Noto‘g‘ri link")
            return

        shortcode = match.group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # temp papka
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # yuklash
        L.download_post(post, target="temp")

        video_path = None

        # mp4 topish
        for file in os.listdir("temp"):
            if file.endswith(".mp4"):
                video_path = f"temp/{file}"
                break

        if not video_path:
            await message.answer("❌ Video topilmadi")
            return

        audio_path = video_path.replace(".mp4", ".mp3")

        # audio ajratish
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

        await message.answer_audio(FSInputFile(audio_path))

        clip.close()

        # tozalash
        os.remove(video_path)
        os.remove(audio_path)

        await message.answer("✅ Tayyor!")

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

# RUN
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
