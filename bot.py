import yt_dlp
import os
import sys

# ================== TELEGRAM BOT TOKEN ==================
TELEGRAM_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

def download_video(url):
    if not url or not url.startswith(('http://', 'https://')):
        print("❌ Noto'g'ri link! To'liq YouTube linkini kiriting.\n")
        return

    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        
        # Eng muhim o'zgartirishlar:
        'format': 'bestvideo[height<=1080]+bestaudio/best',   # 1080p gacha + audio (tezroq va barqaror)
        'merge_output_format': 'mp4',
        
        # Cookies
        'cookiefile': 'cookies.txt',
        
        # Qo'shimcha
        'concurrent_fragment_downloads': 5,
        'retries': 15,
        'extractor_args': {'youtube': {'player_client': ['default', 'android']}},
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Yuklash boshlandi, biroz kuting... (bu jarayon 10-60 soniya olishi mumkin)\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                print(f"✅ Muvaffaqiyatli yuklandi: {info.get('title', 'Video')}\n")
            else:
                print("⚠️ Video ma'lumotlari topilmadi.\n")
    except Exception as e:
        print(f"❌ Xatolik: {e}\n")


# ====================== ASOSIY QISM ======================
if __name__ == "__main__":
    print("=== YouTube Video Yuklovchi ===\n")
    print(f"Telegram Token: {TELEGRAM_TOKEN[:15]}...\n")
    print("🎥 YouTube linkini yuboring:\n")

    try:
        while True:
            url = sys.stdin.readline().strip()
            
            if not url:
                continue
            if url.lower() == 'exit':
                print("Dastur tugatildi.")
                break
                
            download_video(url)
            print("🎥 Yana link yuboring (chiqish uchun 'exit'):\n")
            
    except (EOFError, KeyboardInterrupt):
        print("\nDastur to'xtatildi.")
    except Exception as e:
        print(f"Kutilmagan xatolik: {e}")
