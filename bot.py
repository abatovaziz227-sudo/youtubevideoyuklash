import os
import instaloader
from aiogram import Bot, Dispatcher, types, executor

# Muhim: Hosting panelida (Environment Variables) BOT_TOKEN nomli o'zgaruvchi yarating
API_TOKEN = os.getenv("8424991362:AAGTzrYZBVXM9RWDE6LN5HsnFerJecSzyRw")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Instaloader obyektini yaratamiz
loader = instaloader.Instaloader()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Salom! Men Instagram profil rasmini yuklab beruvchi botman.\n\n"
        "Menga profil **username**ini yoki **link**ini yuboring."
    )

@dp.message_handler()
async def get_profile_pic(message: types.Message):
    user_input = message.text.strip()
    
    # Agar foydalanuvchi link yuborsa, undan username'ni ajratib olamiz
    if "instagram.com/" in user_input:
        username = user_input.split("instagram.com/")[1].split("/")[0].split("?")[0]
    else:
        username = user_input.replace("@", "")

    status_msg = await message.answer("🔍 Profil qidirilmoqda...")

    try:
        # Profil ma'lumotlarini olish
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil rasmi URL manzilini olish
        photo_url = profile.profile_pic_url
        
        # Rasmni bot orqali yuborish
        caption_text = (
            f"👤 **Ism:** {profile.full_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"👥 **Obunachilar:** {profile.followers}\n"
            f"📝 **Bio:** {profile.biography[:100]}..."
        )
        
        await message.answer_photo(photo_url, caption=caption_text, parse_mode="Markdown")
        await status_msg.delete()

    except instaloader.exceptions.ProfileNotExistsException:
        await status_msg.edit_text("❌ Bunday profil topilmadi. Username to'g'riligini tekshiring.")
    except Exception as e:
        await status_msg.edit_text("⚠️ Xatolik yuz berdi. Instagram hozirda so'rovni cheklagan bo'lishi mumkin.")
        print(f"Xato tafsiloti: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
