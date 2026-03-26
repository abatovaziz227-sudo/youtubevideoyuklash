import yt_dlp
import os
import sys

# ================== TELEGRAM BOT TOKEN ==================
TELEGRAM_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

def download_video(url):
    if not url or not url.startswith(('http://', 'https://')):
        print("❌ Noto'g'ri link! YouTube linkini to'liq kiriting.\n")
        return

    # Yuklab olish joyi
    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        
        # ================== COOKIES ==================
        'cookiefile': 'cookies.txt',
        
        'concurrent_fragment_downloads': 8,
        'retries': 10,
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Yuklash boshlandi, biroz kuting...\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Muvaffaqiyatli yuklandi!\n")
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}\n")


# ====================== DASTURNI ISHGA TUSHIRISH ======================
if __name__ == "__main__":
    print("=== YouTube Video Yuklovchi ===\n")
    print(f"Telegram Token: {TELEGRAM_TOKEN[:15]}... (qo‘shilgan)\n")
    
    print("🎥 YouTube linkini yuboring:")
    
    try:
        while True:
            # Foydalanuvchidan linkni olish
            url = sys.stdin.readline().strip()
            
            if not url:        # Bo'sh qator bo'lsa davom ettir
                continue
                
            if url.lower() == 'exit':
                print("Dastur tugatildi. Xayr!")
                break
                
            # Linkni yuklash
            download_video(url)
            
            # Keyingi linkni so'rash
            print("🎥 Yana bir YouTube linkini yuboring (chiqish uchun 'exit' yozing):")
            
    except (EOFError, KeyboardInterrupt):
        print("\n\nDastur to'xtatildi.")
        sys.exit(0)
    except Exception as e:
        print(f"\nKutilmagan xatolik: {e}")
