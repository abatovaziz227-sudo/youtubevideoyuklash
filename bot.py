import logging
import re
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import instaloader
from moviepy.editor import VideoFileClip

API_TOKEN = "8577880682:AAHOD8897USHI4I2XEhGZ8Ter51l05QtHCM"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

L = instaloader.Instaloader()

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply("Instagram link yuboring, men musiqasini ajratib beraman 🎵")

@dp.message_handler(lambda message: "instagram.com" in message.text)
async def get_audio(message: Message):
    url = message.text.strip()

    await message.reply("⏳ Yuklanmoqda...")

    try:
        shortcode = re.search(r"/(reel|p|tv)/([^/]+)/", url).group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        L.download_post(post, target="temp")

        video_path = f"temp/{post.shortcode}.mp4"
        audio_path = f"temp/{post.shortcode}.mp3"

        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

        await message.reply_audio(open(audio_path, "rb"))

        clip.close()
        os.remove(video_path)
        os.remove(audio_path)

        await message.reply("✅ Tayyor!")

    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
