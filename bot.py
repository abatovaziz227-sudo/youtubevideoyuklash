import yt_dlp
import os
import sys
import time

# ================== TELEGRAM BOT TOKEN ==================
TELEGRAM_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

def download_video(url):
    if not url or not url.startswith(('http://', 'https://')):
        print("❌ Noto'g'ri link! YouTube linkini to'liq kiriting.\n")
        return

    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        'cookiefile': 'cookies.txt',
        'concurrent_fragment_downloads': 5,
        'retries': 15,
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Yuklash boshlandi, biroz kuting...\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Video') if info else 'Video'
            print(f"✅ Muvaffaqiyatli yuklandi: {title}\n")
    except Exception as e:
        print(f"❌ Xatolik: {e}\n")


# ====================== ASOSIY QISM ======================
if __name__ == "__main__":
    print("\n=== YouTube Video Yuklovchi ===\n")
    print(f"Telegram Token: {TELEGRAM_TOKEN[:20]}...\n")
    
    # Replit uchun qo'shimcha vaqt berish
    time.sleep(0.5)
    
    print("🎥 YouTube linkini yuboring:")
    print("(Chiqish uchun 'exit' yozing)\n")

    try:
        while True:
            url = sys.stdin.readline().strip()
            
            if not url:
                continue
            if url.lower() == 'exit':
                print("Dastur tugatildi. Xayr!")
                break
                
            download_video(url)
            print("🎥 Yana bir link yuboring:\n")
            
    except (EOFError, KeyboardInterrupt):
        print("\nDastur to'xtatildi.")
    except Exception as e:
        print(f"Kutilmagan xatolik: {e}")
