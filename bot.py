import os
import instaloader
from aiogram import Bot, Dispatcher, types, executor

# 1. BOT TOKENINGIZNI SHU YERGA YOZING (tirnoq ichida!)
API_TOKEN = "8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw" 

# Bot va Dispatcher obyektlarini yaratamiz
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Instagram ma'lumotlarini yuklovchi obyekt
loader = instaloader.Instaloader()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Salom! Men Instagram profil rasmini yuklab beruvchi botman.\n\n"
        "Menga profil **username**ini (masalan: `cristiano`) yuboring."
    )

@dp.message_handler()
async def get_profile_pic(message: types.Message):
    user_input = message.text.strip()
    
    # Instagram linkidan username'ni ajratib olish (agar link yuborilsa)
    if "instagram.com/" in user_input:
        username = user_input.split("instagram.com/")[1].split("/")[0].split("?")[0]
    else:
        username = user_input.replace("@", "")

    status_msg = await message.answer("🔍 Profil qidirilmoqda...")

    try:
        # Profil ma'lumotlarini yuklash
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil rasmi URL manzilini olish
        photo_url = profile.profile_pic_url
        
        # Ma'lumotlarni yuborish
        caption_text = (
            f"👤 **Ism:** {profile.full_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"👥 **Obunachilar:** {profile.followers}\n"
        )
        
        await message.answer_photo(photo_url, caption=caption_text, parse_mode="Markdown")
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ Xatolik: Profil topilmadi yoki Instagram cheklov qo'ydi.")
        print(f"Xato tafsiloti: {e}")

if __name__ == '__main__':
    # Botni ishga tushirish
    executor.start_polling(dp, skip_updates=True)
