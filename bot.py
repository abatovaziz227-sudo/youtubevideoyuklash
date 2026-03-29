import os
import instaloader
from aiogram import Bot, Dispatcher, types, executor

# --- 1. SOZLAMALAR ---
API_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU" # BotFather'dan olgan tokeningiz
INSTA_USER = "abatovazizbek"               # Sessiya fayli nomidagi username

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loader = instaloader.Instaloader()

# --- 2. SESSİYANI YUKLASH FUNKSIYASI ---
def load_session():
    try:
        # Fayl nomi 'session-username' bo'lishi shart
        session_file = f"session-{INSTA_USER}"
        
        if os.path.exists(session_file):
            loader.load_session_from_file(INSTA_USER, filename=session_file)
            print(f"✅ MUVAFFAQIYAT: {session_file} yuklandi!")
            return True
        else:
            print(f"⚠️ OGOHLANTIRISH: {session_file} topilmadi. Bot cheklangan rejimda ishlaydi.")
            return False
    except Exception as e:
        print(f"❌ XATO: Sessiya yuklanmadi: {e}")
        return False

# Botni yoqishdan oldin sessiyani tekshiramiz
is_logged_in = load_session()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    status = "🟢 Tizimga kirilgan" if is_logged_in else "🟡 Loginsiz rejim"
    await message.reply(
        f"👋 Salom! Instagram profil linkini yuboring.\n\n"
        f"**Holat:** {status}\n"
        f"**Vazifa:** Profil rasmini (Avatar) yuklab berish."
    )

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.strip()
    
    # Instagram URL'dan username ajratib olish
    if "instagram.com/" in text:
        try:
            # https://www.instagram.com/username/ -> username
            username = text.split("instagram.com/")[1].split("/")[0].split("?")[0]
        except:
            await message.answer("❌ Havola noto'g'ri shaklda.")
            return
    else:
        username = text.replace("@", "")

    status_msg = await message.answer("🔍 Profil qidirilmoqda...")

    try:
        # Profilni yuklash
        profile = instaloader.Profile.from_username(loader.context, username)
        
        # Profil rasmi URL manzilini olish
        photo_url = profile.profile_pic_url
        
        # Telegramga yuborish
        caption = (
            f"👤 **Ism:** {profile.full_name}\n"
            f"🆔 **Username:** @{username}\n"
            f"👥 **Obunachilar:** {profile.followers:,}"
        )
        
        await message.answer_photo(photo_url, caption=caption, parse_mode="Markdown")
        await status_msg.delete()

    except instaloader.exceptions.LoginRequiredException:
        await status_msg.edit_text("❌ Instagram login talab qildi. Cookies faylini yangilang.")
    except instaloader.exceptions.ProfileNotExistsException:
        await status_msg.edit_text("❌ Bunday profil topilmadi.")
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Xatolik yuz berdi. (Bloklangan bo'lishi mumkin)")
        print(f"DEBUG: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
