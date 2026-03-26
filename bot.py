import yt_dlp
import os
import sys
import time

TELEGRAM_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

def download_video(url):
    if not url or not url.startswith(('http', 'https')):
        print("❌ Noto'g'ri link! To'liq YouTube linkini kiriting.\n")
        return

    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        
        # 2026-yil uchun eng yaxshi sozlamalar
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',  # 720p gacha, barqarorroq
        'merge_output_format': 'mp4',
        
        'cookiefile': 'cookies.txt',
        
        # YouTube bloklarini chetlab o'tish uchun
        'extractor_args': {'youtube': {'player_client': ['default', 'android', 'web']}},
        'concurrent_fragment_downloads': 4,
        'retries': 20,
        'sleep_interval': 5,          # YouTube bloklamasligi uchun
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Yuklash boshlandi... (30-90 soniya vaqt olishi mumkin)\n")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                title = info.get('title', 'Noma’lum video')
                print(f"✅ Muvaffaqiyatli yuklandi!\n   📁 {title}\n")
            else:
                print("⚠️ Video topildi, lekin yuklanmadi.\n")
    except Exception as e:
        print(f"❌ Xatolik: {str(e)[:300]}...\n")


# ====================== ASOSIY QISM ======================
if __name__ == "__main__":
    print("\n=== YouTube Video Yuklovchi ===\n")
    print(f"Token: {TELEGRAM_TOKEN[:20]}...\n")
    time.sleep(0.8)
    
    print("🎥 YouTube linkini yuboring:")
    print("(Chiqish uchun: exit)\n")

    try:
        while True:
            url = sys.stdin.readline().strip()
            
            if not url:
                continue
            if url.lower() == 'exit':
                print("✅ Dastur tugatildi.")
                break
                
            download_video(url)
            print("🎥 Yana link yuboring:\n")
            
    except (EOFError, KeyboardInterrupt):
        print("\nDastur to'xtatildi.")
    except Exception as e:
        print(f"Xatolik: {e}")
