import os
import instaloader
from aiogram import Bot, Dispatcher, types, executor

# --- 1. SOZLAMALAR ---
# Bot tokeningizni @BotFather'dan olib bu yerga qo'ying
API_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU" 

# Sessiya fayli yaratgan Instagram username'ingiz
INSTA_USER = "abatovazizbek" 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Instaloader'ni brauzer kabi ko'rsatish uchun "User-Agent" qo'shamiz
loader = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# --- 2. SESSİYANI YUKLASH ---
def load_session():
    try:
        # Fayl nomi 'session-username' bo'lishi shart
        session_file = f"session-{INSTA_USER}"
        
        if os.path.exists(session_file):
            loader.load_session_from_file(INSTA_USER, filename=session_file)
            print(f"✅ MUVAFFAQIYAT: {session_file} yuklandi!")
            return True
        else:
            print(f"❌ XATO: {session_file} fayli topilmadi!")
            return False
    except Exception as e:
        print(f"❌ SESSİYA XATOSI: {e}")
        return False

# Bot ishga tushishidan oldin sessiyani tekshirish
is_logged_in = load_session()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    status = "🟢 Tizimga kirilgan" if is_logged_in else "🟡 Loginsiz rejim"
    await message.reply(
        f"👋 Salom! Instagram profil linkini yoki username'ni yuboring.\n\n"
        f"**Bot holati:** {status}"
    )

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text.strip()
    
    # Username'ni ajratib olish
    if "instagram.com/" in user_input:
        try:
            username = user_input.split("instagram.com/")[1].split("/")[0].split("?")[0]
        except:
            await message.answer("❌ Havola noto'g'ri shaklda.")
            return
    else:
        username = user_input.replace("@", "")

    status_msg = await message.answer("🔍 Profil qidirilmoqda...")

    try:
        # Instagram'dan profil ma'lumotlarini olish
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil rasmi URL manzilini olish
        photo_url = profile.profile_pic_url
        
        # Telegramga rasmni yuborish
        caption = (
            f"👤 **Ism:** {profile.full_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"👥 **Obunachilar:** {profile.followers:,}"
        )
        
        await message.answer_photo(photo_url, caption=caption, parse_mode="Markdown")
        await status_msg.delete()

    except instaloader.exceptions.LoginRequiredException:
        await status_msg.edit_text("❌ Instagram login so'rayapti. Cookies (sessiya) ishlamadi.")
    except instaloader.exceptions.ProfileNotExistsException:
        await status_msg.edit_text("❌ Bunday profil topilmadi.")
    except Exception as e:
        # Xatoni aniq ko'rish uchun
        await status_msg.edit_text(f"⚠️ Xatolik: {str(e)[:50]}")
        print(f"DEBUG: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
