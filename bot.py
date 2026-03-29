import os
import instaloader
from aiogram import Bot, Dispatcher, types, executor

# 1. BOT TOKENINGIZNI SHU YERGA QO'YING
API_TOKEN = "8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw" 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loader = instaloader.Instaloader()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Salom! Menga Instagram profil havolasini (URL) yuboring.\n"
        "Men sizga o'sha profilning rasmini yuboraman."
    )

@dp.message_handler()
async def get_profile_pic(message: types.Message):
    user_input = message.text.strip()
    
    # Havoladan (URL) username'ni ajratib olish
    # Masalan: https://www.instagram.com/username/ -> username
    if "instagram.com/" in user_input:
        try:
            # URL'ni bo'laklarga bo'lib, username qismini olamiz
            parts = user_input.split("instagram.com/")[1].split("/")
            username = parts[0].split("?")[0] # Parametrlarni olib tashlaymiz
        except IndexError:
            await message.answer("❌ Havola noto'g'ri shaklda.")
            return
    else:
        # Agar shunchaki username yozilsa
        username = user_input.replace("@", "")

    msg = await message.answer("🔄 Profil rasmi qidirilmoqda...")

    try:
        # Instaloader orqali profilni yuklash
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil rasmining URL manzilini olish
        photo_url = profile.profile_pic_url
        
        # Rasmni foydalanuvchiga yuborish
        caption = (
            f"👤 **Ism:** {profile.full_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"👥 **Obunachilar:** {profile.followers}"
        )
        
        await message.answer_photo(photo_url, caption=caption, parse_mode="Markdown")
        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Xato: Bunday profil topilmadi yoki havola noto'g'ri.")
        print(f"Xato: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
